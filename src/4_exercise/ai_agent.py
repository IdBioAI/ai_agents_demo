from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import List, Annotated, Dict
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.types import interrupt
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
import wikipedia
import json
from src.database_init import create_quiz_database, execute_query


DEBUG = False


class State(TypedDict):
    messages: Annotated[list, add_messages]


model = ChatOpenAI(model="gpt-4o")


# =============================================================================
# TOOLS
# =============================================================================

@tool
def select_topics_from_db(sql_query: str) -> str:
    """
    Search topics in database by SQL query.
    Can be used for finding similar topics.
    """
    if DEBUG:
        print(f"Executing SQL query for topics: {sql_query}")

    results = execute_query(sql_query)
    return json.dumps(results, ensure_ascii=False, indent=2)


@tool
def select_questions_from_db(sql_query: str) -> str:
    """
    Search questions in database by SQL query.
    """
    if DEBUG:
        print(f"Executing SQL query for questions: {sql_query}")

    results = execute_query(sql_query)
    return json.dumps(results, ensure_ascii=False, indent=2)


@tool
def inset_questions_to_db(sql_query: str) -> str:
    """
    Insert questions to database using SQL INSERT query.
    """
    if DEBUG:
        print(f"Inserting questions with SQL: {sql_query}")

    results = execute_query(sql_query)

    if results and "error" in results[0]:
        return "error - " + results[0]["error"]
    else:
        return "success"


@tool
def insert_new_topic_to_db_and_questions(insert_query_topic: str, insert_query_questions: str) -> str:
    """
    Insert new topic and its questions using SQL queries.

    IMPORTANT: In "insert_query_questions" SQL query use topic_id as placeholder, use string [topic_id] (without quotes).
    For this purpose .replace('[topic_id]', str(topic_id)) function will be used!
    """
    if DEBUG:
        print(f"🔄 Inserting new topic with questions")
        print(f"Topic query: {insert_query_topic}")
        print(f"Questions query: {insert_query_questions}")

    try:
        # 1. INSERT topic
        topic_result = execute_query(insert_query_topic)

        if "error" in topic_result[0]:
            if DEBUG:
                print(f"Error creating topic: {topic_result[0]['error']}")
            return "Chyba při vytváření tématu"

        # 2. get new topic id
        topic_id = topic_result[0]["last_id"]
        if DEBUG:
            print(f"Newly created topic has ID: {topic_id}")

        # 3. replace placeholder "topic_id" with new topic id
        questions_insert_final = insert_query_questions.replace('[topic_id]', str(topic_id))
        if DEBUG:
            print(f"Final questions query: {questions_insert_final}")

        # 4. INSERT questions
        questions_result = execute_query(questions_insert_final)

        if "error" in questions_result[0]:
            if DEBUG:
                print(f"Error creating questions: {questions_result[0]['error']}")
            return "Chyba při vytváření otázek"

        questions_count = questions_result[0]["affected_rows"]

        return f"Úspěšně vytvořeno téma s ID {topic_id} a {questions_count} otázkami"

    except Exception as e:
        if DEBUG:
            print(f"Error inserting questions or topic: {str(e)}")
        return f"Chyba při vytváření tématu a otázek"


@tool
def get_text_from_wikipedia(query: str) -> str:
    """
    Search information about topic on Wikipedia.

    QUERY RULES:
    - Use exact topic name in nominative singular form

    Examples of correct queries:
    - "kočka" (not "kočky")
    - "Python programming language" (not "Python")
    - "astronomie" (not "hvězdy")
    """
    if DEBUG:
        print(f"🌐 Searching Wikipedia for: {query}")

    try:
        wikipedia.set_lang("cs")

        page = wikipedia.page(query)
        return page.summary[:200]

    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
        try:
            wikipedia.set_lang("en")
            page = wikipedia.page(query)
            return page.summary[:200]
        except Exception as e:
            return f"Téma '{query}' nebylo na Wikipedii nalezeno. Chyba: {str(e)}"


@tool
def exit_program() -> str:
    """Virtual tool. Exit Question Generator Agent program."""
    return ""


tools = [
    select_topics_from_db,
    get_text_from_wikipedia,
    inset_questions_to_db,
    insert_new_topic_to_db_and_questions,
    exit_program
]


# =============================================================================
# WORKFLOW NODES
# =============================================================================

