# Does the Rising Fastball Win?

**Question:** Do high-ride four-seam fastballs (the "rising fastball" approach popularized by teams like the Astros) produce more strikeouts and chases than sinkers and two-seamers? Does the answer change by batter handedness or count?

**Live dashboard:** _link coming soon_

## Data
- 2025 MLB regular-season Statcast pitch data, pulled with [pybaseball](https://github.com/jldbc/pybaseball)
- Fastballs only: four-seam (FF), sinker (SI), two-seam (FT)
- "High-ride" four-seamers = induced vertical break of 18+ inches

## Method
- Grouped pitches into high-ride four-seam, other four-seam, and sinker/two-seam
- Compared whiff rate (whiffs / swings), chase rate (swings on out-of-zone pitches / out-of-zone pitches), and strikeout rate on plate appearances ending with that pitch
- Split results by batter handedness and two-strike counts

## Findings
_To be added._

## Next steps
- Control for velocity and location (e.g. logistic regression on whiff probability)
- Split by hitter type (pull vs. spray hitters)
- Pitcher-level estimates with a hierarchical model to handle small samples

## Files
| File | Purpose |
|---|---|
| `prep_data.py` | Pulls Statcast data and builds `fastballs.csv` |
| `app.py` | Streamlit dashboard |
| `requirements.txt` | Libraries needed to run the app |

## Run locally
```
pip3 install -r requirements.txt
streamlit run app.py
```

*Henry Hartman, Mechanical Engineering, TCU*
