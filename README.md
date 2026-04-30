# 🤖 Mini Chat Bot

A modular conversational AI chatbot built in Python that connects to the OpenAI API, manages multiple agents with custom behaviors, and persists full conversation history in a PostgreSQL database.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [Token Management](#-token-management)

---

## ✨ Features

- 🧠 **Multi-agent support** — create and manage multiple AI agents, each with its own name, behavior, and configuration.
- 💬 **Persistent conversations** — every message and conversation is stored in a PostgreSQL database.
- 🔢 **Token control** — tracks token usage per query and per conversation to avoid exceeding limits.
- 🗂️ **JSON-based agent config** — agents are stored and loaded from a `agents.json` file for easy management.
- 🏗️ **Clean layered architecture** — separated into agent, services, db, and config layers.

---

## 📁 Project Structure

```
mini_chat_bot/
├── main.py                  # Entry point
├── actions.py               # High-level actions
├── agent/
│   ├── connection.py        # OpenAI client connection
│   ├── config_IA.py         # Load, save and update agent settings
│   ├── agent_setter.py      # Name and behavior setters
│   └── query_executor.py    # Executes queries against the OpenAI API
├── config/
│   ├── config.py            # Base directory and global config
│   ├── json_init.py         # JSON agent initialization
│   └── agents.json          # Stored agent configurations
├── db/
│   ├── initialize_db.py     # Database connection context manager
│   ├── models_db.py         # Pydantic models and SQL mappers
│   ├── get_data.py          # UUID and date helpers
│   ├── queries_db.py        # Raw query utilities
│   ├── sql_language.py      # SQL helpers
│   └── tables_db/
│       ├── conversation_repository.py  # CRUD for conversations
│       └── message_repository.py       # CRUD for messages
└── services/
    ├── tokens_service.py    # Token counting via tiktoken
    └── message_service.py   # Query/output message formatting
```

---

## ⚙️ Requirements

- Python 3.10+
- PostgreSQL
- An OpenAI API key

**Python dependencies:**

```
openai
tiktoken
python-dotenv
sqlalchemy
psycopg2-binary
pydantic
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🚀 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-user/mini_chat_bot.git
cd mini_chat_bot
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up the database:**

```bash
psql -U postgres -c "CREATE DATABASE mini_chat_bot_of;"
psql -U postgres -d mini_chat_bot_of -c "CREATE USER ai_app WITH PASSWORD 'your_password';"
psql -U postgres -d mini_chat_bot_of -c "GRANT ALL PRIVILEGES ON DATABASE mini_chat_bot_of TO ai_app;"
```

5. **Configure your `.env` file** (see [Configuration](#-configuration)).

6. **Initialize the database tables:**

```bash
python -c "from db.initialize_db import DataBaseMCB; DataBaseMCB().init()"
```

---

## 🔧 Configuration

Create a `.env` file in the root directory:

```env
API_KEY_OPENAI=your_openai_api_key_here
DATABASE_URL=postgresql://ai_app:your_password@localhost/mini_chat_bot_of
```

---

## 💻 Usage

Run the chatbot from the terminal:

```bash
python main.py
```

**First run — no agents created yet:**

```
you doesn't have any agents created. Let's create one
Give him a name: Aria
Give him a behavior: You are a helpful and concise assistant.
```

**Subsequent runs — choose an existing agent:**

```
Aria
create
Choose one you want to use: Aria

Hola, soy Aria.
¿En que te puedo ayudar hoy?

> What's the capital of France?
Paris is the capital of France.
```

**Commands during chat:**

| Input                         | Effect                      |
| ----------------------------- | --------------------------- |
| Any text                      | Send a message to the agent |
| `create` (at agent selection) | Create a new agent          |

The session ends automatically when the token limit is reached.

---

## 🏗️ Architecture

The project follows a layered architecture where each layer has a single responsibility:

```
main.py
   │
   ├── agent/          → Connects to OpenAI, manages agent config, executes queries
   │
   ├── services/       → Formats messages, counts tokens
   │
   ├── db/             → Persists conversations and messages to PostgreSQL
   │
   └── config/         → Loads environment, manages agents.json
```

**Data flow per user message:**

```
user input
    ↓
TokensQuery         (count tokens, validate limit)
    ↓
HandlingQuery       (format to {"role": "user", "content": ...})
    ↓
MessageRepository   (save user message to DB)
    ↓
QueryExecutor       (send full memory to OpenAI API)
    ↓
HandlingOutPut      (format to {"role": "assistant", "content": ...})
    ↓
MessageRepository   (save assistant message to DB)
    ↓
print response
```

---

## 🔢 Token Management

The bot enforces two token limits:

| Limit                      | Description                                  |
| -------------------------- | -------------------------------------------- |
| `max_input_tokens`         | Max tokens allowed per single user query     |
| `tokens_limit_chat` (3000) | Max total tokens for the entire conversation |

If either limit is exceeded, the session ends with a message and the loop breaks. This prevents runaway API costs.

---

## 📄 License

MIT License. Feel free to use, modify, and distribute this project.
