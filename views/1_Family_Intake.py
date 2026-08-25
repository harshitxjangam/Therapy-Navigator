"""Family Intake AI — therapy recommendation, prep checklist, welcome email."""

import streamlit as st

from utils.claude_client import call_claude, error_body, is_error
from utils.parsing import bullets, has_secondary, numbered_items, parse_sections
from utils.ui import api_key_banner, how_it_works, page_header


AGE_RANGES = [
    "Under 2 years",
    "2–4 years",
    "4–6 years",
    "6–10 years",
    "10–14 years",
    "14–18 years",
]

CONCERNS = [
    "Speech and language delays",
    "Difficulty understanding others",
    "Fine motor skills (writing, buttons, zippers)",
    "Gross motor skills (walking, balance, coordination)",
    "Sensory sensitivities (sounds, textures, lights)",
    "Social interaction and play",
    "Behavioral challenges and emotional regulation",
    "Feeding or swallowing difficulties",
    "Attention and focus",
    "Developmental delays (general)",
]

SYSTEM_PROMPT = """You are an intake specialist at a pediatric therapy clinic. You help families understand which therapy would benefit their child. You communicate in warm, clear, jargon-free language that anxious parents can understand. You never diagnose — you recommend therapy types and explain what they involve.

The therapy types you work with are:
- Speech-Language Therapy (SLT): for speech, language, communication, feeding/swallowing
- Occupational Therapy (OT): for fine motor skills, sensory processing, self-care, handwriting, feeding
- Physical Therapy (PT): for gross motor skills, balance, coordination, strength, mobility
- Applied Behavior Analysis (ABA): for behavioral challenges, social skills, routines, communication in children with autism or developmental differences

Always respond using these exact section labels, each on its own line:

PRIMARY_THERAPY: [therapy name]
SECONDARY_THERAPY: [therapy name, or "None" if not relevant]
EXPLANATION: 2-3 sentences in simple, warm language explaining why this therapy fits the child's needs
WHAT_IT_INVOLVES:
- [3-4 bullet points on what sessions look like]
FIRST_APPOINTMENT: 1-2 sentences on what to expect
CHECKLIST:
1. [7 specific preparation items as a numbered list]
WELCOME_EMAIL:
[A complete, professional email from the clinic to the family. Sign it as [CLINIC_NAME] Team.]

Use the child's name if provided. Be specific to the age and challenges described. Be warm and reassuring — many families are overwhelmed."""

SAMPLE = {
    "child_name": "Emma",
    "age": "4–6 years",
    "concerns": [
        "Speech and language delays",
        "Fine motor skills (writing, buttons, zippers)",
        "Sensory sensitivities (sounds, textures, lights)",
    ],
    "description": (
        "Emma is 5 and started kindergarten this fall. Her teacher mentioned "
        "that other kids have trouble understanding her — she drops the ends "
        "of words and gets frustrated when she has to repeat herself. She also "
        "struggles to hold a pencil and can't manage the buttons on her coat. "
        "Loud places like the cafeteria really overwhelm her and she covers "
        "her ears."
    ),
    "clinic": "Oaklin Lane - Austin",
}

# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #
page_header(
    "🧒 Family Intake AI",
    "Help families find the right therapy for their child",
)

how_it_works(
    "Describe a child's challenges in plain language. The AI matches those "
    "challenges to the therapy discipline best suited to them (Speech, OT, PT "
    "or ABA), explains the recommendation in parent-friendly terms, builds a "
    "checklist for the first visit, and drafts a welcome email your clinic can "
    "send. It never diagnoses — it recommends therapy types and sets "
    "expectations."
)
api_key_banner()

def load_sample():
    """Populate the form. Runs as a button callback, before the widgets exist."""
    for field, value in SAMPLE.items():
        st.session_state["intake_" + field] = value


if "intake_clinic" not in st.session_state:
    st.session_state.intake_clinic = "Our Clinic"
if "intake_run" not in st.session_state:
    st.session_state.intake_run = 0
if "intake_result" not in st.session_state:
    st.session_state.intake_result = None
if "intake_meta" not in st.session_state:
    st.session_state.intake_meta = {}

# --------------------------------------------------------------------------- #
# Layout
# --------------------------------------------------------------------------- #
left, right = st.columns(2, gap="large")

