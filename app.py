"""TherapyNavigator API.

FastAPI backend for the four tools. Vercel's Python preset detects the
top-level `app` and runs it as a serverless function; the static design in
public/ is served alongside it.
"""

import os
from datetime import date

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from api_lib import prompts
from api_lib.claude_client import (
    ClaudeError,
    api_key_configured,
    call_claude,
    call_claude_messages,
)
from api_lib.parsing import bullets, has_secondary, numbered_items, parse_sections

app = FastAPI(title="TherapyNavigator API", docs_url="/api/docs")


def fail(message, status=502):
    return JSONResponse({"error": message}, status_code=status)


@app.get("/api/health")
def health():
    """Cheap readiness probe — also tells the UI whether a key is configured."""
    return {"ok": True, "key_configured": api_key_configured()}


# --------------------------------------------------------------------------- #
# 1. Family intake
# --------------------------------------------------------------------------- #
class IntakeRequest(BaseModel):
    child_name: str = ""
    age_range: str = "4–6 years"
    concerns: list = []
    description: str = ""
    clinic: str = "Our Clinic"


@app.post("/api/intake")
def intake(req: IntakeRequest):
    if not req.concerns and not req.description.strip():
        return fail(
            "Select at least one area of concern, or describe the challenges.",
            status=400,
        )

    clinic = req.clinic.strip() or "Our Clinic"
    user_message = (
        "Child's first name: {}\n"
        "Age range: {}\n"
        "Areas of concern: {}\n"
        "Clinic name: {}\n\n"
        "What the family described:\n{}"
    ).format(
        req.child_name.strip() or "Not provided",
        req.age_range,
        ", ".join(req.concerns) if req.concerns else "Not specified",
        clinic,
        req.description.strip() or "No additional description provided.",
    )

    try:
        raw = call_claude(
            prompts.INTAKE_SYSTEM.replace("[CLINIC_NAME]", clinic),
            user_message,
            max_tokens=2000,
        )
    except ClaudeError as exc:
        return fail(str(exc))

    parsed = parse_sections(raw)
    secondary = parsed.get("SECONDARY_THERAPY", "")
    return {
        "primary": parsed.get("PRIMARY_THERAPY", ""),
        "secondary": secondary if has_secondary(secondary) else "",
        "explanation": parsed.get("EXPLANATION", ""),
        "involves": bullets(parsed.get("WHAT_IT_INVOLVES", "")),
        "first_appointment": parsed.get("FIRST_APPOINTMENT", ""),
        "checklist": numbered_items(parsed.get("CHECKLIST", "")),
        "email": parsed.get("WELCOME_EMAIL", "").strip(),
        # Preserve the original answer as a display fallback when a model uses
        # an unexpected label format.
        "raw": raw.strip(),
    }


# --------------------------------------------------------------------------- #
# 2. Waitlist communications
# --------------------------------------------------------------------------- #
class Family(BaseModel):
    child: str
    parent: str = ""
    weeks: int = 4
    therapy: str = "Speech"


class WaitlistRequest(BaseModel):
    families: list
    email_type: str = "General status update (we haven't forgotten you)"
    tone: str = "Warm and reassuring"
    clinic: str = "Oaklin Lane"


@app.post("/api/waitlist")
def waitlist(req: WaitlistRequest):
    valid = [f for f in req.families if str(f.get("child", "")).strip()]
    if not valid:
        return fail("Add at least one family with a child's first name.", 400)
    if len(valid) > 10:
        return fail("Up to 10 families per batch.", 400)

    emails = []
    for family in valid:
        system_prompt = prompts.WAITLIST_TEMPLATE.format(
            clinic=req.clinic.strip() or "our clinic",
            child=str(family.get("child", "")).strip(),
            weeks=int(family.get("weeks", 4)),
            therapy=family.get("therapy", "Speech"),
            email_type=req.email_type,
            tone=req.tone,
            parent=str(family.get("parent", "")).strip() or "Family",
        )
        try:
            body = call_claude(
                system_prompt, "Write the email now.", max_tokens=700
            )
            error = ""
        except ClaudeError as exc:
            body, error = "", str(exc)

        emails.append(
            {
                "child": str(family.get("child", "")).strip(),
                "therapy": family.get("therapy", "Speech"),
                "weeks": int(family.get("weeks", 4)),
                "email": body,
                "error": error,
                "words": len(body.split()),
            }
        )

    return {"emails": emails}


