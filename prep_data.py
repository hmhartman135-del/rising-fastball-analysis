"""
Pull Statcast data and save a small, cleaned CSV for the dashboard.
Run this once (in Colab or locally), then upload fastballs.csv to the repo.
"""
import pandas as pd
from pybaseball import statcast, cache

cache.enable()

# One season of regular-season pitches (takes a few minutes the first time)
df = statcast(start_dt="2025-03-27", end_dt="2025-09-28")

# Keep fastballs only: four-seam (FF), sinker (SI), two-seam (FT)
df = df[df["pitch_type"].isin(["FF", "SI", "FT"])].copy()
# A few pitches are missing movement data; drop them so grouping works
df = df.dropna(subset=["pfx_x", "pfx_z"])

# Movement in inches (Statcast stores feet)
df["ivb_in"] = df["pfx_z"] * 12
df["hb_in"] = df["pfx_x"] * 12

# Group pitches: high-ride four-seamers vs. the rest
HIGH_RIDE_IN = 18  # induced vertical break threshold, adjust as you like
def group(row):
    if row["pitch_type"] == "FF":
        return "High-ride 4-seam" if row["ivb_in"] >= HIGH_RIDE_IN else "Other 4-seam"
    return "Sinker / 2-seam"
df["group"] = df.apply(group, axis=1)

# Outcome flags
swing_desc = {"swinging_strike", "swinging_strike_blocked", "foul", "foul_tip",
              "hit_into_play", "foul_bunt", "missed_bunt"}
whiff_desc = {"swinging_strike", "swinging_strike_blocked", "missed_bunt"}
df["swing"] = df["description"].isin(swing_desc).astype(int)
df["whiff"] = df["description"].isin(whiff_desc).astype(int)
df["out_of_zone"] = (df["zone"] > 9).astype(int)
df["chase"] = ((df["out_of_zone"] == 1) & (df["swing"] == 1)).astype(int)
df["pa_end"] = df["events"].notna().astype(int)
df["strikeout"] = df["events"].isin(["strikeout", "strikeout_double_play"]).astype(int)

cols = ["player_name", "pitch_type", "group", "stand", "release_speed",
        "ivb_in", "hb_in", "plate_x", "plate_z", "balls", "strikes",
        "swing", "whiff", "out_of_zone", "chase", "pa_end", "strikeout"]
# Compressed so it fits GitHub's 25 MB browser-upload limit
df[cols].to_csv("fastballs.csv.gz", index=False, compression="gzip")
print(f"Saved {len(df):,} pitches to fastballs.csv.gz")
