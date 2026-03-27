def human_agent(state: dict):

    if state.get("decision") == "HUMAN_REQUIRED":

        print("\n🚨 HUMAN REVIEW REQUIRED")
        print("Message:", state.get("incident_text"))

        
        state["human_needed"] = True
        state["human_approval"] = ""
        state["human_input"] = ""

    return state