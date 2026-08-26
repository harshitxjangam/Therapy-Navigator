"""Waitlist Communication Engine — batch personalized emails for waiting families."""

import streamlit as st

from utils.claude_client import call_claude, error_body, is_error
from utils.ui import api_key_banner, how_it_works, page_header

MAX_FAMILIES = 10

EMAIL_TYPES = [
    "General status update (we haven't forgotten you)",
    "Appointment coming soon (within 4 weeks)",
    "Insurance authorization needed",
    "Intake paperwork reminder",
    "Spot available — please respond within 48 hours",
]

TONES = [
    "Warm and reassuring",
    "Professional and clear",
    "Urgent (action required)",
]

THERAPY_TYPES = ["Speech", "OT", "PT", "ABA", "Not yet determined"]

SYSTEM_TEMPLATE = """You are a compassionate patient communications coordinator at a pediatric therapy clinic called {clinic}. Write a single email to a family whose child {child} has been waiting {weeks} weeks for {therapy} therapy.

Email type: {email_type}
Tone: {tone}
Parent name: {parent}

Write only the email — no preamble, no explanation. Include:
- Subject line on the first line starting with 'Subject:'
- One blank line
- Email body starting with a warm greeting
- The body should be 3-4 short paragraphs
- A warm, professional sign-off from the {clinic} Team

The email must feel personal, not like a template. Reference the specific therapy type and waiting time naturally. Do not use jargon. Keep it under 200 words.

Do not invent details you were not given — no phone numbers, email addresses, staff names, or specific dates, and no bracketed placeholders such as [Clinic Phone Number] for the sender to fill in. End with the sign-off and the clinic name, nothing after it."""

SAMPLE_FAMILIES = [
    {"child": "Emma", "parent": "Sarah Chen", "weeks": 6, "therapy": "Speech"},
    {"child": "Marcus", "parent": "Danielle Reed", "weeks": 12, "therapy": "OT"},
    {"child": "Aisha", "parent": "", "weeks": 3, "therapy": "PT"},
    {"child": "Liam", "parent": "Jordan Alvarez", "weeks": 18, "therapy": "ABA"},
]


def blank_family():
    return {"child": "", "parent": "", "weeks": 4, "therapy": "Speech"}


def sync_row_widgets(families):
    """Write the family list into the positional row widget keys.

    Only ever called from a button callback, which Streamlit runs before the
    row widgets are created — writing a widget key after its widget exists
    raises StreamlitAPIException.
    """
    for index, family in enumerate(families):
        st.session_state["wl_child_{}".format(index)] = family["child"]
        st.session_state["wl_parent_{}".format(index)] = family["parent"]
        st.session_state["wl_weeks_{}".format(index)] = int(family["weeks"])
        st.session_state["wl_therapy_{}".format(index)] = family["therapy"]


def read_rows():
    """Rebuild the family list from the widget keys.

    The widgets hold the freshest values — including an edit the user made just
    before clicking — so structural changes read from them rather than from the
    stored list, which lags by one render.
    """
    rows = []
    for index in range(len(st.session_state.waitlist_families)):
        rows.append(
            {
                "child": st.session_state.get("wl_child_{}".format(index), ""),
                "parent": st.session_state.get("wl_parent_{}".format(index), ""),
                "weeks": st.session_state.get("wl_weeks_{}".format(index), 4),
                "therapy": st.session_state.get(
                    "wl_therapy_{}".format(index), THERAPY_TYPES[0]
                ),
            }
        )
    return rows


def clear_email_widgets():
    for key in list(st.session_state.keys()):
        if key.startswith("wl_email_"):
            del st.session_state[key]


def set_families(families):
    st.session_state.waitlist_families = families
    sync_row_widgets(families)


# --- button callbacks: these run before any widget is instantiated ---------- #


def load_sample():
    st.session_state.waitlist_emails = []
    clear_email_widgets()
    set_families([dict(f) for f in SAMPLE_FAMILIES])


def clear_list():
    st.session_state.waitlist_emails = []
    clear_email_widgets()
    set_families([blank_family() for _ in range(3)])


def add_family():
    rows = read_rows()
    if len(rows) < MAX_FAMILIES:
        rows.append(blank_family())
        set_families(rows)


def remove_family(index):
    rows = read_rows()
    if len(rows) > 1 and 0 <= index < len(rows):
        rows.pop(index)
        set_families(rows)


# --------------------------------------------------------------------------- #
# State — must settle before any widget is created
# --------------------------------------------------------------------------- #
if "waitlist_families" not in st.session_state:
    st.session_state.waitlist_families = [blank_family() for _ in range(3)]
    sync_row_widgets(st.session_state.waitlist_families)
if "waitlist_emails" not in st.session_state:
    st.session_state.waitlist_emails = []

# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #
page_header(
    "Nobody waits in <em>silence</em>.",
    "Enter the families who are waiting. Every one gets their own email \u2014 "
    "their child's name, their therapy, their actual wait \u2014 written to be "
    "read, not filed.",
    eyebrow="Tool 02 \u00b7 Waitlist",
)

how_it_works(
    "Waitlisted families go quiet because nobody has time to write to them "
    "individually. Enter your list, pick the message type and tone, and the "
    "AI writes a distinct email for each family — referencing their child's "
    "name, their therapy type, and how long they've actually been waiting. "
    "Every draft is editable before you send it."
)
api_key_banner()

# --------------------------------------------------------------------------- #
# Settings
# --------------------------------------------------------------------------- #
setting_a, setting_b, setting_c = st.columns(3, gap="medium")
with setting_a:
    email_type = st.selectbox("Email type", EMAIL_TYPES)
