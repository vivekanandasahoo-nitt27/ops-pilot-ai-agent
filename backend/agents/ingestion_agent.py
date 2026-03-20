def ingestion_agent(state: dict):

    alert = state.get("alert", "")
    body = state.get("body", "")
    system = state.get("system", "unknown")

    # 🔥 Build full email context properly
    full_text = f"""
Subject: {alert}
Body: {body}
"""

    state["incident_text"] = full_text
    state["source_system"] = system

    return state