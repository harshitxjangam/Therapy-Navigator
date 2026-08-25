"""TherapyNavigator — AI operations tools for pediatric therapy organizations.

Entry point. Owns page config, shared chrome, and the sidebar navigation; the
four tools live in pages/ and are wired up through st.navigation below.
"""

import streamlit as st

from utils.claude_client import api_key_configured
from utils.ui import page_chrome, sidebar_footer

st.set_page_config(
    page_title="TherapyNavigator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

page_chrome()

TOOLS = [
    (
        "🧒",
        "Family Intake AI",
        "Recommend the right therapy for a child and generate a personalized "
        "family welcome email — in seconds.",
        "/Family_Intake",
    ),
    (
        "📬",
        "Waitlist Communication Engine",
        "Auto-generate warm, personalized status update emails for every "
        "family on your waitlist.",
        "/Waitlist_Comms",
    ),
    (
        "💬",
        "Staff Knowledge Assistant",
        "Instantly answer staff questions about therapy types, insurance, "
        "billing, and operations.",
        "/Staff_Assistant",
    ),
    (
        "📊",
        "Operations Report Generator",
        "Paste raw clinic numbers and get a formatted weekly operations "
        "summary with trends and action items.",
        "/Operations_Report",
    ),
]

JOURNEY = """
<a class="journey-link" href="{path}" target="_self">
<div class="journey-step journey-{number}">
    <div class="journey-index">0{number}</div>
    <div class="journey-icon">{icon}</div>
    <div class="journey-copy"><span>AI WORKSPACE</span><h3>{title}</h3><p>{body}</p></div>
    <div class="journey-action">Explore <b>→</b></div>
</div>
</a>
"""

VALUES = [
    (
        "Saves 10+ hours/week",
        "Automates the most repetitive admin tasks — intake summaries, "
        "waitlist follow-ups, and weekly reporting.",
    ),
    (
        "Family-first design",
        "Every tool puts the family experience first, with warm, jargon-free "
        "language that anxious parents can actually understand.",
    ),
    (
        "Built to scale",
        "Designed for multi-clinic organizations, so adding a location does "
        "not mean adding another coordinator.",
    ),
]


def home():
    """Landing page: hero, tool cards, value props."""
    st.markdown(
        """
        <div class="hero hero-home immersive-hero">
            <div class="hero-grid"></div>
            <div class="hero-copy">
                <div class="hero-chip"><i></i> THE THERAPYNAVIGATOR SYSTEM</div>
                <h1>Care, in<br><em>motion.</em></h1>
                <p>One considered workspace for the many small moments that
                make a pediatric therapy clinic feel extraordinary.</p>
                <div class="hero-note"><b>✦</b> Designed to make the everyday feel lighter</div>
            </div>
            <div class="hero-visual" aria-hidden="true">
                <div class="orbital-shadow"></div>
                <div class="care-orb"><div class="orb-glow"></div><div class="orb-mark">✦</div></div>
                <div class="orbit orbit-a"></div><div class="orbit orbit-b"></div>
                <div class="floating-note note-intake"><i>↗</i><b>Family intake</b><small>Thoughtful from hello</small></div>
                <div class="floating-note note-team"><i>✦</i><b>Team clarity</b><small>Answers in the moment</small></div>
                <div class="floating-note note-growth"><i>⌁</i><b>Care continues</b><small>Every follow-up counts</small></div>
                <div class="orbital-dot dot-a"></div><div class="orbital-dot dot-b"></div>
                <div class="tiny-caption">CARE, CONNECTED</div>
            </div>
        </div>
        <div class="hero-footer">
            <span>FAMILY-FIRST OPERATIONS</span><i></i><span>WARMER COMMUNICATION</span><i></i><span>SMARTER WORKFLOWS</span>
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

    st.markdown(
        """<div class="journey-intro"><div class="eyebrow">THE CARE JOURNEY</div>
        <h2>Built around the rhythm<br>of a real clinic.</h2><p>Each workspace
        removes a little friction from the path between a family’s first question
        and their next confident step.</p></div>""",
        unsafe_allow_html=True,
    )

    for number, (icon, title, body, path) in enumerate(TOOLS, start=1):
        st.markdown(
            JOURNEY.format(
                number=number, icon=icon, title=title, body=body, path=path
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        """<div class="statement-band"><div class="statement-orb">✦</div>
        <div><span>THE DIFFERENCE IS IN THE DETAILS</span><h2>More time with the
        people who matter. Less time lost to everything else.</h2></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="home-disclaimer">TherapyNavigator supports your team—it does not '
        'diagnose, store patient data, or replace clinical judgment.</div>',
        unsafe_allow_html=True,
    )


navigation = st.navigation(
    [
        st.Page(home, title="Home", icon="🏠", default=True),
        st.Page("views/1_Family_Intake.py", title="Family Intake", icon="🧒"),
        st.Page("views/2_Waitlist_Comms.py", title="Waitlist Comms", icon="📬"),
        st.Page("views/3_Staff_Assistant.py", title="Staff Assistant", icon="💬"),
        st.Page("views/4_Operations_Report.py", title="Operations Report", icon="📊"),
    ]
)

navigation.run()

sidebar_footer()
