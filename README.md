# 🚀 OpsPilot AI Agent

### Intelligent Email Automation with Human-in-the-Loop + Voice AI

---

## 📌 Overview

**OpsPilot AI Agent** is an intelligent automation system that reads emails, classifies intent, decides actions, and generates human-like responses — with **human approval and voice interaction**.

It combines:

* 🤖 AI decision-making
* 👤 Human-in-the-loop validation
* 🔊 Voice input/output
* 🔐 Secure authentication

---

## 🎯 Key Features

### 📧 Email Intelligence

* Fetch and analyze emails
* Classify into:

  * Meeting
  * Casual
  * Alert (e.g., payments, urgent issues)

---

### 🧠 AI Decision Engine (LangGraph)

* AUTO_REPLY → sends reply automatically
* HUMAN_REQUIRED → asks for approval
* ALERT → triggers actions (Slack, etc.)

---

### 👤 Human-in-the-Loop

* Approve / Reject actions
* Add **custom instructions**
* Instructions are included in final reply

---

### 🔊 Voice AI Integration

* 🎤 Speak additional instructions (Speech → Text)
* 🔈 AI reads email summary (Text → Speech)

---

### 📤 Smart Email Replies

* Context-aware replies
* No hallucination (controlled prompt)
* Human-like tone (1–2 lines)

---

### 🔐 Secure Authentication

* Auth0 integration
* Token-based access
* No hardcoded credentials

---

### 📊 Logs & Monitoring

* JSON-based logging
* Track actions, decisions, approvals

---
## 🏗️ Final System Architecture (Fully Connected with Human Email Flow)

```text
                ┌──────────────────────────────┐
                │ 🔐 Auth0 Authentication      │
                └──────────────────────────────┘
                               |
                ┌──────────────────────────────┐
                │ 📧 Email Input (Gmail/IMAP)  │
                └──────────────┬───────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │ 🧠 Ingestion Agent           │
                └──────────────┬───────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │ 🔍 Classification Agent       │
                └──────────────┬───────────────┘
                               │
                               ▼
                ┌────────────────────────────────────────┐
                │ ⚖️ Decision Agent                      │
                │ AUTO_REPLY | HUMAN_REQUIRED | ALERT    │
                └───────┬────────────┬────────────┬──────┘
                        │            │            |
                        ▼            ▼            |___________________________
                                                                              |
                                                                              |
        ┌──────────────────────┐   ┌──────────────────────────────┐   ┌──────────────────────┐
        │ 🤖 AUTO FLOW         │   │ 👤 HUMAN FLOW                │   │ 🚨 ALERT FLOW        │
        └──────────┬───────────┘   └──────────────┬───────────────┘   └──────────┬───────────┘
                   │                              │                              │
                   ▼                              ▼                              ▼

        ┌──────────────────────┐   ┌────────────────────────────────────────┐   ┌──────────────────────┐
        │ 🧠 Reply Agent       │   │ 🖥️ Gradio Dashboard                    │   │ ⚙️ Action Agent       │
        │ (Auto reply)         │   │                                        │   │ - Slack alerts       │
        └──────────┬───────────┘   │ 🔈 Voice Output (TTS)                  │   │ - Escalation         │
                   │               │ 🎤 Voice Input (Whisper)               │   └──────────┬───────────┘
                   ▼               │ ⌨️ Human Input (Text)                 │              │
        ┌──────────────────────┐   │ ✅ Approve / ❌ Reject                 │              ▼
        │ 📤 Email Sender      │   └──────────────┬────────────────────────┘      ┌──────────────────────┐
        │ (Auto send)          │                  │                               │ 📊 Logging            │
        └──────────┬───────────┘                  ▼                               └──────────────────────┘
                   │               ┌──────────────────────────────┐                        |
                   │               │ 🧠 Reply Agent               │              __________________________
                   │               │ (Uses human + context)       │              | 🧠 Reply Agent         |
                   │               └──────────────┬───────────────┘              |  (Uses human + context)| 
                   │                              │                              |________________________|
                   │                              ▼                                         |
                   │               ┌──────────────────────────────┐                         |
                   │               │ 📤 Email Sender              │                        |
                   │               │ (Human-approved send)        │                         |
                   │               └──────────────┬───────────────┘                         |
                   │                              │                                         |
                   ▼                              ▼                                         |
            ┌──────────────────────────────────────────────┐                                |
            │ ⚙️ Action Agent (Unified Execution Layer)    │<_______________________________|
            │ - Final execution                           │
            │ - Slack / Email / Logging                   │
            └──────────────┬───────────────────────────────┘
                           │
                           ▼
                ┌──────────────────────────────┐
                │ 📊 Report Agent / Logs       │
                └──────────────────────────────┘


                
```

