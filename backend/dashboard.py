import gradio as gr
import requests

from integrations.email_reader import read_latest_email
from workflow.langgraph_flow import graph
from agents.reply_agent import reply_agent
from agents.action_agent import action_agent

# 🔁 Global state
current_state = {}


# ==============================
# 📧 FETCH + ANALYZE EMAIL
# ==============================
def fetch_email():

    global current_state

    email = read_latest_email()

    if not email:
        return "No new email", "", "", "", ""

    full_text = f"""Subject: {email['subject']}
Body: {email.get('body', '')}"""

    state = {
        "alert": email["subject"],
        "body": email.get("body", ""),
        "incident_text": full_text,
        "system": "email-system",
        "sender_email": email["sender"]
    }

    # Run graph (NO human input here)
    state = graph.invoke(state)

    current_state = state

    decision = state.get("decision", "")
    incident_type = state.get("incident_type", "")

    # 👤 Human message
    human_msg = ""
    if state.get("human_review"):
        human_msg = f"🚨 HUMAN REVIEW REQUIRED\n\n{full_text}"

    return full_text, decision, incident_type, human_msg, ""


# ==============================
# 👤 HUMAN ACTION
# ==============================
def human_action(action):

    global current_state

    if not current_state:
        return "No email analyzed"

    current_state["human_approval"] = "yes" if action == "approve" else "no"

    # ❌ Reject
    if action == "reject":
        current_state["action_taken"] = "❌ Action rejected by human"
        return format_result(current_state)

    # ✅ Approve
    try:
        current_state = reply_agent(current_state)
        current_state = action_agent(current_state)
    except Exception as e:
        return f"Error handled: {str(e)}"

    return format_result(current_state)


# ==============================
# 📜 FORMAT RESULT (CLEAN)
# ==============================
def format_result(state):

    return f"""
📌 ALERT: {state.get('alert')}

🧠 DECISION: {state.get('decision')}
📂 TYPE: {state.get('incident_type')}

📧 REPLY:
{state.get('auto_reply', 'N/A')}

⚙️ ACTION:
{state.get('action_taken')}

👤 APPROVAL:
{state.get('human_approval', 'N/A')}
"""


# ==============================
# 📜 LOAD LOGS (POINTWISE)
# ==============================
def load_logs():

    try:
        logs = requests.get("http://127.0.0.1:8000/logs").json()
    except:
        return "No logs found"

    formatted = ""

    for log in logs:
        formatted += f"""
🕒 {log.get('timestamp')}
📩 {log.get('message')}
🧠 {log.get('decision')}
⚙️ {log.get('action')}
-------------------------
"""

    return formatted


# ==============================
# 🎨 UI (CLEAN + STRUCTURED)
# ==============================
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# 🚀 OpsPilot AI Dashboard")

    # ------------------------------
    # 📧 EMAIL SECTION
    # ------------------------------
    gr.Markdown("## 📧 Email Analysis")

    fetch_btn = gr.Button("Fetch & Analyze Email")

    email_box = gr.Textbox(label="Email Content", lines=5)
    decision_box = gr.Textbox(label="Decision")
    type_box = gr.Textbox(label="Incident Type")

    # ------------------------------
    # 👤 HUMAN SECTION
    # ------------------------------
    gr.Markdown("## 👤 Human Review")

    human_msg_box = gr.Textbox(label="Human Review Required", lines=4)

    with gr.Row():
        approve_btn = gr.Button("✅ Approve")
        reject_btn = gr.Button("❌ Reject")

    # ------------------------------
    # ⚙️ RESULT SECTION
    # ------------------------------
    gr.Markdown("## ⚙️ Action Result")

    result_box = gr.Textbox(lines=10)

    # ------------------------------
    # 📜 LOG SECTION
    # ------------------------------
    gr.Markdown("## 📜 Logs")

    log_btn = gr.Button("Load Logs")
    log_box = gr.Textbox(lines=10)

    # ------------------------------
    # 🔗 CONNECTIONS
    # ------------------------------

    fetch_btn.click(
        fetch_email,
        outputs=[email_box, decision_box, type_box, human_msg_box, result_box]
    )

    approve_btn.click(lambda: human_action("approve"), outputs=result_box)
    reject_btn.click(lambda: human_action("reject"), outputs=result_box)

    log_btn.click(load_logs, outputs=log_box)


# ==============================
# 🚀 LAUNCH
# ==============================
demo.launch()