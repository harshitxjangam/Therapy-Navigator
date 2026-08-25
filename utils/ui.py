"""Shared look-and-feel for TherapyNavigator.

Streamlit runs each page as its own script, so the CSS and sidebar branding have
to be re-applied on every page rather than only in app.py.
"""

import os

import streamlit as st

from utils.claude_client import api_key_configured

LOGO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png"
)

PRIMARY = "#1D9E75"

CSS = """
<style>
    /* ---- foundation ---- */
    :root { --ink: #163B43; --muted: #5F7772; --sage: #E7F0EA; --mint: #DDF2E9; --teal: #127A68; --cream: #FBF8F1; --coral: #E48669; }
    .stApp { background: #FCFCFA; }
    .block-container { padding-top: 2.15rem; padding-bottom: 5rem; max-width: 1210px; }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { display: none; }

    /* ---- sidebar ---- */
    section[data-testid="stSidebar"] {
        background: #F1F7F3;
        border-right: 1px solid #D7E6DC;
    }

    /* Streamlit renders the nav above user content; flip the order so the
       brand block sits on top, and pin the footer note to the bottom. */
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        display: flex;
        flex-direction: column;
        min-height: 100%;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] { order: 0; }
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        order: 1;
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] { order: 2; }
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"]::after {
        content: "Thoughtful tools for teams doing meaningful work.";
        order: 3;
        margin-top: auto;
        padding: 1.25rem 1.5rem 1rem 1.5rem;
        font-size: 0.72rem;
        line-height: 1.5;
        color: #78908A;
    }
    section[data-testid="stSidebar"] .sidebar-brand {
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 1.45rem; font-weight: 700; color: #163B43;
        letter-spacing: -0.05em; margin-bottom: 0.18rem;
    }
    section[data-testid="stSidebar"] .sidebar-tagline {
        font-size: 0.82rem;
        color: #58716B;
        line-height: 1.4;
    }
    section[data-testid="stSidebar"] .sidebar-footer {
        font-size: 0.72rem;
        color: #78908A;
        line-height: 1.5;
        padding-top: 0.5rem;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] { padding: .6rem .75rem 0; }
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] { border-radius: 10px; margin: 3px 0; padding: .58rem .72rem; color: #46635C; }
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover { background: #DCEDE2; color: #0D6857; }
    section[data-testid="stSidebar"] [aria-current="page"] { background: #D7EDE1 !important; color: #0E6D5B !important; font-weight: 650; }

    /* ---- typography ---- */
    h1, h2, h3 { color: var(--ink); letter-spacing: -0.035em; }
    h1 { font-family: Georgia, 'Times New Roman', serif; font-weight: 700 !important; }
    h2 { font-family: Georgia, 'Times New Roman', serif; }
    h3 { font-weight: 700; }
    .page-sub {
        color: #617872; font-size: 1rem; margin-top: -.5rem; margin-bottom: 1.55rem;
    }
    .eyebrow, .home-kicker { font-size: .69rem; font-weight: 750; letter-spacing: .13em; color: #20806D; }

    /* ---- cards ---- */
    .card {
        background: #FFFFFF; border: 1px solid #E1EAE2; border-radius: 16px;
        padding: 1.5rem; box-shadow: 0 5px 18px rgba(40, 81, 68, .045);
        height: 100%;
    }
    .card-icon { width: 48px; height: 48px; display: grid; place-items: center; background: #E3F3EA; border-radius: 15px; font-size: 1.45rem; line-height: 1; }
    .card-title {
        font-size: 1.08rem; font-weight: 700; color: #153A38; margin: .82rem 0 .38rem;
    }
    .card-body {
        font-size: .9rem; color: #60756F; line-height: 1.58; margin-bottom: .9rem;
    }
    .card-link {
        font-size: .8rem; font-weight: 750; color: #157966; letter-spacing: .01em;
    }
    .tool-card { position: relative; overflow: hidden; background: white; border: 1px solid #DEEAE0; border-radius: 18px; padding: 1.45rem; box-shadow: 0 8px 22px rgba(26, 68, 57, .04); height: 100%; transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease; }
    .tool-card::after { content: ''; position: absolute; left: 0; bottom: 0; width: 100%; height: 3px; background: linear-gradient(90deg, #16816B, #BDE3CA); opacity: 0; transition: opacity .18s ease; }
    .tool-card:hover { transform: translateY(-4px); border-color: #B9DACE; box-shadow: 0 14px 30px rgba(26, 68, 57, .09); }.tool-card:hover::after { opacity: 1; }
    .tool-card-top { display: flex; justify-content: space-between; align-items: flex-start; }
    .tool-card .card-title { font-size: 1.14rem; margin-top: 1.25rem; }
    .tool-card-status { display: inline-flex; align-items: center; gap: .35rem; color: #6B8580; font-size: .7rem; font-weight: 700; }.tool-card-status i { height: 6px; width: 6px; border-radius: 50%; background: #46AE7B; box-shadow: 0 0 0 3px #E3F5E9; }
    .tool-card .card-link span { font-size: 1rem; margin-left: .15rem; }

    /* ---- hero ---- */
    .hero {
        background: linear-gradient(135deg, #E2F2E7 0%, #EEF7F1 65%); border: 1px solid #D7EADD;
        border-radius: 24px; padding: 2.6rem 2.4rem; margin-bottom: 2.2rem;
    }
    .hero h1 { margin: 0 0 .75rem; font-size: 2.9rem !important; }
    .hero p {
        font-size: 1.06rem; color: #49655D; max-width: 640px; line-height: 1.6; margin: 0;
    }
    .home-kicker { display: flex; gap: .55rem; align-items: center; margin-bottom: .75rem; }
    .home-kicker span { width: 8px; height: 8px; border-radius: 50%; background: #E48669; box-shadow: 0 0 0 4px #F9E5DD; }
    .hero-home { min-height: 340px; padding: 3.1rem 3.2rem; display: grid; grid-template-columns: 1.12fr .88fr; gap: 1rem; overflow: hidden; position: relative; background: radial-gradient(circle at 84% 12%, #D0EDD5 0, transparent 31%), linear-gradient(120deg, #DFF1E7, #F7FBF7 68%); }
    .hero-home::after { content: ''; position: absolute; width: 390px; height: 390px; right: -150px; bottom: -240px; border: 1px solid rgba(33,116,92,.15); border-radius: 50%; box-shadow: 0 0 0 32px rgba(33,116,92,.035), 0 0 0 64px rgba(33,116,92,.025); }
    .hero-home h1 { font-size: clamp(2.8rem, 4.2vw, 4.25rem) !important; line-height: .98; color: #163B43 !important; }
    .hero-home h1 em { font-weight: 400; color: #167863; }
    .hero-home p { max-width: 490px; }
    .hero-note { display: inline-flex; gap: .45rem; align-items: center; margin-top: 1.65rem; color: #315C52; font-size: .82rem; font-weight: 650; }
    .hero-note b { color: #E48669; font-size: 1rem; }
    .hero-visual { position: relative; min-height: 270px; z-index: 1; }
    .pulse-panel { position: absolute; right: 8%; top: 7%; width: 245px; padding: 1.1rem 1.2rem 1rem; background: rgba(255,255,255,.93); border: 1px solid rgba(212,231,218,.9); border-radius: 17px; box-shadow: 0 17px 36px rgba(26, 83, 64, .13); transform: rotate(3deg); }
    .pulse-panel-head { display: flex; justify-content: space-between; color: #617C73; font-size: .7rem; font-weight: 750; }.pulse-panel-head b { color: #16806C; }
    .pulse-metric { display: flex; align-items: center; gap: .65rem; margin: .8rem 0 .55rem; }.pulse-metric strong { font-family: Georgia, serif; color: #163B43; font-size: 2.55rem; line-height: .9; }.pulse-metric span { color: #78908A; font-size: .67rem; line-height: 1.35; }
    .pulse-chart { height: 54px; display: flex; align-items: flex-end; gap: 7px; padding: 0 2px; border-bottom: 1px solid #E4EEE6; }.pulse-chart i { display: block; width: 19px; border-radius: 6px 6px 2px 2px; background: linear-gradient(#53B78A, #BFE6CE); }.pulse-chart i:nth-child(1){height:23px}.pulse-chart i:nth-child(2){height:33px}.pulse-chart i:nth-child(3){height:28px}.pulse-chart i:nth-child(4){height:43px}.pulse-chart i:nth-child(5){height:38px}.pulse-chart i:nth-child(6){height:47px}.pulse-chart i:nth-child(7){height:52px}
    .pulse-days { display: flex; justify-content: space-between; margin-top: .4rem; color: #90A49E; font-size: .58rem; }
    .visual-card { position: absolute; z-index: 2; display: grid; grid-template-columns: auto 1fr; column-gap: .45rem; padding: .65rem .78rem; min-width: 145px; background: rgba(255,255,255,.91); border: 1px solid rgba(255,255,255,.8); border-radius: 12px; box-shadow: 0 8px 20px rgba(24, 69, 55, .10); color: #24574D; backdrop-filter: blur(3px); }
    .visual-card span { grid-row: 1 / span 2; color: #DD7F63; font-size: 1.2rem; }.visual-card b { font-size: .73rem; }.visual-card small { font-size: .62rem; color: #6D867F; }
    .card-family { top: 20%; left: 0; }.card-time { bottom: 11%; right: 0; }.card-time span { font-size: 1rem; font-weight: 800; color: #15816B; }

    /* ---- home sections ---- */
    .section-heading { display: flex; justify-content: space-between; gap: 2rem; align-items: flex-end; margin: .35rem 0 1.45rem; }
    .section-heading h2 { font-size: 2rem; line-height: 1.06; margin: .45rem 0 0; }
    .section-heading p { max-width: 305px; margin: 0 0 .15rem; color: #657B75; line-height: 1.55; font-size: .91rem; }
    .section-rule { height: 1px; background: #DCE7DE; margin: 3.6rem 0 2.6rem; }.value-heading { margin-bottom: 1.35rem; }
    .value-card { padding: 1.2rem 1.35rem; border-top: 1px solid #D9E7DE; height: 100%; }.value-number { font-family: Georgia, serif; color: #C9DED1; font-size: 2.2rem; line-height: 1; }.value-card .card-title { margin-top: .6rem; }.home-disclaimer { margin-top: 4.4rem; text-align: center; color: #81928C; font-size: .74rem; }

    /* ---- softer alert colors ---- */
    div[data-testid="stAlert"] { border-radius: 12px; border: none; }
    div[data-testid="stAlertContentSuccess"] { background-color: #E9F7F1; }
    div[data-testid="stAlertContentInfo"]    { background-color: #EEF3FA; }
    div[data-testid="stAlertContentWarning"] { background-color: #FDF4E7; }

    /* ---- document-style report container ----
       Scoped with :has() off a marker element rather than a Streamlit testid,
       which is internal and has changed names between versions. ---- */
    .report-doc-marker { display: none; }

    [data-testid="stVerticalBlock"]:has(
        > [data-testid="stElementContainer"] .report-doc-marker
    ) {
        color: #24303B;
    }
    [data-testid="stVerticalBlock"]:has(
        > [data-testid="stElementContainer"] .report-doc-marker
    ) h1 {
        font-size: 1.4rem !important;
        line-height: 1.3;
        margin-bottom: 0.1rem;
        padding-top: 0;
    }
    [data-testid="stVerticalBlock"]:has(
        > [data-testid="stElementContainer"] .report-doc-marker
    ) h2 {
        font-size: 0.98rem !important;
        color: #6B7873;
        font-weight: 500;
        margin-top: 0;
        padding-top: 0;
    }
    [data-testid="stVerticalBlock"]:has(
        > [data-testid="stElementContainer"] .report-doc-marker
    ) h3 {
        font-size: 0.95rem !important;
        margin-top: 1.4rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid #EDF1EF;
    }
    [data-testid="stVerticalBlock"]:has(
        > [data-testid="stElementContainer"] .report-doc-marker
    ) p,
    [data-testid="stVerticalBlock"]:has(
        > [data-testid="stElementContainer"] .report-doc-marker
    ) li {
        font-size: 0.9rem;
        line-height: 1.6;
    }
    [data-testid="stVerticalBlock"]:has(
        > [data-testid="stElementContainer"] .report-doc-marker
    ) hr {
        margin: 1.1rem 0;
    }

    /* ---- misc ---- */
    .stat-num { font-size: 1.45rem; font-weight: 700; color: #147B67; }
    .badge {
        display: inline-block;
        background: #E1F3EA; color: #157A5A; border: 1px solid #C7E9DC;
        border-radius: 999px;
        padding: 0.28rem 0.85rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 0.4rem 0.4rem 0;
    }
    .badge-secondary {
        background: #EEF3FA; color: #2C5282; border-color: #D3E0F0;
    }
    /* ---- form and interaction polish ---- */
    .stButton > button { border-radius: 10px; border-color: #CFE0D4; font-weight: 650; transition: all .15s ease; }
    .stButton > button:hover { border-color: #76B59B; color: #0F705D; background: #F1F8F3; }
    .stButton > button[kind="primary"] { background: #147B67; border-color: #147B67; box-shadow: 0 4px 10px rgba(20,123,103,.18); }
    .stButton > button[kind="primary"]:hover { background: #0C6C59; color: white; }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stNumberInput"] input { border-radius: 9px; border-color: #D5E3D8; }
    [data-testid="stExpander"] { border: 1px solid #DDE8E0; border-radius: 12px; overflow: hidden; }
    /* ---- immersive home experience ---- */
    .immersive-hero { min-height: 535px; margin: 0; padding: 4.4rem 4.6rem; isolation: isolate; grid-template-columns: 1fr 1fr; background: radial-gradient(circle at 67% 47%, #81D3AD 0 5%, #52AD8A 21%, #287B6B 46%, #163B43 78%); border: 0; border-radius: 28px; box-shadow: 0 25px 65px rgba(17, 64, 59, .2); }
    .immersive-hero::after { display: none; }.hero-grid { position: absolute; inset: 0; z-index: -1; opacity: .18; background-image: linear-gradient(rgba(255,255,255,.27) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.27) 1px, transparent 1px); background-size: 48px 48px; mask-image: linear-gradient(90deg, rgba(0,0,0,.6), transparent 73%); }
    .immersive-hero .hero-copy { align-self: center; z-index: 3; }.hero-chip { width: max-content; display: flex; gap: .45rem; align-items: center; padding: .42rem .7rem; border: 1px solid rgba(255,255,255,.24); border-radius: 999px; color: #D3F0E5; background: rgba(0,0,0,.09); font-size: .65rem; letter-spacing: .1em; font-weight: 750; }.hero-chip i { width: 7px; height: 7px; background: #A7E6B8; border-radius: 50%; box-shadow: 0 0 0 4px rgba(167,230,184,.1); }
    .immersive-hero h1 { margin-top: 1rem; color: #F4FCF7 !important; font-size: clamp(3.7rem, 5.5vw, 5.6rem) !important; text-shadow: 0 4px 16px rgba(0,0,0,.14); }.immersive-hero h1 em { color: #AEE3C0; }.immersive-hero p { color: #C8E8DC; max-width: 420px; font-size: 1.08rem; }.immersive-hero .hero-note { color: #E3F5EC; }.immersive-hero .hero-note b { color: #F6C77B; }
    .immersive-hero .hero-visual { min-height: 420px; perspective: 1000px; }.care-orb { position: absolute; right: 15%; top: 8%; width: 265px; height: 265px; border-radius: 50%; background: radial-gradient(circle at 32% 28%, #D4FFE0 0 4%, #8BE0AE 20%, #47AA83 48%, #187060 70%, #0B3F40 100%); box-shadow: inset -24px -25px 40px rgba(0,37,37,.26), inset 16px 12px 21px rgba(255,255,255,.28), 0 30px 40px rgba(0,0,0,.27); transform: rotateX(55deg) rotateZ(-23deg); }.orb-mark { color: #ECFFF1; position: absolute; left: 44%; top: 38%; font-size: 4rem; text-shadow: 0 4px 15px rgba(0,69,63,.32); }.orb-glow { position: absolute; inset: -30px; background: radial-gradient(circle, rgba(165,237,185,.25), transparent 65%); filter: blur(8px); }
    .orbit { position: absolute; border: 1px solid rgba(209,255,226,.44); border-radius: 50%; transform: rotateX(64deg) rotateZ(-24deg); }.orbit-a { width: 390px; height: 136px; right: -2%; top: 29%; }.orbit-b { width: 298px; height: 104px; right: 10%; top: 35%; border-color: rgba(209,255,226,.22); }.orbital-shadow { position: absolute; width: 270px; height: 80px; border-radius: 50%; background: rgba(0,25,28,.3); filter: blur(15px); right: 13%; top: 66%; transform: rotate(-15deg); }
    .floating-note { position: absolute; display: grid; grid-template-columns: 24px 1fr; column-gap: .42rem; padding: .66rem .75rem; background: rgba(243,255,248,.85); border: 1px solid rgba(255,255,255,.6); backdrop-filter: blur(12px); color: #1C554C; border-radius: 13px; box-shadow: 0 13px 27px rgba(0,31,35,.18); z-index: 2; transform: rotate(-7deg); }.floating-note i { grid-row: 1 / span 2; display: grid; place-items: center; width: 24px; height: 24px; border-radius: 8px; font-style: normal; background: #D5F2DC; color: #177462; }.floating-note b { font-size: .7rem; }.floating-note small { font-size: .61rem; color: #658078; }.note-intake { left: -4%; top: 15%; }.note-team { right: -3%; top: 55%; transform: rotate(7deg); }.note-growth { left: 7%; bottom: 0; transform: rotate(-2deg); }.orbital-dot { position: absolute; height: 13px; width: 13px; border-radius: 50%; background: #F5C577; box-shadow: 0 0 0 6px rgba(245,197,119,.12); }.dot-a { right: 8%; top: 21%; }.dot-b { right: 62%; top: 76%; background: #CBF1DC; }.tiny-caption { position: absolute; right: 10%; bottom: 0; color: rgba(231,255,241,.66); font-size: .6rem; font-weight: 750; letter-spacing: .14em; }
    .hero-footer { display: flex; justify-content: center; align-items: center; gap: 1.1rem; color: #5F7A72; padding: 1.05rem; font-size: .62rem; font-weight: 750; letter-spacing: .12em; }.hero-footer i { height: 4px; width: 4px; background: #E0866B; border-radius: 50%; }
    .journey-intro { display: grid; grid-template-columns: 1.2fr .8fr; align-items: end; gap: 2rem; margin: 5rem 0 1.9rem; }.journey-intro h2 { margin: .48rem 0 0; font-size: 2.55rem; line-height: 1.03; }.journey-intro p { color: #657B75; line-height: 1.6; max-width: 360px; margin: 0 0 .25rem; }
    .journey-link { display: block; color: inherit !important; text-decoration: none !important; }.journey-step { display: grid; grid-template-columns: 64px 68px 1fr auto; gap: 1.3rem; align-items: center; padding: 1.55rem 1.8rem; margin-bottom: .75rem; min-height: 135px; border-radius: 18px; border: 1px solid #DFEAE2; background: linear-gradient(105deg, #FFFFFF, #F8FCF8); transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease; cursor: pointer; }.journey-step:hover { transform: translateX(8px); border-color: #A9D5BB; box-shadow: 0 15px 32px rgba(30,73,59,.09); }.journey-index { color: #A0B8AB; font-family: Georgia, serif; font-size: 1.7rem; }.journey-icon { display: grid; place-items: center; height: 52px; width: 52px; border-radius: 17px; background: #E2F3E7; font-size: 1.4rem; }.journey-copy span { color: #27806B; font-size: .62rem; font-weight: 750; letter-spacing: .1em; }.journey-copy h3 { margin: .23rem 0; font-size: 1.1rem; }.journey-copy p { margin: 0; max-width: 620px; color: #668078; font-size: .88rem; line-height: 1.55; }.journey-action { color: #176F5E; font-size: .78rem; font-weight: 750; white-space: nowrap; }.journey-action b { font-size: 1.1rem; margin-left: .25rem; }.journey-2 { background: linear-gradient(105deg, #F7FCFA, #FFFFFF); }.journey-3 { background: linear-gradient(105deg, #FFFFFF, #F8FBF5); }.journey-4 { background: linear-gradient(105deg, #F8FCF8, #FFFFFF); }
    .statement-band { position: relative; overflow: hidden; display: flex; align-items: center; gap: 2rem; padding: 3.2rem 3.5rem; margin-top: 4.8rem; border-radius: 22px; color: white; background: #173E45; }.statement-band::after { content: ''; position: absolute; right: -70px; top: -120px; width: 360px; height: 360px; border-radius: 50%; border: 50px solid rgba(101,193,150,.15); }.statement-band span { color: #A4D8BF; font-weight: 750; font-size: .65rem; letter-spacing: .12em; }.statement-band h2 { color: #F3FCF7; font-size: 2rem; line-height: 1.15; max-width: 700px; margin: .45rem 0 0; }.statement-orb { position: relative; z-index: 1; display: grid; place-items: center; flex: 0 0 68px; height: 68px; border-radius: 50%; background: radial-gradient(circle at 30% 28%, #BCF0C8, #2C936F 65%, #19554F); color: white; font-size: 1.7rem; box-shadow: 0 15px 24px rgba(0,0,0,.25); }
    @media (max-width: 760px) { .hero-home { grid-template-columns: 1fr; padding: 2.25rem 1.6rem; }.hero-visual { min-height: 210px; }.section-heading { display: block; }.section-heading p { margin-top: 1rem; }.hero-home h1 { font-size: 3rem !important; }.immersive-hero { min-height: 635px; }.immersive-hero .hero-visual { min-height: 290px; }.care-orb { width: 190px; height: 190px; right: 13%; }.orbit-a { width: 285px; right: -8%; }.orbit-b { width: 215px; right: 7%; }.note-intake { left: 0; }.note-team { right: 0; }.note-growth { display: none; }.hero-footer { flex-wrap: wrap; gap: .6rem; text-align: center; }.journey-intro { display: block; margin-top: 3.2rem; }.journey-intro p { margin-top: 1.2rem; }.journey-step { grid-template-columns: 42px 52px 1fr; gap: .8rem; padding: 1.25rem; }.journey-action { display: none; }.journey-copy p { font-size: .8rem; }.statement-band { padding: 2.2rem 1.6rem; }.statement-band h2 { font-size: 1.55rem; }.statement-orb { display: none; } }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def sidebar_brand():
    """Brand block pinned above the navigation links."""
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=52)
        st.markdown('<div class="sidebar-brand">TherapyNavigator</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-tagline">AI-powered tools for pediatric '
            "therapy operations</div>",
            unsafe_allow_html=True,
        )
        st.divider()


def sidebar_footer():
    """Kept for API stability — the footer note is rendered in CSS so it can be
    pinned below the navigation regardless of render order."""
    return


def page_chrome():
    """Shared chrome applied once by app.py, before the selected page runs."""
    inject_css()
    sidebar_brand()


def page_header(title, subtitle):
    st.markdown("# " + title)
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
