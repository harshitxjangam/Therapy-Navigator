"""TherapyNavigator — AI operations tools for pediatric therapy organizations.

Entry point. Owns page config, shared chrome, and the top navigation; the four
tools live in views/ and are wired up through st.navigation below.
"""

import streamlit as st

from utils.claude_client import api_key_configured
from utils.ui import LOGO_PATH, page_chrome

st.set_page_config(
    page_title="TherapyNavigator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.logo(LOGO_PATH, size="medium")
page_chrome()

TOOLS = [
    (
        "01",
        "✚",
        "Family Intake",
        "Describe what you're noticing. Get a therapy recommendation in plain "
        "language, a prep checklist, and a drafted welcome email.",
    ),
    (
        "02",
        "✉",
        "Waitlist Comms",
        "Nobody waits in silence. Personal status emails for every waiting "
        "family, written one at a time, ready to review and send.",
    ),
    (
        "03",
        "☾",
        "Staff Assistant",
        "Ask what your team asks. Grounded answers on therapy types, "
        "evaluations, insurance and authorization — in the moment.",
    ),
    (
        "04",
        "◈",
        "Weekly Report",
        "Raw clinic numbers become a leadership-ready summary, with rates "
        "calculated, outliers flagged, and actions named.",
    ),
]

CARD = """
<div class="card">
  <div class="card-top">
    <div class="card-icon">{icon}</div>
    <div class="card-num">TOOL {num}</div>
  </div>
  <div class="card-title">{title}</div>
  <div class="card-body">{body}</div>
  <div class="card-link">Open tool →</div>
</div>
"""

PRINCIPLES = [
    (
        "✦",
        "Saves 10+ hours a week",
        "The repetitive middle of the job — intake summaries, waitlist "
        "follow-ups, weekly reporting — handled in a few minutes.",
    ),
    (
        "♥",
        "Family-first language",
        "Warm and jargon-free by default, because most families meet these "
        "words on the hardest week of their year.",
    ),
    (
        "↯",
        "Built to scale",
        "Designed for multi-clinic organizations, so opening a location "
        "doesn't mean hiring another coordinator.",
    ),
]


def home():
    """Landing page: hero, tool cards, principles."""
    st.markdown(
        """
        <div class="hero">
          <div class="hero-eyebrow"><span class="dot"></span>
            Four tools · one calm place</div>
          <h1>Care, in <em>motion.</em></h1>
          <p>Everything the clinic asks of you — intake, outreach, answers and
          reporting — in one considered workspace built for the small moments
          that make a pediatric therapy practice feel extraordinary.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not api_key_configured():
        st.warning(
            "**Setup needed:** no Anthropic API key detected. Add "
            "`ANTHROPIC_API_KEY` to your `.env` file locally, or to your app "
            "secrets on Streamlit Cloud. The interface works without it, but "
            "the AI tools will not generate results."
        )

    st.markdown('<div class="eyebrow">The toolkit</div>', unsafe_allow_html=True)
    st.write("")

    for row_start in (0, 2):
        for col, (num, icon, title, body) in zip(
            st.columns(2, gap="medium"), TOOLS[row_start:row_start + 2]
        ):
            with col:
                st.markdown(
                    CARD.format(num=num, icon=icon, title=title, body=body),
                    unsafe_allow_html=True,
                )
        st.write("")

    st.caption("Open any tool from the navigation above.")
    st.write("")

    st.markdown(
        '<div class="eyebrow">Why TherapyNavigator</div>', unsafe_allow_html=True
    )
    st.write("")

    for col, (glyph, heading, body) in zip(st.columns(3, gap="medium"), PRINCIPLES):
        with col:
            st.markdown(
                '<div class="card"><div class="card-icon">{}</div>'
                '<div class="card-title">{}</div>'
                '<div class="card-body">{}</div></div>'.format(glyph, heading, body),
                unsafe_allow_html=True,
            )

    st.write("")
    st.write("")
    st.caption(
        "TherapyNavigator is a demonstration project. It does not diagnose, "
        "store patient data, or replace clinical judgment."
    )


navigation = st.navigation(
    [
        # The canvas uses typographic glyphs (✦ ✚ ✉ ☾ ◈); st.Page only accepts
        # emoji or Material icon names, so these are the closest equivalents.
        st.Page(home, title="Today", icon=":material/wb_sunny:", default=True),
        st.Page(
            "views/1_Family_Intake.py", title="Intake", icon=":material/add:"
        ),
        st.Page(
            "views/2_Waitlist_Comms.py", title="Waitlist", icon=":material/mail:"
        ),
        st.Page(
            "views/3_Staff_Assistant.py",
            title="Assistant",
            icon=":material/chat_bubble:",
        ),
        st.Page(
            "views/4_Operations_Report.py",
            title="Report",
            icon=":material/insights:",
        ),
    ],
    position="top",
)

navigation.run()
