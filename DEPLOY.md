# Deploying TherapyNavigator

Deployment target: **Streamlit Community Cloud** (free tier).
Total time: about five minutes, of which two to three are the build itself.

---

## Before you start

Confirm your secrets are not about to be committed:

```bash
git status --porcelain | grep -E "^\?\?.*\.env$" && echo "STOP: .env is untracked but visible — check .gitignore" || echo "OK: .env is ignored"
```

`.gitignore` already lists `.env`, `.streamlit/secrets.toml`, and `venv/`. Never
commit an API key — Streamlit Cloud has its own secrets store, covered in step 5.

---

## 1. Create the GitHub repository

Create a new **public** repository named `Therapy-Navigator` at
[github.com/new](https://github.com/new). Do not initialize it with a README,
`.gitignore`, or license — this project already has them.

> Streamlit Community Cloud can deploy private repos too, but public is simpler
> for a portfolio project people will look at.

## 2. Push the code

From the project root:

```bash
git init -b main
```

```bash
git add .
```

Check that no secret slipped in before you commit:

```bash
git status --short | grep -E "\.env$|secrets\.toml$" && echo "STOP — unstage this file" || echo "Clean — safe to commit"
```

```bash
git commit -m "TherapyNavigator: AI operations tools for pediatric therapy"
```

```bash
git remote add origin https://github.com/harshitxjangam/Therapy-Navigator.git
```

```bash
git push -u origin main
```

## 3. Connect Streamlit Cloud

Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
Authorize Streamlit to read your repositories when prompted.

## 4. Create the app

Click **New app**, then:

| Field | Value |
|---|---|
| Repository | `harshitxjangam/Therapy-Navigator` |
| Branch | `main` |
| Main file path | `app.py` |
| App URL | pick your subdomain (e.g. `therapy-navigator`) |

## 5. Add your API key

Still in the create-app dialog, open **Advanced settings → Secrets** and paste:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

TOML format, with the quotes. The app reads `st.secrets["ANTHROPIC_API_KEY"]`
first and falls back to a local `.env` file, so this is the only configuration
Streamlit Cloud needs.

While you are here, confirm **Python version** is 3.11 or newer under Advanced
settings.

## 6. Deploy

Click **Deploy**. The build installs `requirements.txt` and boots the app; the
log streams live. Your app lands at:

```
https://<your-subdomain>.streamlit.app
```

## 7. Verify the deployment

Walk each tool once:

1. **Home** — no yellow "Setup needed" banner. If you see one, the secret is
   missing or misnamed.
2. **Family Intake** — *Load sample data* → *Find the right therapy*. You should
   get a recommendation, a seven-item checklist, and a welcome email.
3. **Waitlist Comms** — *Load sample data* → *Generate all emails*. Four emails,
   each naming its child.
4. **Staff Assistant** — click a quick topic, then ask a follow-up to confirm it
   holds context.
5. **Operations Report** — *Try with sample data* → *Generate report*.

---

## Updating the app

Streamlit Cloud redeploys automatically on every push to `main`:

```bash
git add . && git commit -m "Your change" && git push
```

## Rotating or changing the key

In the Streamlit Cloud dashboard: **⋮ → Settings → Secrets**, edit the value, and
save. The app reboots on its own. Rotate the key at
[console.anthropic.com](https://console.anthropic.com/) if it was ever pasted
somewhere public.

---

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Yellow "Setup needed" banner | The secret is missing or misspelled. It must be exactly `ANTHROPIC_API_KEY` in **Settings → Secrets**. |
| "No Anthropic API key found" on generate | Same as above — the app degrades gracefully instead of crashing. |
| `ModuleNotFoundError` in the build log | A package is missing from `requirements.txt`. Add it, commit, push. |
| "The AI service is busy right now" | Rate limited upstream. Wait a few seconds and retry. |
| "The AI service returned an error (status 401)" | The key is invalid or revoked. Issue a new one and update the secret. |
| App sleeps after inactivity | Expected on the free tier. The first visit wakes it in ~30 seconds. |
| Build fails on Python version | Set Python 3.11+ under Advanced settings. |

## Cost

Each tool action is one Claude API call (the waitlist page makes one call per
family). Usage is billed to your Anthropic account, not to Streamlit. Set a
monthly spend limit under **Billing** at
[console.anthropic.com](https://console.anthropic.com/) before sharing the link
widely.
