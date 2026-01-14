from typing import TypedDict, Optional, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]
    intent: Optional[str]

    # Lead capture fields
    lead_mode: Optional[bool]
    lead_step: Optional[str]

    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]
