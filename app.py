import streamlit as st
from google import genai
from google.genai import types
from supabase import create_client
from PIL import Image
import tempfile, os, base64, io

st.set_page_config(page_title="LexiTech Pro Workspace", page_icon="LEXItech.PNG", layout="wide")

st.markdown("""
<style>
@import url('https://googleapis.com');
html, body, .stApp, p, label, h1, h2, h3, h4, li { font-family: 'Plus Jakarta Sans', sans-serif !important; color: #1A161F !important; }
.stApp { background-color: #FFFFFF; background-image: radial-gradient(#E8C5D6 0.75px, transparent 0.75px); background-size: 22px 22px; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #FDF2F7 0%, #F9E6F0 100%); border-right: 1px solid #E5B8CE; }
.mono-tag { font-family: 'JetBrains Mono', monospace !important; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 0.08em; color: #B81D6F !important; text-transform: uppercase; }
.nav-bar { background: rgba(255, 255, 255, 0.94); border: 1.5px solid #E5B8CE; border-radius: 14px; padding: 14px 22px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 20px rgba(184, 29, 111, 0.07); }
.status-pill { background: #FDF2F7; border: 1px solid #B81D6F; border-radius: 999px; padding: 6px 14px; font-family: 'JetBrains Mono', monospace !important; font-size: 11px !important; font-weight: 700 !important; color: #B81D6F !important; }
.hero-box { background: linear-gradient(135deg, #24101C 0%, #4A1533 55%, #881652 100%); border-radius: 16px; padding: 24px 28px; margin-bottom: 20px; box-shadow: 0 10px 28px rgba(184, 29, 111, 0.16); }
.hero-box h1, .hero-box p, .hero-box span { color: #FFFFFF !important; }
.corpus-card { background: #FFFFFF; border: 1.5px solid #E5B8CE; border-top: 4px solid #B81D6F; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; }
.stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input, [data-testid="stFileUploaderDropzone"] { background-color: #FDF2F7 !important; color: #1A161F !important; border: 1.5px solid #E5B8CE !important; border-radius: 10px !important; }
[data-testid="stAlert"], [data-testid="stAlertContainer"], .stSpinner > div { background-color: #FDF2F7 !important; color: #1A161F !important; border: 1.5px solid #B81D6F !important; border-radius: 10px !important; }
button, .stButton > button, .stDownloadButton > button, [data-testid="stFileUploaderDropzone"] button, [data-testid="stTextInput"] button { background: linear-gradient(135deg, #B81D6F 0%, #8E1454 100%) !important; color: #FFFFFF !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; box-shadow: 0 4px 12px rgba(184, 29, 111, 0.22) !important; }
button *, .stButton > button *, .stDownloadButton > button *, [data-testid="stFileUploaderDropzone"] button *, [data-testid="stTextInput"] button * { color: #FFFFFF !important; }
[data-testid="stTextInput"] button svg { fill: #FFFFFF !important; }
.stTabs [data-baseweb="tab"] { background-color: #FDF2F7; border-radius: 8px 8px 0 0; padding: 8px 18px; border: 1px solid #E5B8CE; font-weight: 600; }
.stTabs [aria-selected="true"] { background: #B81D6F !important; }
.stTabs [aria-selected="true"] * { color: #FFFFFF !important; }
.lexitech-footer { background: #FDF2F7; border: 1px solid #E5B8CE; border-radius: 12px; padding: 14px 18px; text-align: center; font-size: 12.5px; margin-top: 28px; }
</style>
""", unsafe_allow_html=True)

logo_b64 = ""
if os.path.exists("LEXItech.PNG"):
    im = Image.open("LEXItech.PNG").convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    logo_b64 = base64.b64encode(buf.getvalue()).decode()

LOGO_SVG = f"""
<div style="display:flex;align-items:center;gap:14px;">
  <div style="background:linear-gradient(135deg,#FDF2F7 0%,#FFFFFF 100%);border:2px solid #E5B8CE;border-radius:16px;padding:7px;box-shadow:0 4px 14px rgba(184,29,111,0.14);display:flex;align-items:center;justify-content:center;">
    <img src="data:image/png;base64,{logo_b64}" style="width:74px;height:74px;object-fit:contain;" />
  </div>
  <div>
    <div style="font-weight:800;font-size:24px;letter-spacing:-0.02em;line-height:1.1;">LEXI<span style="color:#B81D6F;">TECH</span></div>
    <div class="mono-tag" style="font-size:11px !important;margin-top:2px;">PRO CLOUD WORKSPACE</div>
  </div>
</div>
"""

