from integrations.email_reader import read_latest_email
from workflow.langgraph_flow import graph

email_data = read_latest_email()

if email_data:
    print("📧 Email received:", email_data)

    full_text = f"""
    Subject: {email_data['subject']}
    Body: {email_data.get('body', '')}
    """

    state = {
        "alert": email_data["subject"],
        "body": email_data.get("body", ""), 
        
        "incident_text": full_text,   # 🔥 FULL EMAIL
        "system": "email-system",
        "sender_email": email_data["sender"]
    }

    result = graph.invoke(state)

    print("\nFinal Result:", result)

else:
    print("No new emails")