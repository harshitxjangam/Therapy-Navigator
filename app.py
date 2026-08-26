"""TherapyNavigator — AI operations tools for pediatric therapy organizations.

Entry point. Owns page config, shared chrome, and the top navigation; the four
tools live in views/ and are wired up through st.navigation below.
"""

from datetime import datetime, timedelta

import streamlit as st

from utils.claude_client import api_key_configured
from utils.ui import LOGO_PATH, page_chrome, render_html

st.set_page_config(
    page_title="TherapyNavigator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.logo(LOGO_PATH, size="medium")
page_chrome()

DAY_EVENTS = [
    ("1", "✚", "Emma · intake review", "Speech-Language"),
    ("2", "✎", "Marcus · OT session", "Room 3 · Rachel L."),
    ("3", "✉", "Waitlist batch send", "4 families · Warm"),
    ("4", "♥", "Aisha · PT eval", "New patient · 60m"),
    ("5", "◈", "Weekly report due", "Leadership recap"),
]

JOURNEY = [
    ("1", "✚", "Family Intake",
     "Match a child to the right therapy in plain, warm language. "
     "Then send a welcome email.", "PLAIN LANGUAGE"),
    ("2", "✉", "Waitlist Comms",
     "Personalized status emails for everyone waiting. Nobody goes silent.",
     "UP TO 10 AT ONCE"),
    ("3", "☾", "Staff Assistant",
     "A grounded chat over your clinic knowledge base. Evaluations, "
     "insurance, phrasing.", "GROUNDED"),
    ("4", "◈", "Weekly Report",
     "Raw clinic numbers become a leadership-ready summary with "
     "recommended actions.", "RATES CALCULATED"),
]

# Sample-week figures, the same ones the Report tool ships as demo data.
TICKER = [
    ("1", "+19", "NEW REFERRALS · SPEECH-HEAVY"),
    ("2", "284", "APPOINTMENTS COMPLETED"),
    ("3", "22", "AUTHS PENDING · 3 AGING"),
]

# The timeline track runs 8am to 6pm.
TRACK_START, TRACK_END = 8, 18


def day_calendar():
    """The canvas's 3D day widget, with today's date, clock and now-line live."""
    now = datetime.now()
    monday = now.date() - timedelta(days=now.weekday())

    days = ""
    for offset in range(7):
        day = monday + timedelta(days=offset)
        letter = "MTWTFSS"[offset]
        classes = ["cw-day"]
        marks = ""
        if day == now.date():
            classes.append("is-today")
            marks = '<span class="pulse-dot"></span>'
        elif offset >= 5:
            classes.append("dim")
        elif offset == 4:
            marks = '<span class="due-mark">◈</span>'
        days += (
            '<div class="{}"><span class="d">{}</span>'
            '<span class="n">{}</span>{}</div>'
        ).format(" ".join(classes), letter, day.day, marks)

    events = "".join(
        '<div class="ev ev-{}"><span class="ev-ico">{}</span>'
        "<b>{}</b><small>{}</small></div>".format(slot, icon, title, sub)
        for slot, icon, title, sub in DAY_EVENTS
    )

    # Position the now-line within the 8am–6pm track. Outside clinic hours it
    # clamps to the nearest edge rather than disappearing — the label carries
    # the true time, and the marker is part of what makes the widget read.
    hours = now.hour + now.minute / 60
    pct = (hours - TRACK_START) / (TRACK_END - TRACK_START) * 100
    pct = min(100.0, max(0.0, pct))
    now_line = (
        '<div class="now-line" style="top:{:.1f}%">'
        '<span class="now-lbl">NOW · {}</span></div>'
    ).format(pct, now.strftime("%-I:%M %p").lstrip("0"))

    return """
    <div class="hero-visual">
      <div class="cal">
        <div class="cal-layer-back"></div>
        <div class="cal-head">
          <div>
            <div class="cal-month">{month}</div>
            <div class="cal-today">{today}</div>
          </div>
          <div class="cal-clock">
            <div class="cc-time">{clock}</div>
            <div class="cc-meta">OAKLIN LANE · AUSTIN</div>
          </div>
        </div>
        <div class="cal-week">{days}</div>
        <div class="cal-body">
          <div class="cal-timeline">
            <div class="cal-hours">
              <span>8</span><span>10</span><span>12</span>
              <span>2</span><span>4</span><span>6</span>
            </div>
            <div class="cal-track">
              <div class="cal-grid"></div>
              {now_line}
              {events}
            </div>
          </div>
          <div class="cal-chart">
            <div class="cc-eyebrow">THIS WEEK</div>
            <div class="cc-num">284<em>↑ 2%</em></div>
            <div class="cc-lbl">appointments completed</div>
            <div class="cc-bars">
              <div class="cc-bar" style="height:55%"></div>
              <div class="cc-bar is-today" style="height:78%"></div>
              <div class="cc-bar" style="height:42%"></div>
              <div class="cc-bar" style="height:66%"></div>
              <div class="cc-bar" style="height:88%"></div>
            </div>
            <div class="cc-bar-lbls">
              <span>M</span><span class="on">T</span><span>W</span>
              <span>T</span><span>F</span>
            </div>
          </div>
        </div>
        <div class="cal-foot">
          <div class="cf-chip"><span class="dot" style="background:#D65A4A"></span>Intake</div>
          <div class="cf-chip"><span class="dot" style="background:#C0D77A"></span>Sessions</div>
          <div class="cf-chip"><span class="dot" style="background:#E5A5B0"></span>Comms</div>
          <div class="cf-chip"><span class="dot" style="background:#F0995E"></span>Report</div>
          <div class="cf-count">{count} events today</div>
        </div>
      </div>
    </div>
    """.format(
        month=now.strftime("%B %Y").upper(),
        today=now.strftime("%A %-d"),
        clock=now.strftime("%-I:%M"),
        days=days,
        now_line=now_line,
        events=events,
        count=len(DAY_EVENTS),
    )


def home():
    """Landing page: hero + 3D day calendar, care journey, week ticker."""
    render_html(
        """
        <div class="hero-grid">
          <div>
            <div class="hero-eyebrow"><span class="dot"></span>
              Four tools · one calm place</div>
            <h1 class="hero-h1">Care, in <em>motion.</em></h1>
            <p>Everything the clinic asks of you — intake, outreach, answers
            and reporting — in one considered workspace built for the small
            moments that make a pediatric therapy practice feel
            extraordinary.</p>
            <div class="hero-actions">
              <span class="btn-primary">Start a new intake
                <span class="arrow">→</span></span>
              <span class="btn-ghost">Open from the nav above</span>
            </div>
            <div class="hero-stats">
              <div class="s"><div class="n">4</div><div class="l">TOOLS</div></div>
              <div class="s"><div class="n">10</div><div class="l">FAMILIES PER BATCH</div></div>
              <div class="s"><div class="n">0</div><div class="l">PATIENT DATA STORED</div></div>
            </div>
          </div>
          """
        + day_calendar()
        + "</div>"
    )

    if not api_key_configured():
        st.warning(
            "**Setup needed:** no Anthropic API key detected. Add "
            "`ANTHROPIC_API_KEY` to your `.env` file locally, or to your app "
            "secrets on Streamlit Cloud. The interface works without it, but "
            "the AI tools will not generate results."
        )

    steps = "".join(
        '''<div class="step step-{n}">
             <div class="step-badge"><div class="glyph">{glyph}</div>
               <div class="num">{n}</div></div>
             <h3>{title}</h3>
             <p>{body}</p>
             <div class="step-cta"><span>{cta}</span>
               <span class="arr">→</span></div>
           </div>'''.format(n=n, glyph=glyph, title=title, body=body, cta=cta)
        for n, glyph, title, body, cta in JOURNEY
    )

    render_html(
        '''<div class="journey-wrap">
             <div class="journey-head">
               <div>
                 <div class="eyebrow">The care journey · today</div>
                 <h2>Pick up where you<br>left off.</h2>
               </div>
               <p>Each stop mirrors a real moment in a family's care. Start
               anywhere — open any tool from the navigation above.</p>
             </div>
             <div class="route">''' + steps + "</div></div>"
    )

    items = "".join(
        '''<div class="ticker-item i-{n}"><div class="n">{num}</div>
             <div class="l">{label}</div></div>'''.format(n=n, num=num, label=label)
        for n, num, label in TICKER
    )

    render_html(
        '''<div class="ticker">
             <div class="ticker-l">
               <div class="eyebrow">This week at Oaklin Lane</div>
               <h3>A steady week, but<br>the auth backlog is <em>aging</em>.</h3>
             </div>
             <div class="ticker-r">''' + items + "</div></div>"
    )

    st.write("")
    st.caption(
        "Figures shown are the sample dataset the Report tool ships with. "
        "TherapyNavigator is a demonstration project — it does not diagnose, "
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
