"""Shared look-and-feel for TherapyNavigator.

Implements the "Therapy Navigator" Claude Design canvas: warm cream ground,
Instrument Serif display type, DM Sans body, JetBrains Mono eyebrows, and the
rainbow stripe. Streamlit runs each page as its own script, so the chrome is
applied once by app.py before the selected page runs.
"""

import os

import streamlit as st

from utils.claude_client import api_key_configured

LOGO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png"
)

# Palette from the design canvas.
CREAM = "#F9EFD4"
INK = "#3A2E1F"
FOREST = "#4A6D3F"
YELLOW = "#F5C63C"
RED = "#D65A4A"
PRIMARY = FOREST

RAINBOW = ["#F5C63C", "#F0995E", "#E5A5B0", "#C0D77A", "#4A6D3F", "#8CC0D6", "#9AA0C9"]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root{
  --cream:#F9EFD4; --cream-2:#FBF3DE; --ink:#3A2E1F; --ink-2:#4E3E2A;
  --paper:#FFFAEB; --yellow:#F5C63C; --orange:#F0995E; --pink:#E5A5B0;
  --green:#C0D77A; --forest:#4A6D3F; --blue:#8CC0D6; --teal:#5FA090;
  --purple:#9AA0C9; --red:#D65A4A;
  --line:rgba(58,46,31,.12);
}

/* ---------- ground ---------- */
.stApp { background: var(--cream); }
/* Body face is set once and inherited. Deliberately NOT matching div/span —
   those selectors outrank the component classes below and would silently undo
   every serif and mono treatment in the design. */
.stApp, .stApp button, .stApp input, .stApp textarea, .stApp select,
.stApp p, .stApp li, .stApp label {
  font-family: 'DM Sans', system-ui, -apple-system, sans-serif;
}
/* Streamlit sets its theme font on markdown containers, which beats plain
   inheritance from .stApp. Set it here too — descendants inherit, and the
   component classes below still win because they are direct rules. */
[data-testid="stMarkdownContainer"], [data-testid="stCaptionContainer"] {
  font-family: 'DM Sans', system-ui, -apple-system, sans-serif;
}
/* icon fonts render by ligature — never let the body face win here */
[data-testid="stIconMaterial"], span[class*="material-symbols"] {
  font-family: 'Material Symbols Rounded', 'Material Icons' !important;
}
/* Clears the sticky top-nav header (~60px) — a smaller value slides the
   page eyebrow underneath it. */
.block-container { padding-top: 3.2rem; padding-bottom: 5rem; max-width: 1240px; }

/* hide Streamlit chrome */
[data-testid="stAppDeployButton"], [data-testid="stToolbarActions"] { display:none !important; }
[data-testid="stDecoration"] { display:none; }
#MainMenu, footer { visibility: hidden; }

