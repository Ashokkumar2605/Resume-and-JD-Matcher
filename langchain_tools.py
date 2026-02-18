# langchain_tools.py

from langchain_tools import Tool
from tools.calculator import tool_calculate
from tools.memory import tool_save_memory, tool_get_memory


# -------------------------------
# Wrap tools as LangChain Tools
# -------------------------------

calculator_tool = Tool(
    name="Calculator",
    func=tool_calculate,
    description="Performs mathematical calculations from a string expression"
)

memory_save_tool = Tool(
    name="MemorySave",
    func=lambda data: tool_save_memory(data["key"], data["value"]),
    description="Saves a key-value pair to memory"
)

memory_read_tool = Tool(
    name="MemoryRead",
    func=lambda data: tool_get_memory(data["key"]),
    description="Retrieves a value from memory using a key"
)


# -------------------------------
# Tool Executor (used by FastAPI)
# -------------------------------

def execute_tool(tool_name: str, tool_input):
    if tool_name == "calculator":
        return calculator_tool.func(tool_input)

    if tool_name == "memory_save":
        return memory_save_tool.func(tool_input)

    if tool_name == "memory_read":
        return memory_read_tool.func(tool_input)

    return {"error": "Unknown tool"}
