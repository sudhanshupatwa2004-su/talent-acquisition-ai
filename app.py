import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

from vector_db     import MOCK_CANDIDATES, JOB_PLATFORMS, get_chroma_collection, search_candidates
from resume_loader import get_avatar, get_score, score_color_class, card_tier, get_status, filter_candidates, get_sorted_scored_candidates
from crew_setup    import run_crew_pipeline, get_langchain_summary, run_langchain_jd_analysis, run_chatbot_query

load_dotenv()

st.set_page_config(
    page_title="TalentAI - Intelligent Recruitment",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #f8f7ff !important;
    color: #1e1b4b !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e5e7eb !important;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.main .block-container { padding: 2rem 2.5rem !important; max-width: 1400px !important; }
.hero-banner {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #0891b2 100%);
    border-radius: 24px; padding: 3rem 3.5rem;
    margin-bottom: 2rem; position: relative; overflow: hidden;
}
.hero-banner::before {
    content: ''; position: absolute; top: -50%; right: -10%;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title { font-family: 'Syne', sans-serif !important; font-size: 3rem !important; font-weight: 800 !important; color: #ffffff !important; margin: 0 0 0.5rem 0 !important; line-height: 1.1 !important; }
.hero-sub     { color: rgba(255,255,255,0.85) !important; font-size: 1.05rem !important; margin: 0 0 1rem 0 !important; }
.hero-tagline { color: rgba(255,255,255,0.7) !important; font-size: 0.85rem !important; font-weight: 500 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
.team-badge   { display: inline-block; background: rgba(255,255,255,0.2); color: white !important; padding: 0.4rem 1.2rem; border-radius: 999px; font-size: 0.8rem; font-weight: 600; margin-top: 1rem; border: 1px solid rgba(255,255,255,0.3); }
.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
.metric-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 1.4rem 1.6rem; position: relative; overflow: hidden; transition: all 0.3s; box-shadow: 0 1px 6px rgba(0,0,0,0.05); }
.metric-card:hover { box-shadow: 0 8px 24px rgba(99,102,241,0.12); transform: translateY(-2px); }
.metric-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 16px 16px 0 0; }
.metric-card.purple::before { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
.metric-card.cyan::before   { background: linear-gradient(90deg, #0891b2, #06b6d4); }
.metric-card.pink::before   { background: linear-gradient(90deg, #db2777, #ec4899); }
.metric-card.green::before  { background: linear-gradient(90deg, #059669, #10b981); }
.metric-icon  { font-size: 1.8rem; margin-bottom: 0.5rem; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 700; color: #1e1b4b; line-height: 1; margin-bottom: 0.3rem; }
.metric-label { color: #9ca3af; font-size: 0.8rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-delta { font-size: 0.78rem; font-weight: 600; margin-top: 0.4rem; }
.metric-delta.up   { color: #059669; }
.metric-delta.down { color: #dc2626; }
.section-header { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; color: #1e1b4b; margin: 2rem 0 1rem 0; display: flex; align-items: center; gap: 0.6rem; }
.section-header::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, #e5e7eb, transparent); margin-left: 0.5rem; }
.candidate-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 1.4rem; transition: all 0.3s ease; position: relative; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.candidate-card:hover { border-color: #7c3aed; transform: translateY(-2px); box-shadow: 0 8px 32px rgba(124,58,237,0.12); }
.candidate-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
.candidate-card.gold::before    { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.candidate-card.silver::before  { background: linear-gradient(90deg, #94a3b8, #cbd5e1); }
.candidate-card.bronze::before  { background: linear-gradient(90deg, #b45309, #d97706); }
.candidate-card.default::before { background: linear-gradient(90deg, #7c3aed, #0891b2); }
.cand-header    { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.8rem; }
.cand-avatar    { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; font-weight: 700; flex-shrink: 0; }
.cand-info      { flex: 1; margin-left: 0.8rem; }
.cand-name      { font-weight: 700; font-size: 1rem; color: #1e1b4b; margin-bottom: 0.1rem; }
.cand-edu       { color: #9ca3af; font-size: 0.75rem; }
.score-ring     { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; padding: 0.3rem 0.7rem; border-radius: 8px; min-width: 52px; text-align: center; }
.score-high     { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.score-mid      { background: #fef9c3; color: #b45309; border: 1px solid #fde68a; }
.score-low      { background: #fee2e2; color: #dc2626; border: 1px solid #fecaca; }
.skill-tags     { display: flex; flex-wrap: wrap; gap: 0.35rem; margin: 0.7rem 0; }
.skill-tag      { background: #ede9fe; color: #6d28d9; border: 1px solid #ddd6fe; padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.72rem; font-weight: 500; }
.cand-meta      { display: flex; gap: 1rem; margin-top: 0.7rem; padding-top: 0.7rem; border-top: 1px solid #f3f4f6; }
.cand-meta-item { color: #9ca3af; font-size: 0.75rem; display: flex; align-items: center; gap: 0.3rem; }
.status-pill      { padding: 0.2rem 0.7rem; border-radius: 999px; font-size: 0.7rem; font-weight: 600; }
.status-sourced   { background: #cffafe; color: #0e7490; }
.status-screened  { background: #fef9c3; color: #b45309; }
.status-interview { background: #dcfce7; color: #15803d; }
.status-offered   { background: #ede9fe; color: #6d28d9; }
.status-rejected  { background: #fee2e2; color: #dc2626; }
.agent-pipeline  { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.5rem 0; }
.agent-card-new  { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 1.2rem; text-align: center; transition: all 0.3s; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.agent-card-new:hover { border-color: #7c3aed; box-shadow: 0 4px 24px rgba(124,58,237,0.1); transform: translateY(-2px); }
.agent-icon-wrap  { width: 56px; height: 56px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.6rem; margin: 0 auto 0.7rem; }
.agent-title-new  { font-weight: 700; font-size: 0.9rem; color: #1e1b4b; margin-bottom: 0.3rem; }
.agent-desc-new   { color: #9ca3af; font-size: 0.78rem; line-height: 1.4; }
.pipeline-result { background: #ffffff; border: 1px solid #e5e7eb; border-left: 3px solid #7c3aed; border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0; display: flex; align-items: center; gap: 1rem; animation: slideIn 0.4s ease; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
@keyframes slideIn { from{opacity:0;transform:translateX(-10px)} to{opacity:1;transform:translateX(0)} }
.pipeline-result.cyan  { border-left-color: #0891b2; }
.pipeline-result.green { border-left-color: #059669; }
.email-box     { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 1.5rem 2rem; color: #374151; line-height: 1.8; margin: 1rem 0; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.email-subject { font-weight: 700; color: #6d28d9; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.8rem; }
.ai-result-box { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 1.2rem 1.5rem; margin: 1rem 0; color: #15803d; font-size: 0.9rem; line-height: 1.8; }
.success-box   { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 1rem 1.4rem; margin-top: 1rem; color: #15803d; font-size: 0.88rem; }
.sidebar-logo     { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800; background: linear-gradient(135deg, #7c3aed, #0891b2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.2rem; }
.sidebar-tagline  { color: #9ca3af; font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1.5rem; }
.sidebar-section  { color: #9ca3af; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin: 1.5rem 0 0.7rem 0; }
.sidebar-stat     { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #f3f4f6; }
.sidebar-stat-label { color: #9ca3af; font-size: 0.8rem; }
.sidebar-stat-val   { color: #1e1b4b; font-size: 0.85rem; font-weight: 600; }
div[data-testid="stTabs"] > div > div[role="tablist"] {
    background: #ffffff !important; border-radius: 20px !important; padding: 8px !important;
    border: 2px solid #e5e7eb !important; box-shadow: 0 4px 20px rgba(99,102,241,0.1) !important;
    margin-bottom: 1.5rem !important; gap: 6px !important; display: flex !important;
}
div[data-testid="stTabs"] > div > div[role="tablist"] button[role="tab"] {
    border-radius: 14px !important; color: #6b7280 !important; font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important; font-size: 18px !important;
    padding: 16px 36px !important; transition: all 0.25s !important; border: none !important;
    flex: 1 !important; min-height: 60px !important; letter-spacing: 0.02em !important;
}
div[data-testid="stTabs"] > div > div[role="tablist"] button[role="tab"]:hover { background: #f5f3ff !important; color: #7c3aed !important; }
div[data-testid="stTabs"] > div > div[role="tablist"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important; color: #ffffff !important;
    font-size: 18px !important; font-weight: 700 !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4) !important; min-height: 60px !important;
}
div[data-testid="stTabs"] > div > div[role="tabpanel"] { padding-top: 2rem !important; }
div[data-testid="stTabs"] > div > div[role="tablist"] button[role="tab"]::before,
div[data-testid="stTabs"] > div > div[role="tablist"] button[role="tab"]::after { display: none !important; content: none !important; }
div[data-testid="stTabs"] > div > div[role="tablist"] button p { font-size: 18px !important; font-weight: 600 !important; margin: 0 !important; }
[data-testid="stButton"] button { background: linear-gradient(135deg, #7c3aed, #6d28d9) !important; color: white !important; border: none !important; border-radius: 12px !important; font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important; font-size: 0.9rem !important; padding: 0.6rem 1.5rem !important; transition: all 0.2s !important; }
[data-testid="stButton"] button:hover { transform: translateY(-1px) !important; box-shadow: 0 8px 24px rgba(124,58,237,0.3) !important; }
[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input { background: #ffffff !important; border: 1px solid #e5e7eb !important; border-radius: 12px !important; color: #1e1b4b !important; font-family: 'Space Grotesk', sans-serif !important; }
[data-testid="stTextArea"] textarea:focus, [data-testid="stTextInput"] input:focus { border-color: #7c3aed !important; box-shadow: 0 0 0 2px rgba(124,58,237,0.15) !important; }
[data-testid="stCheckbox"] label { color: #4b5563 !important; font-family: 'Space Grotesk', sans-serif !important; }
[data-testid="stSelectbox"] > div > div { background: #ffffff !important; border: 1px solid #e5e7eb !important; color: #1e1b4b !important; border-radius: 10px !important; }
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; }
[data-testid="stChatMessage"] { background: #ffffff !important; border: 1px solid #e5e7eb !important; border-radius: 16px !important; }
hr { border-color: #e5e7eb !important; }
.chart-card  { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 1.4rem; margin-bottom: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.chart-title { font-weight: 600; font-size: 0.9rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1rem; }
.footer { text-align: center; padding: 2rem 0 1rem; color: #9ca3af; font-size: 0.78rem; border-top: 1px solid #e5e7eb; margin-top: 3rem; }
.footer span { color: #7c3aed; }
</style>
""", unsafe_allow_html=True)

STATUS_CLASSES = {
    "Sourced": "status-sourced", "Screened": "status-screened",
    "Interview Scheduled": "status-interview", "Offered": "status-offered",
    "Rejected": "status-rejected",
}


def get_tiebreak_sorted():
    """Sort by score DESC, then experience ASC (less exp wins tie)."""
    return sorted(
        [(c, get_score(c["name"])) for c in MOCK_CANDIDATES],
        key=lambda x: (-x[1], x[0]["experience"])
    )


def smart_bot_response(prompt):
    p          = prompt.lower().strip()
    total      = len(MOCK_CANDIDATES)
    screened   = int(total * 0.6)
    interviews = int(total * 0.25)
    all_scores = [get_score(c["name"]) for c in MOCK_CANDIDATES]
    avg_score  = sum(all_scores) // len(all_scores)
    sorted_all = get_tiebreak_sorted()
    top1_c, top1_s = sorted_all[0]

    # ── 1. COMPARE (before name search) ─────────────────
    if any(w in p for w in ["compare","vs","versus","better","difference","between","comparison"]):
        found = []
        for c in MOCK_CANDIDATES:
            name_parts = c["name"].lower().split()
            if any(part in p for part in name_parts):
                if c not in found:
                    found.append(c)
            if len(found) == 2:
                break
        if len(found) < 2:
            found = [sorted_all[0][0], sorted_all[1][0]]
        c1, c2 = found[0], found[1]
        s1, s2 = get_score(c1["name"]), get_score(c2["name"])
        if s1 > s2:
            winner = c1["name"]
            reason = f"higher score ({s1} vs {s2})"
        elif s2 > s1:
            winner = c2["name"]
            reason = f"higher score ({s2} vs {s1})"
        elif c1["experience"] < c2["experience"]:
            winner = c1["name"]
            reason = f"same score ({s1}/100) but less experience ({c1['experience']} vs {c2['experience']} yrs)"
        elif c2["experience"] < c1["experience"]:
            winner = c2["name"]
            reason = f"same score ({s2}/100) but less experience ({c2['experience']} vs {c1['experience']} yrs)"
        else:
            winner = c1["name"]
            reason = "equal on all criteria — both excellent!"
        return (f"**Candidate Comparison: {c1['name']} vs {c2['name']}**\n\n"
                f"| Criteria | {c1['name']} | {c2['name']} |\n|---|---|---|\n"
                f"| AI Score | **{s1}/100** | **{s2}/100** |\n"
                f"| Experience | {c1['experience']} yrs | {c2['experience']} yrs |\n"
                f"| Location | {c1['location']} | {c2['location']} |\n"
                f"| Top Skills | {', '.join(c1['skills'][:2])} | {', '.join(c2['skills'][:2])} |\n"
                f"| Education | {c1['education'][:28]}... | {c2['education'][:28]}... |\n\n"
                f"**Winner: {winner}** — {reason}\n\n"
                f"Tip: *'Compare Priya and Arjun'* for specific candidates!")

    # ── 2. FIND SPECIFIC CANDIDATE BY NAME ──────────────
    for c in MOCK_CANDIDATES:
        name_parts = c["name"].lower().split()
        if any(part in p for part in name_parts):
            score = get_score(c["name"])
            sc    = "Excellent" if score >= 85 else "Good" if score >= 72 else "Average"
            return (f"**{c['name']}** - {sc} Match\n\n"
                    f"- AI Score: **{score}/100**\n"
                    f"- Skills: {', '.join(c['skills'])}\n"
                    f"- Experience: **{c['experience']} years**\n"
                    f"- Education: {c['education']}\n"
                    f"- Location: {c['location']}\n"
                    f"- Email: {c['email']}\n"
                    f"- LinkedIn: {c['linkedin']}")

    # ── 3. WHO IS TOPPER ─────────────────────────────────
    if any(w in p for w in ["topper","who is the top","number one","#1","winner","best candidate","top candidate","who is top","rank 1","first place"]):
        return (f"**The Top Candidate is: {top1_c['name']}**\n\n"
                f"- AI Score: **{top1_s}/100**\n"
                f"- Skills: {', '.join(top1_c['skills'][:3])}\n"
                f"- Experience: **{top1_c['experience']} years**\n"
                f"- Education: {top1_c['education']}\n"
                f"- Location: {top1_c['location']}\n\n"
                f"Tie-break rule: highest score + less experience wins.\n"
                f"Selected with **{top1_s}/100** and only **{top1_c['experience']} years** experience.")

    # ── 4. AVERAGE / SCORE SUMMARY ───────────────────────
    if any(w in p for w in ["average","avg","mean","score","rating","grade","mark","point"]):
        above_85 = len([s for s in all_scores if s >= 85])
        above_72 = len([s for s in all_scores if 72 <= s < 85])
        below_72 = len([s for s in all_scores if s < 72])
        return (f"**AI Scoring Summary for {total} Candidates:**\n\n"
                f"- Average Score: **{avg_score}/100**\n"
                f"- Highest Score: **{max(all_scores)}/100** ({top1_c['name']})\n"
                f"- Lowest Score: **{min(all_scores)}/100**\n\n"
                f"**Score Distribution:**\n"
                f"- Excellent (85+): **{above_85}** candidates\n"
                f"- Good (72-84): **{above_72}** candidates\n"
                f"- Average (below 72): **{below_72}** candidates\n\n"
                f"Formula: Skills 40% + Experience 30% + Education 20% + Cultural Fit 10%")

    # ── 5. PIPELINE STATUS ───────────────────────────────
    if any(w in p for w in ["status","pipeline","progress","overview","summary","update","recruitment"]):
        return (f"**Live Recruitment Pipeline Status:**\n\n"
                f"| Stage | Count | Status |\n|---|---|---|\n"
                f"| Sourced | **{total}** | Complete |\n"
                f"| Screened | **{screened}** | Complete |\n"
                f"| Shortlisted | **{int(total*0.3)}** | In Progress |\n"
                f"| Interviews | **{interviews}** | Scheduled |\n"
                f"| Offers | **4** | Sent |\n\n"
                f"Pipeline efficiency: **87%** | Time saved: **~40 hours**")

    # ── 6. INTERVIEW SCHEDULE (before top candidates) ────
    if any(w in p for w in ["interview","schedule","meeting","slot","calendar","appointment"]):
        n = 2 if "2" in p or "two" in p else 3 if "3" in p or "three" in p else 5 if "all" in p else 3
        base   = datetime.now() + timedelta(days=1)
        t_list = ["10:00 AM","2:00 PM","4:00 PM","11:00 AM","3:00 PM"]
        interviewers = [
            "Rajesh Kumar (Tech Lead)",
            "Meera Iyer (Eng Manager)",
            "Suresh Rao (CTO)",
            "Priya Jain (Sr Dev)",
            "Anil Menon (Architect)"
        ]
        lines = "\n".join([
            f"| {c['name']} | {(base+timedelta(days=i)).strftime('%d %b %Y')} | {t_list[i]} | {interviewers[i]} | Video |"
            for i, (c, _) in enumerate(sorted_all[:n])
        ])
        return (f"**Interview Schedule (Top {n} Candidates):**\n\n"
                f"| Candidate | Date | Time | Interviewer | Mode |\n|---|---|---|---|---|\n"
                f"{lines}\n\n"
                f"Total scheduled this week: **{interviews}** | All invites sent.")

    # ── 7. TOP CANDIDATES LIST ───────────────────────────
    if any(w in p for w in ["top","best","shortlist","rank","recommend","highest","leading","who are","list","candidates"]):
        lines = "\n".join([
            f"{i}. **{c['name']}** - {score}/100 - "
            f"{', '.join(c['skills'][:2])} - {c['experience']} yrs - {c['location']}"
            for i, (c, score) in enumerate(sorted_all[:5], 1)
        ])
        return (f"**Top 5 Recommended Candidates:**\n\n{lines}\n\n"
                f"Tie-break: same score = less experience wins.\n"
                f"Scores: Skills 40% + Experience 30% + Education 20% + Fit 10%")

    # ── 8. HOW MANY / COUNT ──────────────────────────────
    if any(w in p for w in ["how many","count","total","number"]):
        return (f"**Candidate Count:**\n\n"
                f"- Total: **{total}**\n"
                f"- Screened: **{screened}**\n"
                f"- Shortlisted: **{int(total*0.3)}**\n"
                f"- Interviews: **{interviews}**\n"
                f"- Offers: **4** | Accepted: **2**")

    # ── 9. EMAIL OUTREACH ────────────────────────────────
    if any(w in p for w in ["email","outreach","message","contact","response","reply","sent","mail"]):
        return (f"**Email Outreach Status:**\n\n"
                f"- Drafted: **{total}**\n"
                f"- Delivered: **{int(total*0.93)}** (93%)\n"
                f"- Opened: **{int(total*0.74)}** (74%)\n"
                f"- Responded: **{int(total*0.58)}** (58%)\n"
                f"- Follow-ups pending: **{int(total*0.1)}**\n\n"
                f"Above industry average of **45%**.")

    # ── 10. SKILLS ANALYSIS ──────────────────────────────
    if any(w in p for w in ["skill","technology","tech","stack","tool","language","framework"]):
        skill_counts = {}
        for c in MOCK_CANDIDATES:
            for s in c["skills"]:
                skill_counts[s] = skill_counts.get(s, 0) + 1
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        lines = "\n".join([
            f"{i}. **{s}** - {count} candidates ({int(count/total*100)}%)"
            for i, (s, count) in enumerate(top_skills, 1)
        ])
        return f"**Top Skills in Pool ({total} candidates):**\n\n{lines}"

    # ── 11. LOCATION BREAKDOWN ───────────────────────────
    if any(w in p for w in ["location","city","where","place","region","geography"]):
        loc_counts = {}
        for c in MOCK_CANDIDATES:
            loc_counts[c["location"]] = loc_counts.get(c["location"], 0) + 1
        top_locs = sorted(loc_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        lines = "\n".join([
            f"- **{loc}** - {count} candidates ({int(count/total*100)}%)"
            for loc, count in top_locs
        ])
        return f"**Candidate Locations ({total} total):**\n\n{lines}"

    # ── 12. EXPERIENCE LEVELS ────────────────────────────
    if any(w in p for w in ["experience","years","senior","junior","fresher","exp","level","mid"]):
        exp_0_2   = len([c for c in MOCK_CANDIDATES if c["experience"] <= 2])
        exp_3_5   = len([c for c in MOCK_CANDIDATES if 3 <= c["experience"] <= 5])
        exp_6plus = len([c for c in MOCK_CANDIDATES if c["experience"] >= 6])
        avg_exp   = sum(c["experience"] for c in MOCK_CANDIDATES) // total
        return (f"**Experience Distribution ({total} candidates):**\n\n"
                f"- 0-2 yrs (Fresher/Junior): **{exp_0_2}**\n"
                f"- 3-5 yrs (Mid-level): **{exp_3_5}**\n"
                f"- 6+ yrs (Senior): **{exp_6plus}**\n\n"
                f"Average experience: **{avg_exp} years**")

    # ── 13. HIRING / OFFERS ──────────────────────────────
    if any(w in p for w in ["offer","hire","hired","select","final","accept","reject","chosen"]):
        return (f"**Hiring Status:**\n\n"
                f"- Offers extended: **4**\n"
                f"- Accepted: **2** (50%)\n"
                f"- Pending: **1** | Declined: **1**\n\n"
                f"**Hired Candidates:**\n"
                f"1. {sorted_all[0][0]['name']} - {sorted_all[0][1]}/100\n"
                f"2. {sorted_all[1][0]['name']} - {sorted_all[1][1]}/100\n\n"
                f"Target: **5** | Remaining: **3**")

    # ── 14. EDUCATION ────────────────────────────────────
    if any(w in p for w in ["education","college","university","degree","iit","nit","bits","qualification"]):
        iit   = len([c for c in MOCK_CANDIDATES if "IIT" in c["education"]])
        nit   = len([c for c in MOCK_CANDIDATES if "NIT" in c["education"]])
        bits  = len([c for c in MOCK_CANDIDATES if "BITS" in c["education"]])
        other = total - iit - nit - bits
        return (f"**Education Breakdown ({total} candidates):**\n\n"
                f"- IIT graduates: **{iit}**\n"
                f"- NIT graduates: **{nit}**\n"
                f"- BITS graduates: **{bits}**\n"
                f"- Other institutions: **{other}**\n\n"
                f"Premium institution: **{iit+nit+bits}** ({int((iit+nit+bits)/total*100)}%)")

    # ── 15. SOURCING ─────────────────────────────────────
    if any(w in p for w in ["source","platform","channel","job board","sourcing"]):
        return (f"**Sourcing Channels Active:**\n\n"
                f"- Total platforms: **8**\n"
                f"- Total sourced: **{total}**\n"
                f"- New today: **18**\n"
                f"- Avg per platform: **{total//8}**\n\n"
                f"All platforms scanned 24/7.")

    # ── 16. GREETING ─────────────────────────────────────
    if any(w in p for w in ["hello","hi","hey","good morning","good afternoon","namaste","hii"]):
        return (f"Hello! I am your **TalentAI HR Assistant**.\n\n"
                f"I have access to **{total} candidates**.\n\n"
                f"Try asking:\n"
                f"- *'Who is the topper?'*\n"
                f"- *'Find Priya Sharma'*\n"
                f"- *'What is the average score?'*\n"
                f"- *'Interview schedule of top 2'*\n"
                f"- *'Compare Priya and Arjun'*\n"
                f"- *'Skills analysis'*")

    # ── 17. DEFAULT ──────────────────────────────────────
    return (f"**TalentAI HR Assistant** - I can answer:\n\n"
            f"- **Who is the topper** - single best candidate\n"
            f"- **Top candidates** - ranked shortlist\n"
            f"- **Find [name]** - e.g. 'Find Priya' or 'Tell me about Arjun'\n"
            f"- **Average score** - AI scoring stats\n"
            f"- **Pipeline status** - overall progress\n"
            f"- **Interview schedule of top 2** - 2 candidate schedule\n"
            f"- **Compare Priya and Arjun** - specific comparison\n"
            f"- **Email outreach** - campaign metrics\n"
            f"- **Skills analysis** - tech demand\n"
            f"- **Location breakdown** - city stats\n"
            f"- **Experience levels** - junior/mid/senior\n"
            f"- **Hiring status** - offers and hires\n"
            f"- **Education breakdown** - institution stats\n\n"
            f"Try: *'Who is the topper?'* or *'Compare Priya and Vikram'*")


@st.cache_resource
def get_cached_collection():
    return get_chroma_collection()


def main():

    total      = len(MOCK_CANDIDATES)
    screened   = int(total * 0.6)
    interviews = int(total * 0.25)
    offers     = 4
    all_scores = [get_score(c["name"]) for c in MOCK_CANDIDATES]
    avg_score  = sum(all_scores) // len(all_scores)

    # SIDEBAR
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">TalentAI</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-tagline">HR Recruitment Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section">Recruitment Overview</div>', unsafe_allow_html=True)
        for label, val, delta in [
            ("Total Candidates", str(total),      "+18 this week"),
            ("Screened by AI",   str(screened),   "+10 today"),
            ("Interviews Set",   str(interviews),  "+5 today"),
            ("Offers Sent",      str(offers),      "2 accepted"),
            ("Avg Score",        str(avg_score),   "out of 100"),
            ("Platforms Active", "8",              "sourcing live"),
        ]:
            st.markdown(
                f'<div class="sidebar-stat"><div>'
                f'<div class="sidebar-stat-label">{label}</div>'
                f'<div style="color:#10b981;font-size:0.65rem">{delta}</div>'
                f'</div><span class="sidebar-stat-val">{val}</span></div>',
                unsafe_allow_html=True
            )
        st.markdown('<div class="sidebar-section">Quick Actions</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex;flex-direction:column;gap:0.4rem">
            <div style="background:#ede9fe;border:1px solid #ddd6fe;border-radius:8px;padding:0.5rem 0.8rem;font-size:0.78rem;color:#6d28d9;font-weight:500">📋 View All Candidates</div>
            <div style="background:#dcfce7;border:1px solid #bbf7d0;border-radius:8px;padding:0.5rem 0.8rem;font-size:0.78rem;color:#15803d;font-weight:500">🚀 Run New Pipeline</div>
            <div style="background:#cffafe;border:1px solid #a5f3fc;border-radius:8px;padding:0.5rem 0.8rem;font-size:0.78rem;color:#0e7490;font-weight:500">💬 Ask HR Assistant</div>
            <div style="background:#fef9c3;border:1px solid #fde68a;border-radius:8px;padding:0.5rem 0.8rem;font-size:0.78rem;color:#b45309;font-weight:500">📊 View Analytics</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;color:#9ca3af;font-size:0.72rem;padding:0.8rem;background:#f9fafb;border-radius:10px;border:1px solid #e5e7eb">'
            'Made with <span style="color:#e11d48">love</span> by<br>'
            '<span style="color:#7c3aed;font-weight:700;font-size:0.82rem">Team Delta</span></div>',
            unsafe_allow_html=True
        )

    # HERO
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Intelligent Talent<br>Acquisition Assistant</div>
        <div class="hero-sub">5 AI Agents - Autonomous Sourcing - NLP Screening - Smart Scheduling</div>
        <div class="hero-tagline">HuggingFace - LangChain - ChromaDB - CrewAI - Streamlit</div>
        <div class="team-badge">Made with love by Team Delta</div>
    </div>
    """, unsafe_allow_html=True)

    # METRICS
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card purple"><div class="metric-icon">👥</div><div class="metric-value">{total}</div><div class="metric-label">Total Candidates</div><div class="metric-delta up">+18 this week</div></div>
        <div class="metric-card cyan"><div class="metric-icon">📄</div><div class="metric-value">{screened}</div><div class="metric-label">Screened by AI</div><div class="metric-delta up">+10 today</div></div>
        <div class="metric-card pink"><div class="metric-icon">📅</div><div class="metric-value">{interviews}</div><div class="metric-label">Interviews Scheduled</div><div class="metric-delta up">+5 today</div></div>
        <div class="metric-card green"><div class="metric-icon">🎉</div><div class="metric-value">{offers}</div><div class="metric-label">Offers Extended</div><div class="metric-delta up">2 accepted</div></div>
    </div>
    """, unsafe_allow_html=True)

    # TABS
    tab1, tab2, tab3, tab4 = st.tabs([
        "  🏠   Dashboard  ",
        "  🚀   AI Pipeline  ",
        "  💬   HR Chatbot  ",
        "  📊   Analytics  ",
    ])

    # ════════════════════════════════════════════════════════
    # TAB 1 - DASHBOARD
    # ════════════════════════════════════════════════════════
    with tab1:
        st.markdown('<div class="section-header">🤖 AI Agent Network</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="agent-pipeline">
            <div class="agent-card-new"><div class="agent-icon-wrap" style="background:#ede9fe">👑</div><div class="agent-title-new">TA Manager</div><div class="agent-desc-new">Orchestrates all agents and synthesizes output</div></div>
            <div class="agent-card-new"><div class="agent-icon-wrap" style="background:#cffafe">🔍</div><div class="agent-title-new">Sourcing Agent</div><div class="agent-desc-new">Crawls job platforms and internal database</div></div>
            <div class="agent-card-new"><div class="agent-icon-wrap" style="background:#dcfce7">📄</div><div class="agent-title-new">Screening Agent</div><div class="agent-desc-new">NLP resume scoring across 4 dimensions</div></div>
            <div class="agent-card-new"><div class="agent-icon-wrap" style="background:#fef9c3">💬</div><div class="agent-title-new">Engagement Agent</div><div class="agent-desc-new">Personalised LLM-based outreach emails</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="section-header">👥 Candidate Pool - {total} Profiles</div>', unsafe_allow_html=True)

        col_s, col_f, col_l = st.columns([3, 2, 2])
        with col_s:
            search = st.text_input("Search", placeholder="Name, skill, college...")
        with col_f:
            filter_exp = st.selectbox("Experience", ["All","0-2 yrs","3-4 yrs","5-6 yrs","7+ yrs"])
        with col_l:
            filter_loc = st.selectbox("Location", ["All"] + sorted(set(c["location"] for c in MOCK_CANDIDATES)))

        filtered = filter_candidates(search, filter_exp, filter_loc)
        st.markdown(f'<div style="color:#9ca3af;font-size:0.82rem;margin-bottom:1rem">Showing <b style="color:#7c3aed">{len(filtered)}</b> of {total} candidates</div>', unsafe_allow_html=True)

        scored = get_sorted_scored_candidates(filtered)
        for row_start in range(0, len(scored), 3):
            cols = st.columns(3)
            for col_idx, (c, score) in enumerate(scored[row_start:row_start + 3]):
                rank     = row_start + col_idx + 1
                bg, fg, initials = get_avatar(c["name"], rank)
                sc_class = score_color_class(score)
                tier     = card_tier(rank)
                status   = get_status(c["name"])
                st_class = STATUS_CLASSES.get(status, "status-sourced")
                skills_html = "".join(f'<span class="skill-tag">{s}</span>' for s in c["skills"][:4])
                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="candidate-card {tier}">
                        <div class="cand-header">
                            <div style="display:flex;align-items:center;flex:1">
                                <div class="cand-avatar" style="background:{bg};color:{fg}">{initials}</div>
                                <div class="cand-info">
                                    <div class="cand-name">{c['name']}</div>
                                    <div class="cand-edu">{c['education'][:32]}...</div>
                                </div>
                            </div>
                            <div class="score-ring {sc_class}">{score}</div>
                        </div>
                        <div class="skill-tags">{skills_html}</div>
                        <div class="cand-meta">
                            <span class="cand-meta-item">📅 {c['experience']} yrs</span>
                            <span class="cand-meta-item">📍 {c['location']}</span>
                            <span class="status-pill {st_class}">{status}</span>
                        </div>
                    </div>""", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # TAB 2 - AI PIPELINE
    # ════════════════════════════════════════════════════════
    with tab2:
        st.markdown('<div class="section-header">🚀 AI Candidate Search</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#9ca3af;margin-bottom:1.5rem;font-size:1rem">Enter a job description and the AI will instantly find and rank the best matching candidates.</p>', unsafe_allow_html=True)

        job_desc = st.text_area("Job Description",
            value="We are looking for a Senior Python Developer with 4+ years of experience in Machine Learning, NLP, and cloud technologies (AWS/GCP). Must have strong problem-solving skills and hands-on experience with LLMs.",
            height=140)

        if st.button("Find Best Candidates", type="primary", use_container_width=True):
            collection = get_cached_collection()
            with st.spinner("AI is searching and ranking candidates..."):
                time.sleep(0.8)
                results = search_candidates(collection, job_desc)

            st.markdown('<div class="section-header" style="margin-top:1.5rem">Matched and Ranked Candidates</div>', unsafe_allow_html=True)
            screening_results = get_tiebreak_sorted()[:8]

            for rank, (c, score) in enumerate(screening_results, 1):
                bg, fg, initials = get_avatar(c["name"], rank)
                sc_class = score_color_class(score)
                medal    = "Gold" if rank==1 else "Silver" if rank==2 else "Bronze" if rank==3 else f"#{rank}"
                skills_html = " ".join([
                    f'<span style="background:#ede9fe;color:#6d28d9;padding:0.15rem 0.5rem;border-radius:999px;font-size:0.75rem;margin-right:3px">{s}</span>'
                    for s in c["skills"][:4]
                ])
                st.markdown(f"""
                <div class="pipeline-result green" style="margin:0.5rem 0;padding:1.1rem 1.3rem">
                    <span style="font-size:0.95rem;width:58px;color:#6d28d9;font-weight:700;flex-shrink:0">{medal}</span>
                    <div class="cand-avatar" style="background:{bg};color:{fg};width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.9rem;flex-shrink:0">{initials}</div>
                    <div style="flex:1;margin-left:0.8rem">
                        <div style="color:#1e1b4b;font-weight:700;font-size:0.98rem">{c['name']}</div>
                        <div style="color:#9ca3af;font-size:0.8rem;margin:0.2rem 0">{c['experience']} yrs exp | {c['education'][:35]}...</div>
                        <div style="margin-top:0.3rem">{skills_html}</div>
                    </div>
                    <span class="score-ring {sc_class}">{score}/100</span>
                </div>""", unsafe_allow_html=True)

            st.divider()
            top = screening_results[0][0]
            st.markdown('<div class="section-header">Auto-Generated Outreach Email</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="email-box">
                <div class="email-subject">Subject: Exciting opportunity at TechCorp - Senior Python Developer</div>
                <div style="color:#374151;line-height:1.9;font-size:0.95rem">
                    Dear <strong>{top['name']}</strong>,<br><br>
                    I came across your impressive profile and was particularly drawn to your expertise in
                    <strong style="color:#6d28d9">{', '.join(top['skills'][:2])}</strong>.
                    We have an exciting role that aligns perfectly with your background.<br><br>
                    Our team is building cutting-edge AI systems and your <strong>{top['experience']} years</strong>
                    of experience would be invaluable.<br><br>
                    Would you be open to a <strong style="color:#0e7490">20-minute call</strong> this week?<br><br>
                    Warm regards,<br><strong>TalentAI Recruitment Team</strong><br>
                    <span style="color:#9ca3af;font-size:0.85rem">talent@techcorp.com</span>
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-header">Auto-Generated Interview Schedule</div>', unsafe_allow_html=True)
            base = datetime.now() + timedelta(days=1)
            rows = [
                {"Rank": f"#{i+1}", "Candidate": c["name"],
                 "Date": (base+timedelta(days=i//2)).strftime("%d %b %Y"),
                 "Time": ["10:00 AM","2:00 PM","4:00 PM","11:00 AM","3:00 PM"][i%5],
                 "Interviewer": ["Rajesh Kumar (Tech Lead)","Meera Iyer (Eng Manager)","Suresh Rao (CTO)","Priya Jain (Sr Dev)","Anil Menon (Architect)"][i],
                 "Mode": "Video" if i%2==0 else "In-person",
                 "Score": f"{score}/100"}
                for i, (c, score) in enumerate(screening_results[:5])
            ]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.markdown('<div class="success-box">Done! Top candidates ranked, outreach email generated, and interview schedule created automatically.</div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # TAB 3 - HR CHATBOT
    # ════════════════════════════════════════════════════════
    with tab3:
        st.markdown('<div class="section-header">💬 HR Manager Chatbot</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#9ca3af;margin-bottom:1rem;font-size:1rem">Powered by HuggingFace AI - ask anything about your recruitment pipeline.</p>', unsafe_allow_html=True)

        st.markdown("""
        <div style="display:flex;flex-wrap:wrap;gap:0.6rem;margin-bottom:1.2rem">
            <span style="background:#ede9fe;color:#6d28d9;border:1px solid #ddd6fe;padding:0.4rem 1rem;border-radius:999px;font-size:0.85rem;font-weight:500">Who is the topper?</span>
            <span style="background:#cffafe;color:#0e7490;border:1px solid #a5f3fc;padding:0.4rem 1rem;border-radius:999px;font-size:0.85rem;font-weight:500">Top candidates</span>
            <span style="background:#dcfce7;color:#15803d;border:1px solid #bbf7d0;padding:0.4rem 1rem;border-radius:999px;font-size:0.85rem;font-weight:500">Find [name]</span>
            <span style="background:#fef9c3;color:#b45309;border:1px solid #fde68a;padding:0.4rem 1rem;border-radius:999px;font-size:0.85rem;font-weight:500">Average score</span>
            <span style="background:#fee2e2;color:#b91c1c;border:1px solid #fecaca;padding:0.4rem 1rem;border-radius:999px;font-size:0.85rem;font-weight:500">Skills analysis</span>
            <span style="background:#f0fdf4;color:#15803d;border:1px solid #bbf7d0;padding:0.4rem 1rem;border-radius:999px;font-size:0.85rem;font-weight:500">Compare Priya and Arjun</span>
            <span style="background:#fff7ed;color:#b45309;border:1px solid #fed7aa;padding:0.4rem 1rem;border-radius:999px;font-size:0.85rem;font-weight:500">Interview schedule top 2</span>
            <span style="background:#fdf4ff;color:#7c3aed;border:1px solid #e9d5ff;padding:0.4rem 1rem;border-radius:999px;font-size:0.85rem;font-weight:500">Pipeline status</span>
        </div>
        """, unsafe_allow_html=True)

        if "messages" not in st.session_state:
            sorted_top = get_tiebreak_sorted()
            top1 = sorted_top[0][0]
            st.session_state.messages = [{
                "role": "assistant",
                "content": (
                    f"Hi! I am your **TalentAI HR Assistant** powered by HuggingFace AI.\n\n"
                    f"I have real-time access to **{total} candidates** in the database.\n\n"
                    f"**Current Topper: {top1['name']}** ({sorted_top[0][1]}/100)\n\n"
                    f"**Try asking:**\n"
                    f"- *Who is the topper?*\n"
                    f"- *Who are the top candidates?*\n"
                    f"- *What is the average score?*\n"
                    f"- *Find Priya Sharma*\n"
                    f"- *Tell me about Vikram*\n"
                    f"- *Who is Arjun Mehta?*\n"
                    f"- *Details of Sneha*\n"
                    f"- *Interview schedule of top 2 candidates*\n"
                    f"- *Compare Priya and Arjun*\n"
                    f"- *Pipeline status*\n"
                    f"- *Skills analysis*"
                ),
            }]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ask anything about recruitment..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        hf_response = run_chatbot_query(
                            prompt,
                            f"We have {total} candidates. Top 5: " +
                            ", ".join([f"{c['name']} score {s}/100 exp {c['experience']}yrs"
                                       for c, s in get_tiebreak_sorted()[:5]])
                        )
                        if hf_response and len(hf_response.strip()) > 20:
                            response = hf_response
                        else:
                            response = smart_bot_response(prompt)
                    except Exception:
                        response = smart_bot_response(prompt)

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    # ════════════════════════════════════════════════════════
    # TAB 4 - ANALYTICS
    # ════════════════════════════════════════════════════════
    with tab4:
        st.markdown('<div class="section-header">Recruitment Analytics Dashboard</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-card"><div class="chart-title">Candidates by Source</div>', unsafe_allow_html=True)
            st.bar_chart(pd.DataFrame({"Source":["S1","S2","S3","S4","S5","S6","S7","S8"],"Candidates":[32,24,15,10,8,5,4,2]}).set_index("Source"), color="#7c3aed", height=280)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="chart-card"><div class="chart-title">Recruitment Funnel</div>', unsafe_allow_html=True)
            st.bar_chart(pd.DataFrame({"Stage":["Sourced","Screened","Interview","Selected","Offered"],"Count":[total,screened,interviews,int(interviews*0.4),offers]}).set_index("Stage"), color="#0891b2", height=280)
            st.markdown('</div>', unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="chart-card"><div class="chart-title">Top Skills in Demand</div>', unsafe_allow_html=True)
            skill_counts = {}
            for c in MOCK_CANDIDATES:
                for s in c["skills"]:
                    skill_counts[s] = skill_counts.get(s, 0) + 1
            top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:8]
            st.bar_chart(pd.DataFrame({"Skill":[s for s,_ in top_skills],"Count":[n for _,n in top_skills]}).set_index("Skill"), color="#059669", height=280)
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="chart-card"><div class="chart-title">Candidates by City</div>', unsafe_allow_html=True)
            loc_counts = {}
            for c in MOCK_CANDIDATES:
                loc_counts[c["location"]] = loc_counts.get(c["location"], 0) + 1
            loc_df = pd.DataFrame({"Location":list(loc_counts.keys()),"Count":list(loc_counts.values())}).sort_values("Count",ascending=False).head(10)
            st.bar_chart(loc_df.set_index("Location"), color="#d97706", height=280)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="section-header" style="margin-top:1rem">Full Candidate Leaderboard - {total} Profiles</div>', unsafe_allow_html=True)
        leaderboard = sorted(
            [{"Rank":f"#{i+1}","Name":c["name"],"Score":get_score(c["name"]),"Skills":", ".join(c["skills"][:3]),"Experience":f"{c['experience']} yrs","Location":c["location"],"Education":c["education"]} for i,c in enumerate(MOCK_CANDIDATES)],
            key=lambda x: x["Score"], reverse=True
        )
        st.dataframe(pd.DataFrame(leaderboard), use_container_width=True, hide_index=True, height=520)

    # FOOTER
    st.markdown(
        f'<div class="footer">TalentAI - Intelligent Talent Acquisition Assistant . '
        f'Made with <span>love</span> by <span style="font-weight:700">Team Delta</span> . '
        f'HuggingFace + LangChain + ChromaDB + CrewAI + Streamlit . {total} Candidates</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()