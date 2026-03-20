from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


def report_agent(state: dict):

    filename = "incident_report.pdf"

    c = canvas.Canvas(filename, pagesize=letter)

    text = c.beginText(50, 750)

    text.textLine("OpsPilot AI - Incident Report")
    text.textLine("-----------------------------")
    text.textLine(f"Timestamp: {datetime.now()}")
    text.textLine("")
    text.textLine(f"Incident: {state['incident_text']}")
    text.textLine(f"Type: {state['incident_type']}")
    text.textLine(f"Decision: {state.get('decision', 'N/A')}")
    text.textLine(f"System: {state['source_system']}")
    text.textLine("")
    text.textLine("Actions Taken:")
    text.textLine(state.get("action_taken", "No action recorded"))

    c.drawText(text)
    c.save()

    print(f"📄 Incident report generated: {filename}")

    return state