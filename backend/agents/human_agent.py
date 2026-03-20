def human_agent(state: dict):

    if state.get("decision") == "HUMAN_REQUIRED":

        print("\n🚨 HUMAN REVIEW REQUIRED")
        print("Message:", state.get("incident_text"))

        # ❌ NO input() here anymore
        # just pass state forward

        state["human_needed"] = True

    return state