# --------------------------------------------------------------------------- #
# 3. Staff assistant
# --------------------------------------------------------------------------- #
class AskRequest(BaseModel):
    messages: list


@app.post("/api/ask")
def ask(req: AskRequest):
    history = [
        {"role": m.get("role", "user"), "content": str(m.get("content", ""))}
        for m in req.messages
        if str(m.get("content", "")).strip()
    ]
    if not history:
        return fail("Ask a question first.", 400)

    try:
        answer = call_claude_messages(
            prompts.ASSISTANT_SYSTEM, history, max_tokens=1200
        )
    except ClaudeError as exc:
        return fail(str(exc))

    return {"answer": answer}


# --------------------------------------------------------------------------- #
# 4. Operations report
# --------------------------------------------------------------------------- #
class ReportRequest(BaseModel):
    clinic: str = "Oaklin Lane"
    period: str = ""
    completed: int = 0
    canceled: int = 0
    evals: int = 0
    referrals: int = 0
    waitlist: int = 0
    auth_approved: int = 0
    auth_pending: int = 0
    auth_denied: int = 0
    therapists: int = 0
    utilization: int = 0
    notes: str = ""
    compare: bool = False
    prev_completed: int = 0
    prev_waitlist: int = 0
    prev_referrals: int = 0
    reframe: bool = False


@app.post("/api/report")
def report(req: ReportRequest):
    if req.completed == 0 and req.canceled == 0:
        return fail(
            "Enter at least the completed and canceled appointment counts.", 400
        )

    scheduled = req.completed + req.canceled
    lines = [
        "Clinic name: {}".format(req.clinic or "Our Clinic"),
        "Report period: {}".format(req.period or "This period"),
        "",
        "Total appointments completed: {}".format(req.completed),
        "Appointments canceled or no-show: {}".format(req.canceled),
        "Total appointments scheduled (completed + canceled): {}".format(scheduled),
        "New patient evaluations: {}".format(req.evals),
        "New referrals received: {}".format(req.referrals),
        "Current waitlist size: {}".format(req.waitlist),
        "Insurance authorizations approved: {}".format(req.auth_approved),
        "Insurance authorizations pending: {}".format(req.auth_pending),
        "Insurance authorizations denied: {}".format(req.auth_denied),
        "Active therapists this period: {}".format(req.therapists),
        "Available therapy hours used: {}%".format(req.utilization),
    ]
    if req.compare:
        lines += [
            "",
            "PRIOR PERIOD COMPARISON:",
            "Previous appointments completed: {}".format(req.prev_completed),
            "Previous waitlist size: {}".format(req.prev_waitlist),
            "Previous new referrals: {}".format(req.prev_referrals),
        ]
    lines += [
        "",
        "Notes, highlights or concerns from the team:",
        req.notes.strip() or "None provided.",
        "",
        "Today's date: {}".format(date.today().strftime("%B %d, %Y")),
    ]
    payload = "\n".join(lines)

    system = prompts.REPORT_SYSTEM + (
        prompts.REPORT_REFRAME if req.reframe else ""
    )
    try:
        markdown = call_claude(system, payload, max_tokens=2500)
    except ClaudeError as exc:
        return fail(str(exc))

    cancel_rate = (100 * req.canceled / scheduled) if scheduled else 0
    decided = req.auth_approved + req.auth_denied
    return {
        "report": markdown,
        "payload": payload,
        "metrics": {
            "scheduled": scheduled,
            "completion_rate": round(100 * req.completed / scheduled, 1)
            if scheduled
            else 0,
            "cancel_rate": round(cancel_rate, 1),
            "denial_rate": round(100 * req.auth_denied / decided, 1)
            if decided
            else 0,
        },
    }


# --------------------------------------------------------------------------- #
# Static design canvas
#
# Mounted last so every /api route above wins first. Vercel's FastAPI preset
# routes all traffic to this app, so serving the frontend here is what makes
# "/" work — relying on platform-level static handling would 404.
# --------------------------------------------------------------------------- #
# On Vercel, public/ is uploaded as CDN static assets and excluded from the
# function bundle, so the directory does not exist at runtime — mounting it
# unconditionally raises during import and fails every request, including
# /api/*. The platform already serves those files, so mount only when the
# directory is actually present (local development).
_PUBLIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
if os.path.isdir(_PUBLIC):
    app.mount("/", StaticFiles(directory=_PUBLIC, html=True), name="static")
