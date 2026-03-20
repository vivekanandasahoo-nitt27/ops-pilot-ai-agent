def ingestion_agent(state: dict):

    alert = state.get("alert", "")
    system = state.get("system", "unknown")

    # ✅ Set required fields
    state["incident_text"] = alert
    state["source_system"] = system

    return state