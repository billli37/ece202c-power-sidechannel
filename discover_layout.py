import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from sidechannel_agent.graph import build_cryptanalysis_graph

def main():
    load_dotenv()
    print("=== STARTING STAGE 1: COMPILE-TIME PARAMETER DISCOVERY ===")
    
    app = build_cryptanalysis_graph()
    config = {"configurable": {"thread_id": "compile_time_discovery"}}
    
    prompt = HumanMessage(
        content="Inspect the physical execution file 'ascad_mini.h5' and map the underlying hardware alignment parameters."
    )
    
    # Run the agentic loop past the supervisor gates
    for event in app.stream({"messages": [prompt]}, config, stream_mode="values"):
        pass
        
    state = app.get_state(config)
    if state.next == ('tools',):
        print("[Director Gate] Approving hardware alignment profiling pass...")
        for event in app.stream(None, config, stream_mode="values"):
            pass
            
    print("Stage 1 Complete. Hardware rule map generated successfully.")

if __name__ == "__main__":
    main()