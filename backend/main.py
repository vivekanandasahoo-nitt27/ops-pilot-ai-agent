from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()


@app.get("/")
def home():
    return {"message": "OpsPilot AI Running 🚀"}


@app.get("/logs")
def get_logs():
    try:
        with open("logs.json", "r") as f:
            return json.load(f)
    except:
        return []


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    try:
        with open("logs.json", "r") as f:
            logs = json.load(f)
    except:
        logs = []

    html = """
    <html>
    <head>
        <title>OpsPilot AI Dashboard</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid black; padding: 10px; }
            th { background-color: black; color: white; }
        </style>
    </head>
    <body>
        <h1>🚀 OpsPilot AI Dashboard</h1>
        <table>
            <tr>
                <th>Time</th>
                <th>Message</th>
                <th>Decision</th>
                <th>Action</th>
                <th>System</th>
            </tr>
    """

    for log in logs:
        html += f"""
        <tr>
            <td>{log.get('timestamp')}</td>
            <td>{log.get('message')}</td>
            <td>{log.get('decision')}</td>
            <td>{log.get('action')}</td>
            <td>{log.get('system')}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html