### 🤖 AUTO FLOW

```text
Decision → Reply Agent → Email Sender → Action → Logs
```

---

### 👤 HUMAN FLOW (FIXED ✅)

```text
Decision → Dashboard → Human Input (Voice/Text)
        → Reply Agent → Email Sender → Action → Logs
```

👉 Human ALSO sends email now (correct behavior)

---

### 🚨 ALERT FLOW

```text
Decision → Action Agent → Slack → Logs
```

---

## 🔁 KEY DESIGN INSIGHT

👉 **ALL email sending flows pass through Email Sender**

* Auto replies ✅
* Human-approved replies ✅

---

## 🔊 VOICE FLOW

* 🔈 AI reads email BEFORE decision
* 🎤 Human gives input BEFORE approval
* Used inside reply generation

---


```

---

## 🧩 Tech Stack

| Layer         | Technology           |
| ------------- | -------------------- |
| AI Models     | Groq (LLaMA 3.1)     |
| Orchestration | LangGraph            |
| Backend       | Python               |
| UI            | Gradio               |
| Auth          | Auth0                |
| Email         | SMTP (Gmail)         |
| Voice         | ElevenLabs + Whisper |
| Deployment    | Docker               |

---

## 📁 Project Structure

```
backend/
│
├── agents/
│   ├── ingestion_agent.py
│   ├── classifier_agent.py
│   ├── decision_agent.py
│   ├── human_agent.py
│   ├── reply_agent.py
│   ├── action_agent.py
│   ├── voice_of_the_doctor.py
│   ├── voice_of_the_patient.py
│
├── integrations/
│   ├── email_reader.py
│   ├── email_sender.py
│   ├── slack.py
│
├── workflow/
│   └── langgraph_flow.py
│
├── auth/
│   └── auth_server.py
│
├── dashboard.py
├── main.py
└── logs.json
```

---

## ⚙️ Setup Instructions

### 🔹 1. Clone Repo

```bash
git clone <your-repo-url>
cd ops-pilot-ai-agent
```

---

### 🔹 2. Create `.env`

```
EMAIL_ID=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
GROQ_API_KEY=your_groq_key
AUTH0_DOMAIN=your_domain
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_secret
ELEVENLABS_API_KEY=your_key
```

---

### 🔹 3. Run Locally

```bash
python backend/dashboard.py
```

Open:

```
http://localhost:7860
```

---

## 🐳 Docker Setup

### 🔹 Build Image

```bash
docker build -t opspilot .
```

---

### 🔹 Run Container

```bash
docker run -p 5000:5000 -p 7860:7860 --env-file .env opspilot
```

---

## 🔐 Auth0 Configuration

| Setting      | Value                          |
| ------------ | ------------------------------ |
| Callback URL | http://localhost:5000/callback |
| Logout URL   | http://localhost:7860          |
| Web Origin   | http://localhost:7860          |

---

## 🎮 How It Works (Demo Flow)

1. Click **Login with Auth0**
2. Fetch email
3. AI analyzes and classifies
4. Decision:

   * Auto reply OR
   * Human approval
5. Add instructions (text or voice)
6. Approve
7. Email is sent automatically

---

## 🧠 AI Capabilities

* Context-aware replies
* Structured extraction (time, person, intent)
* Prompt-controlled (no hallucination)
* Multi-modal interaction (voice + text)

---

## 🚀 Future Enhancements

* WhatsApp integration
* Multi-user support (DB)
* Role-based access
* Cloud deployment (DigitalOcean/AWS)
* Advanced analytics dashboard

---

## 🏆 Why This Project Stands Out

✅ Real-world automation use case
✅ Human + AI collaboration
✅ Voice-enabled workflow
✅ Secure authentication
✅ End-to-end pipeline

---

## 👨‍💻 Author

**Vivekananda Sahoo**

---

## 📜 License

MIT License
