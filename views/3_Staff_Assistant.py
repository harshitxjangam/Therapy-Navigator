"""Staff Knowledge Assistant — grounded chat over an embedded knowledge base."""

import streamlit as st

from utils.claude_client import call_claude_messages, error_body, is_error
from utils.ui import api_key_banner, how_it_works, page_header


KNOWLEDGE_BASE = """
THE FOUR THERAPY DISCIPLINES

Speech-Language Therapy (SLT)
Speech-language pathologists treat communication and swallowing. That covers
articulation (how clearly sounds are produced), expressive language (putting
words together), receptive language (understanding what others say), fluency
(stuttering), voice, social communication, and feeding/swallowing difficulties
(dysphagia). Common referrals: late talkers, children who are hard to
understand outside the family, children who stutter, children with autism who
need language or AAC support, and infants and toddlers with feeding problems.
A first evaluation runs 60-90 minutes and mixes standardized testing with play-
based observation and a detailed parent interview. Plain-language explanation
for parents: "Speech therapy helps your child be understood and understand
others — through play, games and practice, not drills at a desk."

Occupational Therapy (OT)
Occupational therapists help children participate in the everyday "occupations"
of childhood: dressing, eating, writing, playing, and managing their bodies in
a busy environment. Focus areas are fine motor skills (pencil grip, scissors,
buttons, zippers), visual-motor integration, sensory processing, self-
regulation, and activities of daily living (ADLs). Common referrals: messy or
painful handwriting, trouble with utensils or clothing fasteners, extreme
reactions to noise/textures/lights, difficulty settling after transitions, and
picky eating with a sensory component. A first evaluation runs 60-90 minutes
and includes fine-motor testing, a sensory profile questionnaire completed by
caregivers, and structured play. Plain-language explanation: "OT helps your
child do the everyday things kids need to do — get dressed, hold a pencil,
handle a loud room — with more independence and less frustration."

Physical Therapy (PT)
Physical therapists address gross motor skills, strength, balance,
coordination, gait, and mobility. Common referrals: not meeting motor
milestones (rolling, sitting, crawling, walking), toe walking, frequent falls,
low muscle tone, torticollis and plagiocephaly in infants, and children with
cerebral palsy, spina bifida or post-surgical needs. A first evaluation runs
45-60 minutes and covers milestone history, range of motion, strength, gait
observation, and functional movement. Plain-language explanation: "PT works on
how your child moves — strength, balance and coordination — so they can keep
up on the playground safely and confidently."

Applied Behavior Analysis (ABA)
ABA is a structured, data-driven approach used most often with autistic
children and children with developmental differences. It builds communication,
social, play, self-help and daily-living skills, and reduces behaviors that
interfere with learning or safety. Sessions are led by a Registered Behavior
Technician (RBT) under a Board Certified Behavior Analyst (BCBA) who designs
and supervises the plan. Programs are typically more intensive than the other
disciplines — often 10-25+ hours per week. The assessment phase includes a
functional behavior assessment and skills assessment (e.g. VB-MAPP) and can
take several sessions. Plain-language explanation: "ABA breaks big skills into
small steps, teaches them one at a time with lots of encouragement, and tracks
progress carefully so we know what's working."

WHAT A SESSION LOOKS LIKE
Most SLT, OT and PT sessions run 30-60 minutes, once or twice a week, in a
clinic gym or treatment room, and the work is play-based. Caregivers are
usually invited in for part of the session and always get a home-practice plan.
ABA sessions run longer (2-4 hours) and are more frequent. Progress is reviewed
formally every 3-6 months against the goals in the plan of care.

INSURANCE AND AUTHORIZATION BASICS
Prior authorization (prior auth) is the payer's advance approval for a course
of therapy. The clinic submits the evaluation report, the plan of care, and the
diagnosis codes; the payer reviews medical necessity and approves a set number
of visits over a set window. It commonly takes 5-15 business days, longer if
the payer requests more documentation — that wait is the single most common
reason a family sits between evaluation and first treatment session.
Authorizations expire and must be renewed with a progress report, so track end
dates, not just approvals. Denials are frequently administrative (missing
documentation, wrong code, expired referral, out-of-network provider) rather
than clinical, and many are overturned on appeal or peer-to-peer review. Common
billing terms: CPT codes identify the service (evaluations have their own
codes; treatment is often billed in 15-minute timed units), ICD-10 codes
identify the diagnosis, an EOB is the payer's explanation of benefits, and the
deductible/copay/coinsurance determine family responsibility. Some states'
Medicaid and Early Intervention programs cover therapy through age three with a
different process entirely. Never quote specific coverage or dollar amounts to
a family — route them to the billing team for a benefits check.

COMMON PARENT QUESTIONS
"How long will my child need therapy?" — It depends on the goals, the starting
point, and how consistent practice is at home. Give a review horizon, not a
duration: "We'll set goals now and formally review progress in three months."
"Will insurance cover this?" — Most plans cover medically necessary pediatric
therapy, but coverage, visit limits and family cost vary. Offer a benefits
check rather than a yes/no.
"How do I know if it's working?" — Progress is measured against specific,
written goals and reviewed every few months. Real-world change (understood by a
new teacher, dressing independently) matters as much as test scores.
"Why is there a wait?" — Demand for pediatric therapy exceeds the supply of
licensed clinicians nearly everywhere. Be honest, give a realistic range, and
keep the family updated rather than going silent.
"Can I stay in the room?" — Usually yes, and caregiver participation improves
carryover; the therapist may occasionally suggest stepping out.
"Is this my fault?" — No. Reassure directly and move to what happens next.

HOW A PEDIATRIC CLINIC OPERATES
The typical flow is referral -> intake and insurance verification -> evaluation
-> plan of care and prior authorization -> recurring treatment slots ->
progress review -> reauthorization or discharge. Recurring weekly slots are the
scarcest resource in the building, which is why cancellation and no-show rates
matter so much: an unfilled slot cannot be recovered. Waitlists are usually
managed by discipline and by the times a family can actually attend — after-
school slots are the most contested. Many children see more than one discipline
and benefit from co-treatment. A referral from a pediatrician or specialist is
required by many payers before an evaluation can be billed.
""".strip()

