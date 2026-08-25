# TherapyNavigator

**AI-powered operations tools for pediatric therapy organizations**

TherapyNavigator is a four-tool web application that takes on the administrative
work that grows fastest as a pediatric therapy practice scales: explaining
therapy options to anxious families, keeping waitlisted families informed,
answering the same staff questions over and over, and turning a week of raw
clinic numbers into something leadership can actually read. Each tool is built
around a real bottleneck in the referral-to-treatment pipeline, and each one
produces output a coordinator can review, edit, and send.

## What it does

- **🧒 Family Intake AI** — A parent or intake coordinator describes a child's
  challenges in plain language. The app recommends the appropriate therapy
  discipline (Speech, OT, PT, or ABA), explains the reasoning in warm,
  jargon-free terms, generates a preparation checklist for the first visit, and
  drafts a welcome email from the clinic. It recommends therapy types — it never
  diagnoses.
- **📬 Waitlist Communication Engine** — Enter up to ten waiting families, choose
  a message type and tone, and get a distinct, personal email for each one that
  references the child's name, therapy type, and actual wait time. Every draft is
  editable, and emails download individually or as a single batch file.
- **💬 Staff Knowledge Assistant** — A grounded chat assistant for clinic staff,
  answering questions about the four therapy disciplines, evaluations, prior
  authorization, billing terminology, and common parent questions. It answers
  from a built-in knowledge base, keeps conversational context, and declines to
  guess about specific coverage or clinical decisions.
- **📊 Operations Report Generator** — Paste in the week's raw numbers and get a
  leadership-ready summary: completion and cancellation rates, therapist
  utilization, referral and waitlist trends, authorization approval and denial
  rates, and concrete recommended actions. Derived metrics are calculated from
  the raw inputs, and out-of-range figures are flagged.

## Why I built this

Pediatric therapy organizations are bottlenecked less by clinical capacity than
by the administrative load that surrounds it — intake, communication, insurance
follow-up, and reporting. I built TherapyNavigator to demonstrate applying AI and
automation to those specific operational problems, rather than to a generic
chatbot use case. The goal was tools a growing multi-clinic organization could
actually put in front of staff: grounded, reviewable, and designed so that adding
a location doesn't mean adding another coordinator.

## Tech stack

- Python + Streamlit (multi-page app via `st.navigation`)
- Anthropic Claude API (`claude-sonnet-4-6`)
- Deployed on Streamlit Community Cloud

## Running locally

```bash
git clone https://github.com/harshitxjangam/Therapy-Navigator.git
cd Therapy-Navigator
```

```bash
python3 -m venv venv && source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root (copy `.env.example`) and add your key
from [console.anthropic.com](https://console.anthropic.com/):

```bash
cp .env.example .env
```

```
ANTHROPIC_API_KEY=sk-ant-...
```

Then start the app:

```bash
streamlit run app.py
```

It opens at `http://localhost:8501`. Every input page has a **Load sample data**
button, so you can try all four tools without typing anything real.

## Deploying to Streamlit Cloud

1. Push the repo to GitHub (confirm `.env` is **not** committed — it is listed in
   `.gitignore`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select the repo, the `main` branch, and `app.py` as the
   entry point.
4. Under **Advanced settings → Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
5. Click **Deploy**. It takes about two to three minutes.

Full instructions, including how to rotate the key later, are in
[DEPLOY.md](DEPLOY.md).

## Project structure

```
Therapy-Navigator/
├── app.py                      # entry point, navigation, home page
├── views/                      # the four tool pages
│   ├── 1_Family_Intake.py
│   ├── 2_Waitlist_Comms.py
│   ├── 3_Staff_Assistant.py
│   └── 4_Operations_Report.py
├── utils/
│   ├── claude_client.py        # shared Anthropic client + error handling
│   ├── parsing.py              # response parsing helpers
│   └── ui.py                   # shared CSS and page chrome
├── assets/logo.png
├── .streamlit/config.toml      # theme
└── requirements.txt
```

## Notes

- **Why `views/` and not `pages/`:** navigation is declared explicitly in
  `app.py` with `st.navigation`, which gives each tool a proper title and icon
  and labels the landing page "Home" rather than "app". Streamlit *also*
  auto-generates routes for any directory literally named `pages/`, and the two
  routers collide: the sidebar links work, but loading or refreshing a tool URL
  directly gets served by the auto-router, which skips `app.py` and therefore
  renders without the theme, logo, or navigation icons. Naming the directory
  `views/` leaves `st.navigation` as the single router, so shared and refreshed
  links render correctly.
- The API key is never hardcoded. It loads from `st.secrets` on Streamlit Cloud
  and falls back to a local `.env` file, and the app shows a setup banner instead
  of crashing when no key is present.
- No database and no authentication — all state lives in `st.session_state`, and
  nothing is persisted between sessions.
- This is a demonstration project. It does not diagnose, does not store patient
  data, and is not a substitute for clinical judgment.

---
*Built by Harshit Swami Jangam — MS AI student at SJSU*

[GitHub](https://github.com/harshitxjangam)
