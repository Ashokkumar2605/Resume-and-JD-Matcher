from pydantic import BaseModel
from typing import Any, Optional


class AgentRequest(BaseModel):
    """
    Request model for /agent/query
    """
    prompt: str


class AgentResponse(BaseModel):
    """
    Standard response model returned by the agent
    """
    original_prompt: str
    chosen_tool: str
    tool_input: Optional[Any] = None
    response: Optional[Any] = None
    error: Optional[str] = None
