
from fastapi import FastAPI
from models import AgentRequest, AgentResponse
from router import route_prompt
from langchain_tools import execute_tool
from database import init_db

app = FastAPI(title="Simple AI Agent")

# Create DB table at startup
init_db()


@app.post("/agent/query", response_model=AgentResponse)
def agent_query(request: AgentRequest):
    prompt = request.prompt

    # Step 1: Agent brain decides tool
    routing = route_prompt(prompt)
    tool_name = routing["tool"]
    tool_input = routing["tool_input"]

    # Step 2: Handle unknown tool
    if tool_name == "unknown":
        return AgentResponse(
            original_prompt=prompt,
            chosen_tool=tool_name,
            tool_input=None,
            response=None,
            error="I do not have a tool for that."
        )

    # Step 3: Execute tool via LangChain layer
    result = execute_tool(tool_name, tool_input)

    # Step 4: Return unified response
    return AgentResponse(
        original_prompt=prompt,
        chosen_tool=tool_name,
        tool_input=tool_input,
        response=result,
        error=None
    )
