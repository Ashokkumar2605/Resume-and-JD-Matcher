 Simple AI Agent Backend — FastAPI + SQLite + LangChain
 Overview

This project implements the “brain” of a simple AI agent using a FastAPI backend.

The agent receives a natural language prompt, analyzes its intent using a rule-based router, and routes the request to one of two internal tools:

* Calculator Tool — evaluates math expressions

* Memory Tool — performs CRUD operations on a database

Technologies Used
Technology	Purpose
Python 3.13	Core language
FastAPI	REST API framework
Pydantic	Request/response validation
SQLite	Lightweight database
LangChain	Tool abstraction layer (agent-style design)

The Agent Brain (Router)

The core of the project is router.py, which:

Detects user intent using rule-based logic

Extracts entities from English sentences

Determines which tool to call

Prepares structured input for that tool

Examples:

Prompt	Tool	Tool Input
What is 10 plus 5?	Calculator	"10 + 5"
Remember my cat's name is Fluffy	Memory Save	{"key": "cat's name", "value": "Fluffy"}
What is my cat's name?	Memory Read	{"key": "cat's name"}
Calculator Tool
tool_calculate(expression: str)


Accepts a math expression string

Uses Python eval() with restricted globals

Returns the computed result

Security Note — Use of eval()

The calculator tool uses Python’s built-in eval() function as permitted by the assignment instructions.

However, eval() can execute arbitrary Python code if given malicious input, leading to code injection attacks.

Example malicious input:

__import__('os').system('rm -rf /')

✅ Mitigation Implemented

The evaluation environment is restricted:

allowed_globals = {"__builtins__": None}
eval(expression, allowed_globals, {})


This prevents access to:

os module

open()

import

any built-in Python functions

Only basic mathematical expressions are allowed.

Memory Tool

Implements database CRUD operations:

tool_save_memory(key, value)

tool_get_memory(key)

Table schema:

id	key	value
🔗 LangChain Usage

LangChain is used to wrap tools into agent-style Tool objects via tool_registry.py.

The router decides which tool to call, and LangChain handles tool abstraction and execution, similar to real AI agents.

Running the Application
1️. Install dependencies
pip install -r requirements.txt

2️. Run the API

From project root:

uvicorn main:app --reload

3️⃣ Open Swagger UI
http://127.0.0.1:8000/docs
