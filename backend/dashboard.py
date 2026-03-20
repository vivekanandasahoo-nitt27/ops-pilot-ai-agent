import gradio as gr
from integrations.email_reader import read_latest_email
from workflow.langgraph_flow import graph
from agents.reply_agent import reply_agent
from agents.action_agent import action_agent
from utils.logger import log_event

current_state = {}

# ==============================
# 📧 FETCH + ANALYZE EMAIL
# ==============================
def fetch_email():

    global current_state

    email = read_latest_email()

    if not email:
        return "No new email", "", "", ""

    full_text = f"""
Subject: {email['subject']}
Body: {email.get('body', '')}
"""

    state = {
        "alert": email["subject"],
        "body": email.get("body", ""),
        "incident_text": full_text,
        "system": "email-system",
        "sender_email": email["sender"]
    }

    state = graph.invoke(state)

    current_state = state

    decision_text = f"Decision: {state.get('decision')}"

    return full_text, decision_text, "", ""

# ==============================
# 👤 HUMAN ACTION
# ==============================
def human_action(action):

    global current_state

    if not current_state:
        return "No email analyzed"

    current_state["human_approval"] = "yes" if action == "approve" else "no"

    try:
        current_state = reply_agent(current_state)
        current_state = action_agent(current_state)
    except Exception as e:
        return f"Error handled: {str(e)}"

    return f"Final Result:\n{current_state}"

# ==============================
# 📜 LOAD LOGS (POINTWISE)
# ==============================
def show_logs():

    logs = log_event()

    formatted = ""

    for log in logs:
        formatted += f"🕒 {log['timestamp']} | {log['message']} → {log['decision']} → {log['action']}\n\n"

    return formatted


# ==============================
# 🎨 UI
# ==============================
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# 🚀 OpsPilot AI Dashboard")

    # 📧 SECTION 1
    gr.Markdown("## 📧 Analyze Email")

    fetch_btn = gr.Button("Fetch & Analyze Email")

    email_box = gr.Textbox(label="Email Content", lines=5)
    decision_box = gr.Textbox(label="Decision")

    # 👤 SECTION 2
    gr.Markdown("## 👤 Human Approval")

    approve_btn = gr.Button("✅ Approve")
    reject_btn = gr.Button("❌ Reject")

    # ⚙️ SECTION 3
    gr.Markdown("## ⚙️ Action Result")

    action_output = gr.Textbox(lines=10)

    # 📜 SECTION 4
    gr.Markdown("## 📜 Activity Logs")

    log_btn = gr.Button("Load Logs")
    log_output = gr.Textbox(lines=10)

    # ==============================
    # 🔗 CONNECT EVENTS
    # ==============================

    fetch_btn.click(fetch_email, outputs=[email_box, decision_box, action_output, log_output])

    approve_btn.click(lambda: human_action("approve"), outputs=action_output)
    reject_btn.click(lambda: human_action("reject"), outputs=action_output)

    log_btn.click(show_logs, outputs=log_output)

demo.launch()