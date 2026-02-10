import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import date
from moviepy.editor import VideoFileClip
import librosa

# ---------------- CONFIG ----------------
st.set_page_config("Eloquence AI", layout="centered")

DATA_PATH = "data/scores.xlsx"
VIDEO_DIR = "uploads/videos"
os.makedirs("data", exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# ---------------- UI ----------------
st.title("🎤 Eloquence AI – Public Speaking Evaluation")

with st.form("upload_form"):
    name = st.text_input("Speaker Name")
    eval_date = st.date_input("Date", value=date.today())
    theme = st.selectbox(
        "Speech Theme",
        ["Head (Informative)", "Heart (Inspirational)", "Hilarious (Funny)"]
    )
    video_file = st.file_uploader("Upload Speech Video (.mp4)", type=["mp4"])
    submit = st.form_submit_button("Analyze Speech")

# ---------------- PROCESS ----------------
if submit and name and video_file:

    video_path = os.path.join(VIDEO_DIR, video_file.name)
    with open(video_path, "wb") as f:
        f.write(video_file.read())

    st.info("Processing video...")

    # Extract audio
    clip = VideoFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".wav")
    clip.audio.write_audiofile(audio_path, logger=None)

    # Load audio
    y, sr = librosa.load(audio_path, sr=None)

    # Duration
    duration_sec = int(librosa.get_duration(y=y, sr=sr))
    duration_min = max(1, duration_sec // 60)

    # Speech detection
    rms = librosa.feature.rms(y=y)[0]
    speech_ratio = int(np.mean(rms > np.percentile(rms, 25)) * 100)

    if speech_ratio < 10:
        clarity = engagement = structure = theme_bonus = 0
        base_score = final_score = 0
        st.error("No meaningful speech detected.")

    else:
        # Speech metrics
        word_estimate = duration_sec * 2.5
        pitch = librosa.yin(y, fmin=80, fmax=300)
        pitch_var = int(np.nanstd(pitch))

        raw_clarity = int(word_estimate // 30)
        raw_engagement = int(pitch_var // 20)
        raw_structure = int(duration_sec // 30)

        clarity = min(10, max(5, raw_clarity))
        engagement = min(10, max(5, raw_engagement))
        structure = min(10, max(5, raw_structure))

        theme_bonus = (
            10 if theme.startswith("Heart")
            else 5 if theme.startswith("Hilarious")
            else 0
        )

        base_score = clarity + engagement + structure + theme_bonus  # /40
        final_score = base_score * duration_min

    # ---------------- SAVE ----------------
    row = {
        "Name": name,
        "Date": eval_date,
        "Theme": theme,
        "Duration (sec)": duration_sec,
        "Duration (min)": duration_min,
        "Speech Ratio (%)": speech_ratio,
        "Clarity": clarity,
        "Engagement": engagement,
        "Structure": structure,
        "Theme Bonus": theme_bonus,
        "Base Score (out of 40)": base_score,
        "Final Score": final_score,
        "Video File": video_file.name
    }

    if os.path.exists(DATA_PATH):
        df = pd.read_excel(DATA_PATH)
    else:
        df = pd.DataFrame(columns=row.keys())

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_excel(DATA_PATH, index=False)

    # ---------------- DISPLAY ----------------
    st.success(
        f"Final Score: {final_score} "
        f"(Base: {base_score}/40 × {duration_min} min)"
    )

    st.dataframe(pd.DataFrame([row]))

# ---------------- DOWNLOAD ----------------
if os.path.exists(DATA_PATH):
    st.divider()
    with open(DATA_PATH, "rb") as f:
        st.download_button(
            "📥 Download All Scores",
            data=f,
            file_name="eloquence_scores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
