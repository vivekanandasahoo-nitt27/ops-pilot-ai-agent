from integrations.slack import send_slack_alert
from integrations.email_sender import send_email
from utils.logger import log_event
from agents.reply_agent import reply_agent
def action_agent(state: dict):
    token = state.get("auth_token")

    if not token:
        state["action_taken"] = "❌ Not authenticated"
        return state
    print(f"🔐 Using token: {token[:10]}...")

    print("\n🚀 Executing response actions")

    decision = state.get("decision")
    print("Decision:", decision)

    # 🟢 AUTO REPLY
    if decision == "AUTO_REPLY":

        print("📧 Sending auto reply email")

        send_email(
            to_email=state.get("sender_email"),
            subject="Re: Your Message",
            body=state.get("auto_reply", "Thank you for your message.")
        )

        state["action_taken"] = "Auto email reply sent"

    # 🔴 ALERT
    elif decision == "ALERT":

        print("🚨 Sending Slack alert")
        send_slack_alert(state)

        # 🔥 ALSO send smart email reply
        if state.get("sender_email"):

            print("📧 Sending alert acknowledgment email")

            send_email(
                to_email=state.get("sender_email"),
                subject="Re: " + state.get("alert", ""),
                body=state.get("auto_reply", 
                    "Your request has been received and is under review by our team.")
            )

        state["action_taken"] = "Slack alert + email reply sent"

    # 🟡 HUMAN REQUIRED
    elif decision == "HUMAN_REQUIRED":

        approval = state.get("human_approval", "").strip().lower()

        if approval == "yes":
            print("✅ Human approved action")

            # 🔥 Generate smart reply FIRST
            state = reply_agent(state)

            send_email(
                to_email=state.get("sender_email"),
                subject="Re: " + state.get("alert", ""),
                body=state.get("auto_reply", "Approved, proceeding.")
            )

            state["action_taken"] = "Human approved and smart email sent"

        else:
            print("❌ Human rejected action")
            state["action_taken"] = "Action rejected by human"
        
        
    log_event(state)
    return state