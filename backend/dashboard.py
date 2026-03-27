import gradio as gr
import requests

from integrations.email_reader import read_latest_email
from workflow.langgraph_flow import graph
from agents.reply_agent import reply_agent
from agents.action_agent import action_agent
from agents.voice_of_the_doctor import text_to_speech_with_elevenlabs
from agents.voice_of_the_patient import transcribe_with_groq
import requests
import webbrowser

# 🔁 Global state
current_state = {}



#the voice input 
def process_voice(audio_path):
    if audio_path:
        text = transcribe_with_groq(audio_path)
        print("🎤 Transcribed:", text)
        return text   # 👈 goes to textbox
    return ""

# ==============================
# 📧 FETCH + ANALYZE EMAIL
# ==============================
def fetch_email():

    global current_state

    # 🔐 Get Auth0 Token
    try:
        res = requests.get("http://localhost:5000/get-token")
        token = res.json().get("token")
    except:
        token = None

    print("DEBUG TOKEN:", token)  # 👈 ADD THIS

    if not token:
        return "❌ Please login first", "", "", "", "",None 

    # ✅ IMPORTANT: DO NOT overwrite state
    state = {}

    # 🔥 ADD TOKEN INTO STATE
    state["auth_token"] = token

    email = read_latest_email()

    if not email:
        return "No new email", "", "", "", "",None 

    full_text = f"""Subject: {email['subject']}
Body: {email.get('body', '')}"""

    state.update({
    "alert": email["subject"],
    "body": email.get("body", ""),
    "incident_text": full_text,
    "system": "email-system",
    "sender_email": email["sender"]
    })

    # Run graph (NO human input here)
    state = graph.invoke(state)

    current_state = state

    decision = state.get("decision", "")
    incident_type = state.get("incident_type", "")

    # 👤 Human message
    human_msg = ""
    if state.get("human_review"):
        human_msg = f"🚨 HUMAN REVIEW REQUIRED\n\n{full_text}"
        
    #speech output
    # 🔊 AI SPEECH (ONLY EMAIL + DECISION)
    speech_text = f"""
    New email received.

    Subject: {state.get("alert")}

    Body: {state.get("body")}

    Decision: {state.get("decision")}

    Incident Type: {state.get("incident_type")}

    Please review and provide instructions if needed.
    Then approve or reject.
    """

    audio_path = text_to_speech_with_elevenlabs(speech_text)

    return full_text, decision, incident_type, human_msg, "",audio_path  


# ==============================
# 👤 HUMAN ACTION
# ==============================
def human_action(action, human_text):

    global current_state

    if not current_state:
        return "No email analyzed"

    current_state["human_approval"] = "yes" if action == "approve" else "no"
    current_state["human_input"] = human_text 

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
import json
import os

def load_logs():

    base_path = os.path.dirname(os.path.dirname(__file__))
    log_path = os.path.join(base_path, "logs.json")

    try:
        with open(log_path, "r") as f:
            logs = json.load(f)
    except Exception as e:
        return f"No logs found: {str(e)}"

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




def open_login():
    webbrowser.open("http://localhost:5000/login")
    return "🔐 Opening Auth0 login..."

# ==============================
# 🎨 UI (CLEAN + STRUCTURED)
# ==============================
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# 🚀 OpsPilot AI Dashboard")

    # ------------------------------
    # 📧 EMAIL SECTION
    # ------------------------------
    gr.Markdown("## 📧 Email Analysis")
    login_btn = gr.Button("🔐 Login with Auth0")

    fetch_btn = gr.Button("Fetch & Analyze Email")

    email_box = gr.Textbox(label="Email Content", lines=5)
    decision_box = gr.Textbox(label="Decision")
    type_box = gr.Textbox(label="Incident Type")
    # 🔊 OUTPUT (AI speaks email)
    voice_output = gr.Audio(label="🔊 AI Reading Email", autoplay=True)

    # ------------------------------
    # 👤 HUMAN SECTION
    # ------------------------------
    gr.Markdown("## 👤 Human Review")
    with gr.Row():
        voice_input = gr.Audio(
        sources=["microphone"],
        type="filepath",
        label="🎤 Speak Additional Instructions"
        )

        human_input_box = gr.Textbox(
        label="Additional Instructions (optional)",
        placeholder="e.g. tell him I will be late",
        interactive=True 
        )

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
    
    voice_input.change(
    fn=process_voice,
    inputs=voice_input,
    outputs=human_input_box
    )

    fetch_btn.click(
        fetch_email,
        outputs=[email_box, decision_box, type_box, human_input_box, result_box,voice_output]
    )

    approve_btn.click(
    fn=human_action,
    inputs=[gr.State("approve"), human_input_box],
    outputs=result_box
    )
    reject_btn.click(
    fn=human_action,
    inputs=[gr.State("reject"), human_input_box],
    outputs=result_box
    )

    log_btn.click(load_logs, outputs=log_box)
    login_btn.click(fn=open_login, outputs=result_box)


# ==============================
# 🚀 LAUNCH
# ==============================
demo.launch()