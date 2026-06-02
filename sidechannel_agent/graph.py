# sidechannel_agent/graph.py
import operator
from typing import Literal, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage
from langchain_anthropic import ChatAnthropic 
from langgraph.checkpoint.memory import MemorySaver 

from .state import AgentState
from .prompts import SYSTEM_PROMPT
from .tools import execute_adaptive_cpa, get_all_tools
from .report import generate_iteration_report

def build_cryptanalysis_graph():
    llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0)
    
    all_tools = get_all_tools()
    llm_with_tools = llm.bind_tools(all_tools)
    tool_node = ToolNode(all_tools)
    
    def agent_node(state: AgentState) -> dict:
        msgs = state["messages"]
        if not msgs or not isinstance(msgs[0], SystemMessage):
            msgs = [SystemMessage(content=SYSTEM_PROMPT)] + list(msgs)
        response = llm_with_tools.invoke(msgs)
        return {"messages": [response]}
        
    def reporting_node(state: AgentState) -> dict:
        """Invokes Claude to analyze the tool's raw mathematical metrics before pausing."""
        last_tool_msg = [m for m in state["messages"] if isinstance(m, ToolMessage)][-1]
        raw_content = last_tool_msg.content
        
        # Deduce what mode the attack was running in
        mode = "textbook"
        for m in reversed(state["messages"]):
            if isinstance(m, AIMessage) and m.tool_calls:
                mode = m.tool_calls[0]["args"].get("hypothesis_mode", "textbook")
                break
        
        print("[Telemetry Analyzer] Querying Claude for cryptanalytic assessment...")
        analysis_prompt = (
            f"You are an expert microarchitectural security auditor. Analyze the following raw CPA telemetry table "
            f"obtained from a target device running in {mode.upper()} mode. Provide a brief 2-3 sentence executive summary "
            f"explaining why the results succeeded or failed based on the correlation coefficients (ρ) and delta (Δρ) values.\n\n"
            f"Telemetry Table:\n{raw_content}"
        )
        
        ai_analysis = llm.invoke([HumanMessage(content=analysis_prompt)]).content
        
        # Calculate iteration count
        iteration_num = sum(1 for m in state["messages"] if isinstance(m, ToolMessage))
        
        # Append both the raw table and the AI's brief analysis into the dashboard template
        full_tool_output = f"{raw_content}\n\n LLM ANALYSIS:\n{ai_analysis}"
        
        formatted_report = generate_iteration_report(mode, full_tool_output, iteration_num)
        return {"iteration_report": formatted_report}

    def should_continue(state: AgentState) -> Literal["tools", "agent", "__end__"]:
        messages = state["messages"]
        last_msg = messages[-1]
        
        if hasattr(last_msg, "tool_calls") and len(last_msg.tool_calls) > 0:
            return "tools"
            
        if isinstance(last_msg, HumanMessage):
            return "agent"
            
        if isinstance(last_msg, AIMessage) and not last_msg.tool_calls:
            has_succeeded = any("CRITICAL ANALYSIS STATUS: SUCCESS" in getattr(m, "content", "") for m in messages if isinstance(m, ToolMessage))
            if not has_succeeded:
                return "agent"
                
        return END

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("reporting_node", reporting_node)
    
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges("agent", should_continue, {
        "tools": "tools",
        "agent": "agent",
        END: END
    })
    
    workflow.add_edge("tools", "reporting_node")
    workflow.add_edge("reporting_node", "agent")
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory, interrupt_after=["reporting_node"])