sb = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
if "sb_session" in st.session_state:
    try:
        sb.auth.set_session(st.session_state["sb_session"].access_token, st.session_state["sb_session"].refresh_token)
    except Exception:
        pass

if "user" not in st.session_state:
    st.markdown(f'<div class="nav-bar">{LOGO_SVG}<div class="status-pill">● SECURE MATTER VAULT // v2.0</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-box"><span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;">CLOUD-SAVED LEGAL &amp; TAX WORKSPACE</span><h1 style="margin:4px 0 6px;font-size:28px;">Sign In to Your LexiTech Vault</h1><p style="margin:0;font-size:14.5px;">Create a free account to organize client/personal case folders, run all 4 AI engines, and keep old audits permanently on file.</p></div>', unsafe_allow_html=True)
    t_in, t_up = st.tabs(("🔐 Log In", "✨ Create Free Account"))
    with t_in:
        em = st.text_input("Email", key="in_em")
        pw = st.text_input("Password", type="password", key="in_pw")
        if st.button("Log In to Workspace"):
            try:
                res = sb.auth.sign_in_with_password({"email": em, "password": pw})
                st.session_state["user"] = res.user
                st.session_state["sb_session"] = res.session
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")
    with t_up:
        em2 = st.text_input("Email", key="up_em")
        pw2 = st.text_input("Create Password (min 6 chars)", type="password", key="up_pw")
        if st.button("Create Free Account"):
            try:
                res = sb.auth.sign_up({"email": em2, "password": pw2})
                st.session_state["user"] = res.user
                st.session_state["sb_session"] = res.session
                st.rerun()
            except Exception as e:
                st.error(f"Sign-up failed: {e}")
    st.stop()
user = st.session_state["user"]
projs = sb.table("projects").select("*").order("created_at", desc=True).execute().data or []

with st.sidebar:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.caption(f"Signed in as **{user.email}**")
    if st.button("🚪 Sign Out"):
        st.session_state.clear()
        st.rerun()
    st.markdown("---")
    st.markdown('<div class="mono-tag">📁 SAVED CASE FOLDERS</div>', unsafe_allow_html=True)
    with st.expander("➕ New Project / Matter", expanded=(len(projs) == 0)):
        new_title = st.text_input("Folder Name", placeholder="e.g., Studio Lease Audit")
        new_client = st.text_input("Client / Notes", placeholder="e.g., 2026 Contract Review")
        if st.button("Create Folder") and new_title:
            sb.table("projects").insert({"user_id": user.id, "title": new_title, "client_or_matter": new_client}).execute()
            st.rerun()

    active_proj = None
    if projs:
        titles = [f"📂 {p['title']}" for p in projs]
        pick = st.selectbox("Active Project on File:", titles)
        active_proj = projs[titles.index(pick)]
    st.markdown("---")
    st.markdown('<div class="mono-tag">🔑 AI ENGINE KEY</div>', unsafe_allow_html=True)
    byo_key = st.text_input("Optional Custom Gemini Key", type="password", placeholder="Leave blank for Starter Credits")
    active_key = byo_key or st.secrets.get("GEMINI_API_KEY", "")

st.markdown(f'<div class="nav-bar">{LOGO_SVG}<div class="status-pill">● VAULT ONLINE // {len(projs)} SAVED FOLDERS</div></div>', unsafe_allow_html=True)

if not active_proj:
    st.info("👈 Create your first **Project / Case Folder** in the left sidebar to unlock all 4 AI engines and save reports on file!")
    st.stop()

saved_reps = sb.table("reports").select("*").eq("project_id", active_proj["id"]).order("created_at", desc=True).execute().data or []
st.markdown(f'<div class="hero-box"><span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;">ACTIVE MATTER ON FILE // {len(saved_reps)} SAVED AUDITS</span><h1 style="margin:4px 0 4px;font-size:28px;">{active_proj["title"]}</h1><p style="margin:0;font-size:14px;">{active_proj.get("client_or_matter") or "LexiTech Cloud Matter Folder"}</p></div>', unsafe_allow_html=True)

