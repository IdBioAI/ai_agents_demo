from openai import OpenAI
import requests
import json
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Define custom tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_etc_balance_by_address",
            "description": (
                "Returns information about an Ethereum Classic (ETC) account based on its address. "
                "The result includes fields such as:\n"
                "- `coin_balance`: string, the balance is calculated as (coin_balance / 10^18).\n"
                "- `exchange_rate`: string, current ETC to USD rate \n"
                "Other fields provide metadata."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "etc_address": {
                        "type": "string",
                        "description": "The address of the ETC account in hexadecimal format, starting with '0x'.",
                    }
                },
                "required": ["etc_address"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_info_from_web_search",
            "description": (
                "Performs a web search using a powerful AI-enabled search engine to retrieve up-to-date information from the internet. "
                "This tool is used to fetch live data such as exchange rates, news, or other information that requires accessing current web content."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query what information to retrieve from the web.",
                    }
                },
                "required": ["query"],
            },
        }
    },
]

function_map = {
    "get_etc_balance_by_address": lambda args: get_etc_balance_by_address(args["etc_address"]),
    "get_info_from_web_search": lambda args: get_info_from_web_search(args["query"]),
}


def get_etc_balance_by_address(etc_address: str):
    url = "https://etc.blockscout.com/api/v2/addresses/" + etc_address
    headers = {
        "Content-Type": "application/json"
    }
    timeout = 5

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"blockscout API call error: {e}")
        return None


def get_info_from_web_search(query: str):
    print("get_info_from_web_search query:" + query)
    response = client.chat.completions.create(
        model="gpt-4o-search-preview",
        messages=[
            {
                "role": "developer",
                "content": "Answer in very short, concise sentences. No explanations, no URLs, no extra text."
            },
            {
                "role": "user",
                "content": query
            }
        ],
    )

    print("get_info_from_web_search query response:" + response.choices[0].message.content)
    return response.choices[0].message.content


def get_response_from_llm(messages: []):
    iteration = 0

    while iteration < 3:
        iteration += 1

        response = client.chat.completions.create(
            model="gpt-4o",
            tools=tools,
            tool_choice="auto",
            parallel_tool_calls=False,
            messages=messages,
        )

        # Check if there are tool calls
        if response.choices[0].message.tool_calls:
            # Add the assistant's message with tool calls to history
            messages.append({
                "role": "assistant",
                "content": response.choices[0].message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    }
                    for tc in response.choices[0].message.tool_calls
                ]
            })

            for tool_call in response.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                tool_id = tool_call.id

                result = function_map[function_name](function_args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_id,
                    "name": function_name,
                    "content": json.dumps(result)
                })
        else:
            # No tool calls - we have our final answer
            final_content = response.choices[0].message.content

            # Add the final assistant message to history
            messages.append({
                "role": "assistant",
                "content": final_content
            })

            return final_content


def main():
    test_etc_address = "0x75a263044914A34838ba3a438A7fCBE9BEa76E51"
    messages = [
        {"role": "developer",
         "content": "Financial advisor (cryptocurrency). Speak only Czech. Answer without formatting, plain text for console."},
        {
            "role": "user",
            "content": f"What is ETC balance on address {test_etc_address}"
                       " look up the current CZK→USD exchange rate from"
                       " https://www.kurzy.cz/kurzy-men/kurzovni-listek/ceska-narodni-banka/"
                       " and convert the ETC balance into CZK.",
        },
    ]

    reply_text = get_response_from_llm(messages)

    print("--------------------------")
    print(reply_text)


if __name__ == "__main__":
    main()
