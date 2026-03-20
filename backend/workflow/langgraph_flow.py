from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agents.decision_agent import decision_agent
from agents.ingestion_agent import ingestion_agent
from agents.classifier_agent import classifier_agent

from agents.action_agent import action_agent
from agents.human_agent import human_review
from agents.report_agent import report_agent
from agents.reply_agent import reply_agent
from agents.decision_agent import decision_agent

class IncidentState(TypedDict, total=False):
    alert: str
    system: str
    incident_text: str
    source_system: str
    incident_type: str
    
    
    decision: Optional[str]
    auto_reply: Optional[str]
    sender_email: Optional[str]
    action_taken: Optional[str]
    human_approval: Optional[str]
    
   
   
def decision_router(state):

    decision = state.get("decision")

    if decision == "AUTO_REPLY":
        return "reply"

    elif decision == "HUMAN_REQUIRED":
        return "human_review"

    elif decision == "ALERT":
        return "action"

    else:
        print("⚠️ Decision missing, defaulting to human_review")
        return "human_review"
    
    
workflow = StateGraph(IncidentState)

workflow.add_node("ingestion", ingestion_agent)
workflow.add_node("classification", classifier_agent)
workflow.add_node("decision", decision_agent)
workflow.add_node("action", action_agent)
workflow.add_node("human_review", human_review)
workflow.add_node("report", report_agent)
workflow.add_node("reply", reply_agent)

workflow.set_entry_point("ingestion")

workflow.add_edge("ingestion", "classification")
workflow.add_edge("classification", "decision")
workflow.add_conditional_edges(
    "decision",
    decision_router,
    {
        "reply": "reply",
        "human_review": "human_review",
        "action": "action"
    }
)
workflow.add_edge("reply", "action")
workflow.add_edge("human_review", "action")
workflow.add_edge("action", "report")
workflow.add_edge("report", END)

graph = workflow.compile()