SYSTEM_PROMPT = """You are a knowledgeable, friendly internal assistant for a pediatric therapy clinic called Oaklin Lane. You help clinic staff quickly get accurate information about therapy types, patient/family communication, insurance, and clinical operations.

Here is your knowledge base:

{knowledge}

Answer questions clearly and concisely. If a staff member needs to explain something to a parent, help them phrase it simply. If a question is outside your knowledge base, say so clearly and suggest who to ask. Never guess about specific insurance coverage or clinical diagnoses. Keep responses under 250 words unless a longer answer is clearly needed. Use bullet points for multi-part answers.""".format(
    knowledge=KNOWLEDGE_BASE
)

QUICK_TOPICS = [
    "What is OT therapy?",
    "How does ABA work?",
    "What is a speech evaluation?",
    "What insurance do we accept?",
    "How do I explain PT to parents?",
    "What is sensory processing disorder?",
]

# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #
title_col, clear_col = st.columns([5, 1])
with title_col:
    page_header(
        "Ask what your <em>team</em> asks.",
        "In the moment, on your side. Grounded answers on therapy types, "
        "evaluations, insurance and authorization \u2014 and a straight "
        "\u201ccheck with billing\u201d when that's the honest answer.",
        eyebrow="Tool 03 \u00b7 Assistant",
    )
with clear_col:
    st.write("")
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

how_it_works(
    "This assistant is grounded in a clinic knowledge base covering the four "
    "therapy disciplines, evaluations, insurance and authorization basics, "
    "common parent questions, and how a pediatric clinic runs day to day. It "
    "answers from that document rather than from open-ended guesswork, and it "
    "will tell you when a question falls outside what it knows. It remembers "
    "the conversation, so you can ask follow-ups."
)
api_key_banner()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------------------------------- #
# Quick topics
# --------------------------------------------------------------------------- #
st.caption("Quick topics")
pending = None
for row_start in (0, 3):
    for col, question in zip(
        st.columns(3, gap="small"), QUICK_TOPICS[row_start:row_start + 3]
    ):
        if col.button(question, use_container_width=True, key="topic_" + question):
            pending = question

st.write("")

# --------------------------------------------------------------------------- #
# Chat
# --------------------------------------------------------------------------- #
typed = st.chat_input("Ask anything about pediatric therapy...")
question = typed or pending

if not st.session_state.messages and not question:
    st.info("Ask a question below, or tap a quick topic above to get started.")

for message in st.session_state.messages:
    avatar = "🏥" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🏥"):
        with st.spinner("Thinking..."):
            answer = call_claude_messages(
                SYSTEM_PROMPT,
                st.session_state.messages,
                max_tokens=1200,
            )
        if is_error(answer):
            st.error(error_body(answer))
            st.caption("Try asking again — most issues clear up on a second attempt.")
            # Drop the unanswered question so history stays consistent.
            st.session_state.messages.pop()
        else:
            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

# --------------------------------------------------------------------------- #
# Knowledge base contents
# --------------------------------------------------------------------------- #
st.write("")
with st.expander("📚 Knowledge base topics"):
    st.markdown(
        """
- **Speech-Language Therapy** — what it is, who it helps, what sessions look
  like, common goals
- **Occupational Therapy** — sensory processing, fine motor skills, activities
  of daily living
- **Physical Therapy** — gross motor skills, developmental milestones, mobility
- **ABA Therapy** — behavior, autism, structured interventions, supervision
  model
- **Insurance & billing basics** — prior authorization, denials and appeals,
  CPT/ICD-10 overview
- **Common parent questions** — and how to answer them in plain language
- **Waitlist and scheduling** — how the referral-to-treatment pipeline works
        """
    )
    st.caption(
        "The assistant answers from this document. For anything outside it — "
        "a specific patient, a specific policy, or a clinical decision — check "
        "with the clinical director or billing lead."
    )

