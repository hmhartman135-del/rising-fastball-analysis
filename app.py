import pandas as pd
import streamlit as st

st.set_page_config(page_title="Rising Fastball Analysis", layout="wide")
st.title("Does the rising fastball win?")
st.caption("High-ride four-seamers vs. other four-seamers vs. sinkers/two-seamers, 2025 Statcast")


@st.cache_data
def load():
    return pd.read_csv("fastballs.csv.gz")


df = load()

# ---- Filters ----
with st.sidebar:
    st.header("Filters")
    hand = st.radio("Batter handedness", ["Both", "R", "L"], horizontal=True)
    two_strikes = st.checkbox("Two-strike counts only")
    pitchers = ["All"] + sorted(df["player_name"].dropna().unique())
    pitcher = st.selectbox("Pitcher", pitchers)

f = df.copy()
if hand != "Both":
    f = f[f["stand"] == hand]
if two_strikes:
    f = f[f["strikes"] == 2]
if pitcher != "All":
    f = f[f["player_name"] == pitcher]

# ---- Summary table ----
def summarize(g):
    swings = g["swing"].sum()
    ooz = g["out_of_zone"].sum()
    pas = g["pa_end"].sum()
    return pd.Series({
        "Pitches": len(g),
        "Avg velo (mph)": g["release_speed"].mean(),
        "Avg IVB (in)": g["ivb_in"].mean(),
        "Whiff %": 100 * g["whiff"].sum() / swings if swings else None,
        "Chase %": 100 * g["chase"].sum() / ooz if ooz else None,
        "K % (PA ending on pitch)": 100 * g["strikeout"].sum() / pas if pas else None,
    })

summary = f.groupby("group").apply(summarize).round(1)
st.subheader("Results by fastball type")
st.dataframe(summary, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Whiff % by type")
    st.bar_chart(summary["Whiff %"])
with c2:
    st.subheader("Chase % by type")
    st.bar_chart(summary["Chase %"])

# ---- Movement plot ----
st.subheader("Pitch movement (sample)")
sample = f.sample(min(len(f), 5000), random_state=1)
st.scatter_chart(sample, x="hb_in", y="ivb_in", color="group")
st.caption("Horizontal break vs. induced vertical break, in inches (catcher's view).")