/* ---------- header = the design's nav bar, rainbow stripe on its top edge ---------- */
[data-testid="stHeader"] {
  background: var(--cream) !important;
  border-bottom: 1px solid rgba(58,46,31,.08);
  padding-top: 8px;
  height: auto;
}
[data-testid="stHeader"]::before {
  content:''; position:absolute; top:0; left:0; right:0; height:8px;
  background: linear-gradient(90deg,
    #F5C63C 0 14.285%, #F0995E 14.285% 28.57%, #E5A5B0 28.57% 42.85%,
    #C0D77A 42.85% 57.14%, #4A6D3F 57.14% 71.42%, #8CC0D6 71.42% 85.71%,
    #9AA0C9 85.71% 100%);
}
[data-testid="stToolbar"] { background: transparent; }

/* nav pills */
[data-testid="stTopNavLinkContainer"] a {
  font:600 13px 'DM Sans', sans-serif !important;
  color: var(--ink-2) !important;
  border-radius: 10px !important;
  padding: 8px 14px !important;
  transition: background .2s ease, color .2s ease;
}
[data-testid="stTopNavLinkContainer"] a:hover { background: rgba(58,46,31,.06) !important; color: var(--ink) !important; }
[data-testid="stTopNavLinkContainer"] a[aria-current="page"] {
  background: var(--paper) !important; color: var(--ink) !important;
  box-shadow: 0 2px 8px rgba(58,46,31,.08);
}
[data-testid="stTopNavLinkContainer"] [data-testid="stIconMaterial"] { font-size:17px !important; }

/* ---------- typography ---------- */
.serif { font-family:'Instrument Serif', Georgia, serif; font-weight:400; letter-spacing:-.01em; }
.italic { font-style:italic; }
.eyebrow {
  font-family:'JetBrains Mono', ui-monospace, monospace;
  font-size:10px; letter-spacing:.2em; text-transform:uppercase;
  color:var(--ink-2); opacity:.75;
}
h1, h2 { font-family:'Instrument Serif', Georgia, serif !important; font-weight:400 !important;
         color:var(--ink) !important; letter-spacing:-.01em; }
h3, h4 { font-family:'DM Sans', sans-serif !important; font-weight:700 !important; color:var(--ink) !important; }
h1 { font-size:60px !important; line-height:1 !important; margin:.35rem 0 .4rem !important; }
h1 em, h2 em { color:var(--forest); font-style:italic; }

/* page header block */
.page-head { margin-bottom:1.6rem; }
.page-head h1 { margin:.4rem 0 .45rem !important; }
.page-sub { font-family:'DM Sans',sans-serif; font-size:15px; color:var(--ink-2); margin:0 0 1.5rem; max-width:600px; line-height:1.55; }

/* ---------- brand ---------- */
.brand { font-family:'Instrument Serif', Georgia, serif; font-size:28px; line-height:1; color:var(--ink); }
.brand em { color:var(--forest); font-style:normal; }
.brand .plus {
  display:inline-grid; place-items:center; width:26px; height:26px;
  background:var(--red); color:#fff; border-radius:8px;
  font-family:'DM Sans',sans-serif; font-weight:700; font-size:18px;
  margin-right:8px; vertical-align:-4px; transform:rotate(-6deg);
}

/* ---------- hero ---------- */
.hero { padding:.5rem 0 1.5rem; }
.hero-eyebrow {
  display:inline-flex; align-items:center; gap:10px; padding:6px 14px;
  background:var(--paper); border:1px solid rgba(58,46,31,.15); border-radius:999px;
  font:600 11px 'DM Sans',sans-serif; color:var(--ink-2); margin-bottom:20px;
}
.hero-eyebrow .dot { width:8px; height:8px; background:var(--red); border-radius:50%; }
.hero h1 {
  font-family:'Instrument Serif',Georgia,serif !important;
  font-size:clamp(3.2rem, 6.5vw, 6rem) !important; line-height:.94 !important;
  margin:0 0 1.1rem !important;
}
.hero h1 em { color:var(--forest); position:relative; display:inline-block; font-style:italic; }
.hero h1 em::after {
  content:''; position:absolute; left:0; right:0; bottom:8px; height:14px;
  background:var(--yellow); z-index:-1; opacity:.55; transform:skewX(-8deg);
}
.hero p { font-size:17px; line-height:1.55; max-width:520px; color:var(--ink-2); margin:0 0 1.6rem; }
.hero-stats { display:flex; gap:36px; padding-top:20px; border-top:1px solid rgba(58,46,31,.1); flex-wrap:wrap; }
.hero-stats .s { display:flex; flex-direction:column; gap:4px; }
.hero-stats .n { font-family:'Instrument Serif',serif; font-size:38px; line-height:1; color:var(--forest); }
.hero-stats .l { font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--ink-2); letter-spacing:.1em; }

