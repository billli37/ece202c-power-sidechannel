# sidechannel_agent/state.py
from typing import TypedDict, Annotated, Sequence, List
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    target_byte: int
    recovered_key: List[str]
    status: str
    iteration_report: str