with left:
    st.subheader("Tell us about the child")

    st.button(
        "Load sample data", use_container_width=True, on_click=load_sample
    )

    child_name = st.text_input(
        "Child's first name (optional)",
        placeholder="e.g. Emma",
        key="intake_child_name",
    )
    age_range = st.selectbox(
        "Child's age range",
        AGE_RANGES,
        key="intake_age",
    )
    concerns = st.multiselect(
        "Primary areas of concern",
        CONCERNS,
        key="intake_concerns",
    )
    description = st.text_area(
        "Describe the challenges in your own words",
        placeholder=(
            "Tell us what you've been noticing. The more detail, the better "
            "we can help."
        ),
        height=150,
        key="intake_description",
    )
    clinic_name = st.text_input(
        "Clinic name (for the welcome email)",
        placeholder="e.g. Oaklin Lane - Austin",
        key="intake_clinic",
    )

    submitted = st.button(
        "Find the right therapy →",
        use_container_width=True,
        type="primary",
    )

if submitted:
    if not concerns and not description.strip():
        st.session_state.intake_result = None
        with right:
            st.error(
                "Please select at least one area of concern, or describe the "
                "challenges in your own words."
            )
    else:
        clinic = clinic_name.strip() or "Our Clinic"
        user_message = (
            "Child's first name: {}\n"
            "Age range: {}\n"
            "Areas of concern: {}\n"
            "Clinic name: {}\n\n"
            "What the family described:\n{}"
        ).format(
            child_name.strip() or "Not provided",
            age_range,
            ", ".join(concerns) if concerns else "Not specified",
            clinic,
            description.strip() or "No additional description provided.",
        )

        with right:
            with st.spinner("Analyzing your child's needs..."):
                response = call_claude(
                    SYSTEM_PROMPT.replace("[CLINIC_NAME]", clinic),
                    user_message,
                    max_tokens=2000,
                )

        if is_error(response):
            st.session_state.intake_result = None
            with right:
                st.error(error_body(response))
                st.caption("Try again — most issues clear up on a second attempt.")
        else:
            st.session_state.intake_result = parse_sections(response)
            st.session_state.intake_raw = response
            st.session_state.intake_meta = {
                "child": child_name.strip() or "your child",
                "clinic": clinic,
            }
            # New generation => new checkbox keys => everything starts unticked.
            st.session_state.intake_run += 1

with right:
    result = st.session_state.intake_result

    if result is None and not submitted:
        st.subheader("Your recommendation")
        st.info(
            "Fill in the form on the left and select **Find the right "
            "therapy** — results appear here."
        )

    elif result:
        st.subheader("Your recommendation")

        # ---- A. Therapy recommendation ---------------------------------- #
        with st.expander("✅ Therapy Recommendation", expanded=True):
            primary = result.get("PRIMARY_THERAPY", "").strip()
            secondary = result.get("SECONDARY_THERAPY", "").strip()

            badges = ""
            if primary:
                badges += '<span class="badge">{}</span>'.format(primary)
            if has_secondary(secondary):
                badges += '<span class="badge badge-secondary">Also helpful: {}</span>'.format(
                    secondary
                )
            if badges:
                st.markdown(badges, unsafe_allow_html=True)

            explanation = result.get("EXPLANATION", "")
            if explanation:
                st.write(explanation)

            involves = result.get("WHAT_IT_INVOLVES", "")
            if involves:
                st.markdown("**What this therapy involves**")
                for item in bullets(involves):
                    st.markdown("- " + item)

            first_appt = result.get("FIRST_APPOINTMENT", "")
            if first_appt:
                st.markdown("**At the first appointment**")
                st.info(first_appt)

        # ---- B. Preparation checklist ----------------------------------- #
        with st.expander("📋 Preparation Checklist", expanded=True):
            items = numbered_items(result.get("CHECKLIST", ""))
            if items:
                st.caption("Tick these off as you go — your progress is saved.")
                run = st.session_state.intake_run
                for index, item in enumerate(items):
                    st.checkbox(item, key="intake_check_{}_{}".format(run, index))
                done = sum(
                    1
                    for index in range(len(items))
                    if st.session_state.get(
                        "intake_check_{}_{}".format(run, index)
                    )
                )
                st.progress(done / len(items))
                st.caption("{} of {} complete".format(done, len(items)))
            else:
                st.write("No checklist was returned. Try generating again.")

        # ---- C. Welcome email ------------------------------------------- #
        with st.expander("📧 Draft Welcome Email", expanded=False):
            email = result.get("WELCOME_EMAIL", "").strip()
            if email:
                st.caption(
                    "Hover the box below and use the copy icon in its top-right "
                    "corner to copy the email."
                )
                st.code(email, language=None)
                st.download_button(
                    "Download email (.txt)",
                    data=email,
                    file_name="welcome_email_{}.txt".format(
                        st.session_state.intake_meta.get("child", "family")
                        .lower()
                        .replace(" ", "_")
                    ),
                    mime="text/plain",
                    use_container_width=True,
                )
            else:
                st.write("No email was returned. Try generating again.")

        with st.expander("View raw AI response"):
            st.text(st.session_state.get("intake_raw", ""))

