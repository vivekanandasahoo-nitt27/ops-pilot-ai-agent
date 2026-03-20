from integrations.slack import send_slack_alert
from integrations.email_sender import send_email
from utils.logger import log_event
def action_agent(state: dict):

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

        state["action_taken"] = "Slack alert sent"

    # 🟡 HUMAN REQUIRED
    elif decision == "HUMAN_REQUIRED":

        approval = state.get("human_approval", "").strip().lower()

        if approval == "yes":
            print("✅ Human approved action")

            send_email(
                to_email=state.get("sender_email"),
                subject="Re: Your Message",
                body=state.get("auto_reply", "Approved. Proceeding.")
            )

            state["action_taken"] = "Human approved and smart email sent"

        else:
            print("❌ Human rejected action")
            state["action_taken"] = "Action rejected by human"
    else:
        print("⚠️ Unknown decision")
        state["action_taken"] = "No action taken"
    log_event(state)
    return state