/* ---------- cards ---------- */
.card {
  background:var(--paper); border-radius:22px; padding:26px;
  border:1px solid rgba(58,46,31,.08); position:relative; height:100%;
}
.card-icon {
  width:44px; height:44px; display:grid; place-items:center;
  background:var(--cream-2); border-radius:13px; font-size:1.3rem; line-height:1;
}
.card-num {
  font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:.16em;
  color:var(--ink-2); opacity:.65;
}
.card-title { font-family:'Instrument Serif',serif; font-size:1.5rem; color:var(--ink); margin:.9rem 0 .45rem; line-height:1.1; }
.card-body { font-family:'DM Sans',sans-serif; font-size:.92rem; color:var(--ink-2); line-height:1.6; margin-bottom:1rem; }
.card-link { font:700 12px 'DM Sans',sans-serif; color:var(--forest); letter-spacing:.02em; }
.card-top { display:flex; justify-content:space-between; align-items:flex-start; }

/* ---------- chips / badges ---------- */
.chip {
  display:inline-flex; align-items:center; gap:6px; padding:6px 12px; border-radius:999px;
  font-family:'DM Sans',sans-serif; font-size:12px;
  background:var(--cream-2); border:1px solid var(--line);
  color:var(--ink-2); margin:0 .35rem .4rem 0;
}
.chip.on { background:var(--ink); color:var(--cream); border-color:var(--ink); }
.badge {
  display:inline-block; padding:6px 14px; border-radius:999px; margin:0 .4rem .4rem 0;
  font:700 12px 'DM Sans',sans-serif; background:var(--forest); color:var(--paper);
}
.badge-secondary { background:var(--cream-2); color:var(--ink-2); border:1px solid var(--line); }

/* ---------- stat cells ---------- */
.stat-cell { padding:12px 14px; background:var(--cream-2); border-radius:12px; }
.stat-cell .l { font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--ink-2); letter-spacing:.08em; text-transform:uppercase; }
.stat-cell .v { font-family:'Instrument Serif',serif; font-size:26px; line-height:1.1; margin-top:4px; color:var(--ink); }

/* ---------- Streamlit widgets ---------- */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
  background:var(--cream-2) !important; border:1px solid var(--line) !important;
  border-radius:10px !important; color:var(--ink) !important;
  font-family:'DM Sans',sans-serif !important; font-size:14px !important;
}
[data-testid="stTextArea"] textarea { line-height:1.55 !important; }
label, [data-testid="stWidgetLabel"] p {
  font-size:12px !important; font-weight:600 !important; color:var(--ink-2) !important;
}

/* multiselect pills read as design chips */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
  background:var(--ink) !important; color:var(--cream) !important; border-radius:999px !important;
}

/* buttons */
.stButton > button {
  background:var(--paper); color:var(--ink); border:1px solid rgba(58,46,31,.15);
  border-radius:10px; font:600 12px 'DM Sans',sans-serif; padding:.55rem .9rem;
  transition:transform .18s ease, background .18s ease;
}
.stButton > button:hover { background:var(--cream-2); border-color:rgba(58,46,31,.3); color:var(--ink); transform:translateY(-1px); }
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"] {
  background:var(--yellow); color:var(--ink); border:none;
  border-radius:14px; font:700 14px 'DM Sans',sans-serif; padding:.85rem 1rem;
}
.stButton > button[kind="primary"]:hover, .stButton > button[data-testid="stBaseButton-primary"]:hover {
  background:#E8B825; transform:translateY(-2px); color:var(--ink);
}
[data-testid="stDownloadButton"] > button {
  background:var(--paper); border:1px solid rgba(58,46,31,.15); border-radius:10px;
  font:600 12px 'DM Sans',sans-serif; color:var(--ink);
}

/* expanders as paper cards */
[data-testid="stExpander"] {
  background:var(--paper); border:1px solid rgba(58,46,31,.08);
  border-radius:18px; overflow:hidden;
}
[data-testid="stExpander"] summary { font-weight:600 !important; color:var(--ink) !important; }

