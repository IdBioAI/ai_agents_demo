# 📚 Library Management Agent

AI-powered library assistant built with n8n that helps users search and manage books through natural language queries.

## 🏗️ Architecture Overview

This project implements an intelligent library agent that combines:
- **MySQL Database** for structured data storage
- **OpenAI Chat Model** for natural language processing
- **n8n Workflow** for orchestration and tool integration
- **Simple Memory** for conversation context


### Tables

#### `authors`

#### `books`

#### `loans`


## 🚀 Usage

### API Endpoint
**POST** `https://your-n8n-instance.com/webhook/d51bd6d7-a5ff-492b-a26c-3d92cc8a2024`

### Request Format
```json
{
  "msg": "Your natural language query here",
  "sessionId": "unique_user_identifier"
}
```

### Example Requests

#### Basic Book Search
```json
{
  "msg": "Kolik máme knih? napiš jejich názvy a k nim autora",
  "sessionId": "uzivatel_2"
}
```

#### Author-based Search
```json
{
  "msg": "Máte knihy od Tolkiena?",
  "sessionId": "user_123"
}
```

#### Genre Inquiry
```json
{
  "msg": "Jaké máte fantasy knihy?",
  "sessionId": "fantasy_lover"
}
```

#### Availability Check
```json
{
  "msg": "Je dostupný Hobit?",
  "sessionId": "reader_456"
}
```

## 🛠️ Technical Components

### Core Technologies
- **n8n**: Workflow automation platform
- **MySQL 8.0**: Relational database
- **OpenAI GPT**: Large Language Model for natural language processing
- **Docker**: Containerization

### n8n Nodes Used
- **Webhook Trigger**: Receives user requests
- **OpenAI Chat Model**: Processes natural language
- **Simple Memory**: Maintains conversation context
- **MySQL**: Database operations (SELECT queries)
- **Respond to Webhook**: Returns formatted responses

### Capabilities
- ✅ Natural language book search
- ✅ Author-based queries
- ✅ Genre filtering
- ✅ Availability checking
- ✅ Conversation memory
- ❌ Book reservations (read-only mode)
- ❌ Data modifications

### Testing the Agent

Use curl to test the webhook:
```bash
curl -X POST \
  http://localhost:5678/webhook/d51bd6d7-a5ff-492b-a26c-3d92cc8a2024 \
  -H "Content-Type: application/json" \
  -d '{
    "msg": "Kolik máme knih v knihovně?",
    "sessionId": "test_user"
  }'
```

## 📝 Sample Data

## 🤖 Agent Capabilities

### What the Agent Can Do
- Search books by title, author, or genre
- Check book availability
- Provide book recommendations
- Answer questions about library inventory
- Maintain conversation context across requests

### Example Conversations
```
User: "Máte nějaké české autory?"
Agent: "Ano, v naší knihovně máme Karel Čapek, který napsal R.U.R. z roku 1920..."

User: "A je ta kniha dostupná?"
Agent: "R.U.R. od Karla Čapka je dostupná - máme 1 výtisk k dispozici..."
```

## 🔒 Limitations

- **Read-only operations**: Agent can only query data, not modify it
- **Simple memory**: Basic conversation context, not persistent across sessions
- **No authentication**: Open webhook endpoint
- **Single language**: Primarily designed for Czech language queries