with setting_b:
    clinic_name = st.text_input("Your clinic name", value="Oaklin Lane")
with setting_c:
    tone = st.selectbox("Tone", TONES)

st.divider()

# --------------------------------------------------------------------------- #
# Family list
# --------------------------------------------------------------------------- #
st.subheader("Add families to your list")
st.info(
    "Enter each family below. You can add up to {} at once. Only the child's "
    "first name and wait time are required.".format(MAX_FAMILIES)
)

sample_col, clear_col = st.columns(2)
with sample_col:
    st.button("Load sample data", use_container_width=True, on_click=load_sample)
with clear_col:
    st.button("Clear list", use_container_width=True, on_click=clear_list)

families = st.session_state.waitlist_families

header = st.columns([3, 3, 2, 3, 1])
for col, label in zip(header, ["Child", "Parent", "Weeks waiting", "Therapy", ""]):
    col.caption(label)

for index, family in enumerate(families):
    name_col, parent_col, weeks_col, therapy_col, remove_col = st.columns(
        [3, 3, 2, 3, 1]
    )
    family["child"] = name_col.text_input(
        "Child",
        placeholder="Child's name",
        key="wl_child_{}".format(index),
        label_visibility="collapsed",
    )
    family["parent"] = parent_col.text_input(
        "Parent",
        placeholder="Parent name (optional)",
        key="wl_parent_{}".format(index),
        label_visibility="collapsed",
    )
    family["weeks"] = weeks_col.number_input(
        "Weeks",
        min_value=1,
        max_value=52,
        step=1,
        key="wl_weeks_{}".format(index),
        label_visibility="collapsed",
    )
    family["therapy"] = therapy_col.selectbox(
        "Therapy",
        THERAPY_TYPES,
        key="wl_therapy_{}".format(index),
        label_visibility="collapsed",
    )
    remove_col.button(
        "✕",
        key="wl_remove_{}".format(index),
        help="Remove this family",
        disabled=len(families) <= 1,
        on_click=remove_family,
        args=(index,),
    )

add_col, count_col = st.columns([2, 3])
with add_col:
    st.button(
        "+ Add another family",
        use_container_width=True,
        disabled=len(families) >= MAX_FAMILIES,
        on_click=add_family,
    )
with count_col:
    st.caption("{} of {} slots used".format(len(families), MAX_FAMILIES))

st.write("")
generate = st.button(
    "Generate all emails →", type="primary", use_container_width=True
)

# --------------------------------------------------------------------------- #
# Generation
# --------------------------------------------------------------------------- #
if generate:
    valid = [f for f in families if f["child"].strip()]
    if not valid:
        st.error("Add at least one family with a child's first name.")
    else:
        clear_email_widgets()
        progress = st.progress(0.0, text="Starting…")
        results = []
        for position, family in enumerate(valid):
            progress.progress(
                position / len(valid),
                text="Writing email for {} ({} of {})…".format(
                    family["child"], position + 1, len(valid)
                ),
            )
            system_prompt = SYSTEM_TEMPLATE.format(
                clinic=clinic_name.strip() or "our clinic",
                child=family["child"].strip(),
                weeks=int(family["weeks"]),
                therapy=family["therapy"],
                email_type=email_type,
                tone=tone,
                parent=family["parent"].strip() or "Family",
            )
            results.append(
                {
                    "child": family["child"].strip(),
                    "therapy": family["therapy"],
                    "weeks": int(family["weeks"]),
                    "email": call_claude(
                        system_prompt, "Write the email now.", max_tokens=700
                    ),
                }
            )
        progress.empty()
        st.session_state.waitlist_emails = results

# --------------------------------------------------------------------------- #
# Results
# --------------------------------------------------------------------------- #
emails = st.session_state.waitlist_emails
if emails:
    st.divider()
    failures = sum(1 for item in emails if is_error(item["email"]))
    succeeded = len(emails) - failures

    st.subheader("Generated emails")
    if failures:
        st.warning(
            "{} of {} emails generated. {} failed — use **Generate all "
            "emails** to retry.".format(succeeded, len(emails), failures)
        )
    else:
        st.success("{} emails ready to review and send.".format(succeeded))

    for index, item in enumerate(emails):
        title = "{} — {} therapy ({} weeks waiting)".format(
            item["child"], item["therapy"], item["weeks"]
        )
        with st.expander(title, expanded=index == 0):
            if is_error(item["email"]):
                st.error(error_body(item["email"]))
                continue

            edited = st.text_area(
                "Email draft",
                value=item["email"],
                height=200,
                key="wl_email_{}".format(index),
                label_visibility="collapsed",
            )
            st.caption("{} words".format(len(edited.split())))
            st.download_button(
                "Download this email (.txt)",
                data=edited,
                file_name="waitlist_{}.txt".format(
                    item["child"].lower().replace(" ", "_")
                ),
                mime="text/plain",
                key="wl_dl_{}".format(index),
            )

    good = [
        (index, item)
        for index, item in enumerate(emails)
        if not is_error(item["email"])
    ]
    if good:
        separator = "\n\n" + "=" * 70 + "\n\n"
        bundle = separator.join(
            "TO: {} family — {} therapy ({} weeks waiting)\n\n{}".format(
                item["child"],
                item["therapy"],
                item["weeks"],
                st.session_state.get("wl_email_{}".format(index), item["email"]),
            )
            for index, item in good
        )
        st.download_button(
            "Download all {} emails (.txt)".format(len(good)),
            data=bundle,
            file_name="waitlist_emails_all.txt",
            mime="text/plain",
            type="primary",
            use_container_width=True,
        )