/* alerts */
[data-testid="stAlert"] { border-radius:14px; border:1px solid var(--line); }
[data-testid="stAlertContentInfo"] { background:var(--cream-2); }
[data-testid="stAlertContentSuccess"] { background:#EDF3DE; }
[data-testid="stAlertContentWarning"] { background:#FDF0D8; }

/* chat */
[data-testid="stChatMessage"] { background:var(--paper); border:1px solid rgba(58,46,31,.08); border-radius:18px; }
[data-testid="stChatInput"] { border-radius:14px; }

/* misc */
[data-testid="stMetricValue"] { font-family:'Instrument Serif',serif !important; color:var(--forest) !important; }
hr, [data-testid="stDivider"] { border-color:rgba(58,46,31,.12); }
code, pre, [data-testid="stCode"] { font-family:'JetBrains Mono', ui-monospace, monospace !important; }
[data-testid="stCode"] { background:var(--paper) !important; border-radius:12px; }
.stProgress > div > div > div { background:var(--forest) !important; }

/* ---------- report document ---------- */
.report-doc-marker { display:none; }
[data-testid="stVerticalBlock"]:has( > [data-testid="stElementContainer"] .report-doc-marker) {
  color:var(--ink);
}
[data-testid="stVerticalBlock"]:has( > [data-testid="stElementContainer"] .report-doc-marker) h1 {
  font-size:1.7rem !important; line-height:1.15; margin-bottom:.1rem !important;
}
[data-testid="stVerticalBlock"]:has( > [data-testid="stElementContainer"] .report-doc-marker) h2 {
  font-size:1rem !important; color:var(--ink-2); font-weight:400 !important; margin-top:0 !important;
}
[data-testid="stVerticalBlock"]:has( > [data-testid="stElementContainer"] .report-doc-marker) h3 {
  font-family:'JetBrains Mono',monospace !important; font-size:.72rem !important;
  letter-spacing:.16em; text-transform:uppercase; color:var(--ink-2) !important;
  margin-top:1.5rem; padding-bottom:.35rem; border-bottom:1px solid var(--line);
}
[data-testid="stVerticalBlock"]:has( > [data-testid="stElementContainer"] .report-doc-marker) p,
[data-testid="stVerticalBlock"]:has( > [data-testid="stElementContainer"] .report-doc-marker) li {
  font-size:.9rem; line-height:1.62;
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def rainbow():
    """The stripe that opens every page in the design."""
    bars = "".join('<span style="background:{}"></span>'.format(c) for c in RAINBOW)
    st.markdown('<div class="rainbow">' + bars + "</div>", unsafe_allow_html=True)


def brand():
    st.markdown(
        '<div class="brand"><span class="plus">+</span>Therapy<em>Navigator</em></div>',
        unsafe_allow_html=True,
    )


def page_chrome():
    """Shared chrome applied once by app.py, before the selected page runs.

    The rainbow stripe rides the header's top edge in CSS, so there is no
    separate element to render here.
    """
    inject_css()


def page_header(title, subtitle, eyebrow=None):
    """Design's page-head: mono eyebrow, serif headline, muted standfirst.

    `title` may contain <em> for the italic forest-green accent.
    """
    block = '<div class="page-head">'
    if eyebrow:
        block += '<div class="eyebrow">' + eyebrow + "</div>"
    block += "<h1>" + title + "</h1></div>"
    st.markdown(block, unsafe_allow_html=True)
    st.markdown('<div class="page-sub">' + subtitle + "</div>", unsafe_allow_html=True)


def how_it_works(body):
    with st.expander("How this works"):
        st.info(body)


def api_key_banner():
    """Warn once, up front, if no key is configured — before the user types."""
    if not api_key_configured():
        st.warning(
            "No Anthropic API key detected. Add `ANTHROPIC_API_KEY` to your "
            "`.env` file (local) or app secrets (Streamlit Cloud). You can "
            "explore the interface, but generating results will fail."
        )


# Retained so existing imports keep working; the design uses top navigation, so
# there is no sidebar to brand or foot.
def sidebar_brand():
    return


def sidebar_footer():
    return