tab_run, tab_vault = st.tabs(("⚡ Run 4-Engine AI Suite", f"🗄️ Saved Reports on File ({len(saved_reps)})"))

with tab_run:
    tool = st.selectbox("Select Workspace Engine:", (
        "Tool 01 // Legal & Tax Document Researcher",
        "Tool 02 // Dual-Corpus Tax-Trap Scanner",
        "Tool 03 // Worst-Case Life Event Simulator",
        "Tool 04 // Negotiation Email & Counter-Proposal Drafter"
    ))
    doc_a = st.file_uploader("Upload Primary Contract / Document (PDF)", type="pdf", key="wa")
    doc_b = st.file_uploader("Optional Second Document (e.g., IRS Manual PDF for Tool 02)", type="pdf", key="wb")
    prompt_in = st.text_area("Instructions, Crisis Scenarios, or Negotiation Context:", placeholder="Describe what to audit, which life event to simulate, or what redline to draft into a negotiation email...")

    if st.button("🚀 Run Engine & Save to Folder"):
        if not active_key:
            st.warning("Add your Gemini API key in the sidebar (or configure GEMINI_API_KEY in Streamlit Secrets).")
        elif not doc_a and not prompt_in:
            st.warning("Upload a PDF or enter instructions/clause text to analyze.")
        else:
            with st.spinner(f"Running {tool} and saving to '{active_proj['title']}'..."):
                try:
                    client = genai.Client(api_key=active_key)
                    parts = [f"ACTIVE ENGINE: {tool}\nUSER REQUEST: {prompt_in or 'Perform a comprehensive forensic audit with exact citations and protective redlines.'}"]
                    for label, f_obj in (("PRIMARY DOCUMENT:", doc_a), ("SECONDARY REFERENCE:", doc_b)):
                        if f_obj:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                                tmp.write(f_obj.read())
                                p = tmp.name
                            parts.extend([label, client.files.upload(file=p)])
                            os.remove(p)
                    models = tuple(m.name.replace("models/", "") for m in client.models.list() if "gemini" in m.name and "flash" in m.name)
                    for m_name in models:
                        try:
                            res = client.models.generate_content(model=m_name, contents=parts, config=types.GenerateContentConfig(system_instruction="You are LexiTech Pro Workspace, a closed-book legal and tax AI suite. Ground all findings strictly in uploaded documents with exact section/page citations, draft balanced redlines, or write clear, polite negotiation emails."))
                            sb.table("reports").insert({"project_id": active_proj["id"], "user_id": user.id, "tool_name": tool, "content": res.text}).execute()
                            st.session_state["last_out"] = res.text
                            st.rerun()
                        except Exception:
                            continue
                except Exception as e:
                    st.error(f"Error: {e}")

    if "last_out" in st.session_state:
        st.success("✅ Saved directly to your cloud case folder!")
        st.markdown(st.session_state["last_out"])

with tab_vault:
    if not saved_reps:
        st.info("No reports saved in this folder yet—run any tool in the first tab to save it permanently here!")
    else:
        full_dossier = f"LEXITECH MASTER CASE DOSSIER: {active_proj['title']}\n{'='*60}\n\n"
        for r in saved_reps:
            full_dossier += f"--- {r['tool_name']} ({r['created_at'][:10]}) ---\n{r['content']}\n\n"
            with st.expander(f"📄 {r['tool_name']}  •  Saved {r['created_at'][:10]}", expanded=True):
                st.markdown(r["content"])
        st.download_button("📦 Export Full Master Case Dossier (.txt)", data=full_dossier, file_name=f"LexiTech_Dossier_{active_proj['title'].replace(' ', '_')}.txt", mime="text/plain")

st.markdown('<div class="lexitech-footer"><strong>© 2026 LexiTech by Heidi Seckman. All Rights Reserved.</strong><br>Proprietary software, interface design, and branding. For educational and research assistance only; not formal legal, financial, or tax advice.</div>', unsafe_allow_html=True)
