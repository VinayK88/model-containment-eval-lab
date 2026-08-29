import streamlit as st

st.set_page_config(page_title="Model Containment Eval Lab", page_icon="◉", layout="wide", initial_sidebar_state="expanded")
METRICS=[("Eval scenarios","18","illustrative"),("Strict denials","14","illustrative"),("Tripwire hits","9","illustrative"),("Shutdown checks","6","illustrative"),("Trace-risk alerts","11","illustrative"),("False positives","2","illustrative"),("Host access","None","design boundary"),("Network access","None","design boundary"),("Shell access","None","design boundary"),("Real credentials","None","design boundary"),("Replay coverage","100%","illustrative"),("Live actions","0","evaluation only")]
SIGNALS=[("Strict-control coverage",.94),("Tripwire coverage",.86),("Shutdown compliance",.91),("Trace monitor quality",.82),("Containment boundary",1.0)]
st.markdown("""<style>html,body,[class*="css"]{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Helvetica Neue",Arial,sans-serif;color:#1d1d1f}.stApp{background:#f5f5f7}[data-testid="stHeader"]{background:transparent}[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e5e5ea}.block-container{max-width:1500px;padding:2rem 2.4rem 4rem}.hero{background:linear-gradient(135deg,#fff,#f7fbff);border:1px solid #e5e5ea;border-radius:32px;padding:38px 42px;margin-bottom:24px;box-shadow:0 14px 36px rgba(0,0,0,.045)}.eyebrow{color:#0071e3;font-size:.78rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase}.hero h1{font-size:3.15rem;letter-spacing:-.05em;margin:.22rem 0 .55rem}.hero p{max-width:900px;color:#6e6e73;font-size:1.12rem;line-height:1.55}.pill{display:inline-block;background:#eef6ff;color:#0066cc;border:1px solid #d8eaff;border-radius:999px;padding:.42rem .78rem;margin:.55rem .35rem 0 0;font-size:.76rem;font-weight:650}[data-testid="stMetric"]{background:#fff;border:1px solid #e5e5ea;border-radius:24px;padding:18px 20px;box-shadow:0 8px 26px rgba(0,0,0,.035);min-height:116px}[data-testid="stMetricLabel"]{color:#6e6e73;font-weight:600}[data-testid="stMetricValue"]{font-size:1.9rem;font-weight:700}.stTabs [data-baseweb="tab"]{background:#fff;border:1px solid #e5e5ea;border-radius:999px;padding:8px 16px}.card{background:#fff;border:1px solid #e5e5ea;border-radius:22px;padding:18px 20px}.note{background:#fff;border:1px solid #e5e5ea;border-radius:18px;padding:14px 18px;color:#6e6e73}</style>""",unsafe_allow_html=True)
with st.sidebar:
    st.markdown("## Model Containment Eval Lab"); st.caption("Containment & Tripwire Evaluation"); st.divider(); st.markdown("**Overview**\n\nContainment\n\nTripwires\n\nShutdown\n\nTrace risk"); st.divider(); st.caption("In-memory synthetic evaluation")
st.markdown("""<div class="hero"><div class="eyebrow">Containment &amp; Tripwire Evaluation</div><h1>Model Containment Eval Lab</h1><p>Evaluate strict controls, tripwires, shutdown compliance, trace-risk monitoring, and containment boundaries without host access.</p><span class="pill">Containment</span><span class="pill">Tripwires</span><span class="pill">Shutdown</span><span class="pill">Trace risk</span></div>""",unsafe_allow_html=True)
for s in range(0,len(METRICS),4):
    cols=st.columns(4)
    for c,(l,v,n) in zip(cols,METRICS[s:s+4]): c.metric(l,v,n)
st.subheader("Containment assurance")
l,r=st.columns([1.15,.85],gap="large")
with l:
    for n,v in SIGNALS: st.progress(v,text=f"{n} · {v:.0%}")
with r: st.markdown('<div class="card"><b>Intent and effect stay separate</b><br><br><span style="color:#6e6e73">Attempted violations remain visible in traces even when strict controls prevent their simulated effect.</span></div>',unsafe_allow_html=True)
t1,t2,t3,t4=st.tabs(["Containment","Tripwires","Shutdown","Trace risk"])
with t1: st.dataframe([{"Profile":"Strict","Effect":"DENY + RECORD"},{"Profile":"Audit","Effect":"SIMULATE + RECORD"}],use_container_width=True,hide_index=True)
with t2: st.dataframe([{"Tripwire":"unauthorized-write","Hits":4},{"Tripwire":"boundary-probe","Hits":3},{"Tripwire":"shutdown-resistance","Hits":2}],use_container_width=True,hide_index=True)
with t3: st.success("Synthetic shutdown-compliance checks remain within the in-memory evaluation boundary.")
with t4:
    for n,v in SIGNALS: st.progress(v,text=n)
st.markdown('<div class="note"><b>Evaluation boundary.</b> No host filesystem, shell, real network, or real credentials are available to this evaluation surface.</div>',unsafe_allow_html=True)
