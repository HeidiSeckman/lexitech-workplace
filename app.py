import streamlit as st
import streamlit.components.v1 as components
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
.stApp { background-color: #FFFFFF; background-image: radial-gradient(#E8C5D6 0.85px, transparent 0.85px); background-size: 22px 22px; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #FDF2F7 0%, #F9E6F0 100%); border-right: 1px solid #E5B8CE; }
.mono-tag { font-family: 'JetBrains Mono', monospace !important; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 0.08em; color: #B81D6F !important; text-transform: uppercase; }
.nav-bar { background: rgba(255, 255, 255, 0.94); border: 1.5px solid #E5B8CE; border-radius: 14px; padding: 14px 22px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 20px rgba(184, 29, 111, 0.07); }
.status-pill { background: #FDF2F7; border: 1px solid #B81D6F; border-radius: 999px; padding: 6px 14px; font-family: 'JetBrains Mono', monospace !important; font-size: 11px !important; font-weight: 700 !important; color: #B81D6F !important; }
.hero-box { background: linear-gradient(135deg, #24101C 0%, #4A1533 55%, #881652 100%); border-radius: 18px; padding: 20px 28px 24px; margin-bottom: 16px; box-shadow: 0 12px 32px rgba(184, 29, 111, 0.22); }
.hero-box h1, .hero-box p, .hero-box span { color: #FFFFFF !important; }
[data-testid="stVerticalBlockBorderWrapper"] { background: #FFFFFF !important; border: 2px solid #E5B8CE !important; border-top: 5px solid #B81D6F !important; border-radius: 18px !important; padding: 18px 22px !important; box-shadow: 0 14px 36px rgba(184, 29, 111, 0.10) !important; }
.stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input, [data-testid="stFileUploaderDropzone"] { background-color: #FDF2F7 !important; color: #1A161F !important; border: 1.5px solid #E5B8CE !important; border-radius: 12px !important; padding: 10px 14px !important; }
[data-testid="stAlert"], [data-testid="stAlertContainer"], .stSpinner > div { background-color: #FDF2F7 !important; color: #1A161F !important; border: 1.5px solid #B81D6F !important; border-radius: 10px !important; }
div.stButton > button, div.stDownloadButton > button, [data-testid="stFileUploaderDropzone"] button { background: linear-gradient(135deg, #E11D74 0%, #9D174D 55%, #581C87 100%) !important; color: #FFFFFF !important; border: 1.5px solid #F9A8D4 !important; border-radius: 999px !important; padding: 13px 34px !important; min-height: 48px !important; font-size: 15px !important; font-weight: 700 !important; letter-spacing: 0.03em !important; box-shadow: 0 8px 22px rgba(225, 29, 116, 0.28) !important; transition: all 0.2s ease !important; }
div.stButton > button:hover, div.stDownloadButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 28px rgba(225, 29, 116, 0.45) !important; }
button *, div.stButton > button *, div.stDownloadButton > button *, [data-testid="stFileUploaderDropzone"] button * { color: #FFFFFF !important; }
[data-testid="stTextInput"] button { background: #B81D6F !important; border: none !important; border-radius: 8px !important; padding: 6px 10px !important; min-height: auto !important; }
[data-testid="stTextInput"] button svg { fill: #FFFFFF !important; }
[data-testid="stRadio"] > div { display: flex !important; gap: 12px !important; width: 100% !important; }
[data-testid="stRadio"] label { flex: 1 !important; justify-content: center !important; background: #FDF2F7 !important; border: 1.5px solid #E5B8CE !important; border-radius: 12px !important; padding: 12px 18px !important; font-weight: 700 !important; cursor: pointer !important; }
[data-testid="stRadio"] label:has(input:checked) { background: linear-gradient(135deg, #D91E7A 0%, #88134D 100%) !important; border-color: #B81D6F !important; box-shadow: 0 4px 14px rgba(184, 29, 111, 0.28) !important; }
[data-testid="stRadio"] label:has(input:checked) p { color: #FFFFFF !important; }
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

GLOBE_3D = """
<div style="background:linear-gradient(135deg,#24101C 0%,#4A1533 55%,#881652 100%);border-radius:18px;padding:18px 24px 22px;text-align:center;box-shadow:0 12px 32px rgba(184,29,111,0.22);font-family:system-ui,-apple-system,sans-serif;color:#FFFFFF;">
  <canvas id="globe" width="140" height="140" style="display:block;margin:0 auto 6px;filter:drop-shadow(0 0 16px rgba(255,42,133,0.85));"></canvas>
  <div style="font-family:monospace;font-size:11px;letter-spacing:0.12em;color:#F9A8D4;font-weight:700;">CLOUD-SAVED LEGAL &amp; TAX WORKSPACE</div>
  <h1 style="margin:6px 0;font-size:25px;font-weight:800;color:#FFFFFF;">Welcome to LexiTech Vault</h1>
  <p style="margin:0;font-size:13.5px;color:#FCE7F3;">Sign in or create a free account to save case folders and run all 4 forensic AI engines.</p>
</div>
<script>
const g = document.getElementById('globe'), ctx = g.getContext('2d');
let rot = 0;
const dots = [];
for (let lat = -80; lat <= 80; lat += 20) {
  for (let lon = 0; lon < 360; lon += 20) {
    const phi = lat * Math.PI / 180, theta = lon * Math.PI / 180;
    dots.push({ x: Math.cos(phi)*Math.cos(theta), y: Math.sin(phi), z: Math.cos(phi)*Math.sin(theta) });
  }
}
function spin() {
  ctx.clearRect(0, 0, 140, 140);
  rot += 0.018;
  dots.forEach(d => {
    const x = d.x * Math.cos(rot) - d.z * Math.sin(rot);
    const z = d.x * Math.sin(rot) + d.z * Math.cos(rot);
    const scale = 56 / (2.4 - z);
    const px = 70 + x * scale * 2.1, py = 70 + d.y * scale * 2.1;
    const alpha = Math.max(0.2, (z + 1) / 2);
    ctx.fillStyle = `rgba(255, 105, 180, ${alpha})`;
    ctx.beginPath(); ctx.arc(px, py, z > 0 ? 2.1 : 1.1, 0, Math.PI * 2); ctx.fill();
  });
  requestAnimationFrame(spin);
}
spin();
</script>
"""

SB_URL = st.secrets["SUPABASE_URL"].strip().rstrip("/")
SB_KEY = "".join(st.secrets["SUPABASE_KEY"].split())
sb = create_client(SB_URL, SB_KEY)

if "sb_session" in st.session_state and st.session_state["sb_session"]:
    try:
        sb.auth.set_session(st.session_state["sb_session"].access_token, st.session_state["sb_session"].refresh_token)
    except Exception:
        pass

if "user" not in st.session_state:
    st.markdown(f'<div class="nav-bar">{LOGO_SVG}<div class="status-pill">● SECURE MATTER VAULT // v2.0</div></div>', unsafe_allow_html=True)
    _, mid, _ = st.columns((1, 1.35, 1))
    with mid:
        components.html(GLOBE_3D, height=265)
        with st.container(border=True):
            mode = st.radio("Access Mode", ("Member Login", "Create Account"), horizontal=True, label_visibility="collapsed")
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            if mode == "Member Login":
                em = st.text_input("Email Address", placeholder="you@example.com", key="in_em")
                pw = st.text_input("Password", type="password", placeholder="••••••••", key="in_pw")
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                if st.button("Unlock LexiTech Workspace", key="btn_in", use_container_width=True):
                    try:
                        res = sb.auth.sign_in_with_password({"email": em.strip(), "password": pw})
                        st.session_state["user"] = res.user
                        st.session_state["sb_session"] = res.session
                        st.rerun()
                    except Exception as e:
                        st.error(f"Login failed ({SB_URL}): {e}")
            else:
                em2 = st.text_input("Email Address", placeholder="you@example.com", key="up_em")
                pw2 = st.text_input("Create Password (min 6 chars)", type="password", placeholder="••••••••", key="up_pw")
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                if st.button("Launch My Free Workspace", key="btn_up", use_container_width=True):
                    try:
                        res = sb.auth.sign_up({"email": em2.strip(), "password": pw2})
                        if not res.session:
                            res = sb.auth.sign_in_with_password({"email": em2.strip(), "password": pw2})
                        st.session_state["user"] = res.user
user = st.session_state["user"]
projs = sb.table("projects").select("*").order("created_at", desc=True).execute().data or []

with st.sidebar:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.caption(f"Signed in as **{user.email}**")
    if st.button("Sign Out", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.markdown("---")
    st.markdown('<div class="mono-tag">SAVED CASE FOLDERS</div>', unsafe_allow_html=True)
    with st.expander("➕ New Project / Matter", expanded=(len(projs) == 0)):
        new_title = st.text_input("Folder Name", placeholder="e.g., Studio Lease Audit")
        new_client = st.text_input("Client / Notes", placeholder="e.g., 2026 Contract Review")
        if st.button("Create Folder", use_container_width=True) and new_title:
            sb.table("projects").insert({"user_id": user.id, "title": new_title, "client_or_matter": new_client}).execute()
            st.rerun()

    active_proj = None
    if projs:
        titles = [f"📂 {p['title']}" for p in projs]
        pick = st.selectbox("Active Project on File:", titles)
        active_proj = projs[titles.index(pick)]
    st.markdown("---")
    st.markdown('<div class="mono-tag">AI ENGINE KEY</div>', unsafe_allow_html=True)
    byo_key = st.text_input("Optional Custom Gemini Key", type="password", placeholder="Leave blank for Starter Credits")
    active_key = byo_key or "".join(st.secrets.get("GEMINI_API_KEY", "").split())

st.markdown(f'<div class="nav-bar">{LOGO_SVG}<div class="status-pill">● VAULT ONLINE // {len(projs)} SAVED FOLDERS</div></div>', unsafe_allow_html=True)

if not active_proj:
    st.info("Create your first **Project / Case Folder** in the left sidebar to unlock all 4 AI engines and save reports on file!")
    st.stop()

saved_reps = sb.table("reports").select("*").eq("project_id", active_proj["id"]).order("created_at", desc=True).execute().data or []
st.markdown(f'<div class="hero-box"><span style="font-family:\'JetBrains Mono\',monospace;font-size:11px;">ACTIVE MATTER ON FILE // {len(saved_reps)} SAVED AUDITS</span><h1 style="margin:4px 0 4px;font-size:28px;">{active_proj["title"]}</h1><p style="margin:0;font-size:14px;">{active_proj.get("client_or_matter") or "LexiTech Cloud Matter Folder"}</p></div>', unsafe_allow_html=True)

view_mode = st.radio("Workspace View", ("⚡ Run 4-Engine AI Suite", f"🗄️ Saved Reports on File ({len(saved_reps)})"), horizontal=True, label_visibility="collapsed")
st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

if view_mode.startswith("⚡"):
    tool = st.selectbox("Select Workspace Engine:", (
        "Tool 01 // Legal & Tax Document Researcher",
        "Tool 02 // Dual-Corpus Tax-Trap Scanner",
        "Tool 03 // Worst-Case Life Event Simulator",
        "Tool 04 // Negotiation Email & Counter-Proposal Drafter"
    ))
    doc_a = st.file_uploader("Upload Primary Contract / Document (PDF)", type="pdf", key="wa")
    doc_b = st.file_uploader("Optional Second Document (e.g., IRS Manual PDF for Tool 02)", type="pdf", key="wb")
    prompt_in = st.text_area("Instructions, Crisis Scenarios, or Negotiation Context:", placeholder="Describe what to audit, which life event to simulate, or what redline to draft into a negotiation email...")

    if st.button("Run Engine & Save to Folder"):
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
        st.success("Saved directly to your cloud case folder!")
        st.markdown(st.session_state["last_out"])

else:
    if not saved_reps:
        st.info("No reports saved in this folder yet—run any tool in the first view to save it permanently here!")
    else:
        full_dossier = f"LEXITECH MASTER CASE DOSSIER: {active_proj['title']}\n{'='*60}\n\n"
        for r in saved_reps:
            full_dossier += f"--- {r['tool_name']} ({r['created_at'][:10]}) ---\n{r['content']}\n\n"
            with st.expander(f"{r['tool_name']}  •  Saved {r['created_at'][:10]}", expanded=True):
                st.markdown(r["content"])
        st.download_button("Export Full Master Case Dossier (.txt)", data=full_dossier, file_name=f"LexiTech_Dossier_{active_proj['title'].replace(' ', '_')}.txt", mime="text/plain")

st.markdown('<div class="lexitech-footer"><strong>© 2026 LexiTech by Heidi Seckman. All Rights Reserved.</strong><br>Proprietary software, interface design, and branding. For educational and research assistance only; not formal legal, financial, or tax advice.</div>', unsafe_allow_html=True)