def question_agent(state: State):
    """Main chatbot node - processes user input and calls tools"""

    last_message = state["messages"][-1] if state["messages"] else None
    is_tool_result = hasattr(last_message, 'name') and hasattr(last_message, 'tool_call_id')

    # If it's not tool result, ask for user input
    if not is_tool_result:
        user_input = input("\n❓ Vaše volba: ")
        user_message = {"role": "user", "content": user_input}
        state["messages"].append(user_message)
        print("🤖 Agent rozhoduje...")
    else:
        if DEBUG:
            print("Model processing tool result...")

    model_with_tools = model.bind_tools(tools, parallel_tool_calls=False)
    response = model_with_tools.invoke(state["messages"])

    if response.content:
        print(f"💬 Agent odpověděl: \n {response.content}")

    if hasattr(response, 'tool_calls') and response.tool_calls:
        if DEBUG:
            print(f"Agent called tool: {response.tool_calls[0]['name']}")

    return {"messages": [response]}


def should_continue(state: State):
    """Decide where to go based on last tool result"""

    # Get last message
    last_message = state["messages"][-1] if state["messages"] else None

    # Check if it's ToolMessage with name "exit_program"
    if (hasattr(last_message, 'name') and
            last_message.name == "exit_program"):
        return "exit"

    return "question_agent"


def create_question_agent():
    graph_builder = StateGraph(State)
    tool_node = ToolNode(tools=tools)

    # add nodes
    graph_builder.add_node("question_agent", question_agent)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_edge("question_agent", "tools")

    graph_builder.add_conditional_edges(
        "tools",
        should_continue,
        {
            "question_agent": "question_agent",
            "exit": END
        }
    )
    graph_builder.add_edge(START, "question_agent")

    # Memory according to documentation
    memory = InMemorySaver()
    graph = graph_builder.compile(checkpointer=memory)

    # Visualize
    try:
        graph_image = graph.get_graph().draw_mermaid_png()
        with open("question_workflow_graph.png", "wb") as f:
            f.write(graph_image)
        if DEBUG:
            print("Graph saved as question_workflow_graph.png")
    except Exception as e:
        if DEBUG:
            print(f"Failed to save graph: {e}")

    return graph


def run_question_agent():
    graph = create_question_agent()

    initial_state = {
        "messages": [{"role": "system", "content": """
           You are Question Generator Agent - intelligent assistant for creating questions only in Czech language. 
           
           DATABASE SCHEMA:
           
           Table 'topics':
           - id (INTEGER PRIMARY KEY AUTOINCREMENT)
           - name (TEXT NOT NULL UNIQUE) 
           - description (TEXT) MAX 255 chars
           
           Table 'questions':
           - id (INTEGER PRIMARY KEY AUTOINCREMENT)
           - topic_id (INTEGER NOT NULL) - FOREIGN KEY to topics.id
           - question_text (TEXT NOT NULL)
           
            If you have topic ID available, don't use WHERE name but id in queries
           DECISION LOGIC:
           
           When user provides request, decide by type:
           - "all topics" or "show topics" → call 'select_topics_from_db("SELECT * FROM topics")'
           - specific topic name → call 'select_topics_from_db("SELECT * FROM topics WHERE name LIKE '%name%'")'
           - "topics with questions" → call 'select_topics_from_db("SELECT t.name, COUNT(q.id) as question_count FROM topics t LEFT JOIN questions q ON t.id = q.topic_id GROUP BY t.id, t.name")'
           
           If you don't understand query, apologize and ask for clarification.
        
           If user provides topic for question generation or directly writes that questions should be generated for some topic:
           - first check if topic already exists using SQL query
           - if yes, inform user about it and always write under which ID the topic is stored
           - if not, inform user and let them decide if they want to create the topic.
           - if user selected to generate questions and you already have text from wikipedia, generate maximum number of questions from it. Generate only questions, not answers. Then display questions to user. User will then confirm if they want to save these questions to database.
           - If topic doesn't exist and you already have generated questions, use function "insert_new_topic_to_db_and_questions", where SQL query for topic insert and SQL query for questions save will be generated.
             If topic exists in chat history find its ID and generate insert sql query
            
"""}],
    }

    config = {"configurable": {"thread_id": "question-session-1"}}

    try:
        # Simple run without interrupt handling
        for event in graph.stream(initial_state, config):
            if DEBUG:
                print(f"Event: {list(event.keys())}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    create_quiz_database(False, DEBUG)

    print("🤖 Vítejte v AI Agentovi pro generování otázek!")
    print("Jsem váš inteligentní asistent pro vytváření a správu otázek.")

    run_question_agent()
