# run_attack.py
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from sidechannel_agent.graph import build_cryptanalysis_graph

def main():
    load_dotenv()
    print("=== INITIALIZING ===")
    
    app = build_cryptanalysis_graph()
    config = {"configurable": {"thread_id": "director_interactive_session"}}
    
    initial_trigger = HumanMessage(
        content="Initialize side-channel exploration loops across the target file channels."
    )
    
    print("Running initial hardware sweep...")
    for event in app.stream({"messages": [initial_trigger], "target_byte": 0, "recovered_key": [], "status": "analyzing", "iteration_report": ""}, config, stream_mode="values"):
        pass

    while True:
        state = app.get_state(config)
        
        # Check if execution is paused at the reporting gate
        if state.next == ('agent',):
            print(state.values.get("iteration_report", "No telemetry compiled."))
            
            # Check if total success has already been verified
            if "SUCCESS" in state.values.get("iteration_report", ""):
                print("Extraction complete. Exiting dashboard session.")
                break
                
            director_input = input("Director Input (Press [ENTER] to proceed autonomously): ").strip()
            
            if director_input:
                print(f"\n[Director Gate] Injecting human feedback constraints: '{director_input}'")
                app.update_state(config, {"messages": [HumanMessage(content=director_input)]})
            else:
                print("\n[Director Gate] Approved. Resuming processing loops autonomously...")
                
            for event in app.stream(None, config, stream_mode="values"):
                pass
                
        elif not state.next:
            print("\nAnalysis Complete. Final State Established.")
            break

if __name__ == "__main__":
    main()