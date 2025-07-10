import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

# --- 페이지 설정 ---
st.set_page_config(page_title="감정일기", layout="centered")

# --- 비밀번호 체크 상태 저장 ---
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if not st.session_state.unlocked:
    st.markdown("<h1 style='color:#497325;'>🔐 감정일기 잠금 해제</h1>", unsafe_allow_html=True)
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if password == "1234":
        st.session_state.unlocked = True
        st.experimental_rerun()  # 잠금 해제 직후 새로고침
    else:
        st.warning("비밀번호를 입력하면 감정일기를 작성할 수 있어요.")
        st.stop()

# --- 여기부터는 잠금 해제된 후만 실행됨 ---
st.success("접속되었습니다! 🎉")

emotions = {
    "😊 기쁨": "#a8c98c",
    "😢 슬픔": "#d0e1f9",
    "😠 화남": "#f9d0d0",
    "😱 불안": "#f9ecd0",
    "😍 설렘": "#f9d0f0",
    "😶 무덤덤": "#e0e0e0",
    "😴 피곤함": "#d0f0f9",
    "😷 몸이 안좋음": "#e2f0d0",
    "😳 민망": "#f0d9f9",
    "😇 감사함": "#f0f9d0",
    "🫥 무기력": "#dcdcdc",
    "😬 어색함": "#f5e6cc",
    "😌 편안함": "#d0f9e2",
    "😭 울컥함": "#f0d0d0",
    "🤩 신남": "#e0d0f9",
    "🤔 복잡함": "#cfd8dc"
}

selected = st.radio("오늘 기분은 어땠나요?", list(emotions.keys()), horizontal=True)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {emotions[selected]};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"<div style='background-color:{emotions[selected]}; padding: 0.5em; border-radius: 6px;'>"
    f"<strong>{selected}</strong> 상태로 일기를 작성해보세요.</div>",
    unsafe_allow_html=True
)

st.markdown("### 오늘 있었던 일을 적어보세요")
note = st.text_area("✏️ 오늘의 일기", height=200)

if st.button("💾 저장하기"):
    if note.strip() == "":
        st.warning("일기를 입력해주세요!")
    else:
        today = date.today().isoformat()
        new_entry = pd.DataFrame([[today, selected, note]], columns=["날짜", "감정", "일기"])

        try:
            diary = pd.read_csv("diary.csv")
            diary = pd.concat([diary, new_entry], ignore_index=True)
        except FileNotFoundError:
            diary = new_entry

        diary.to_csv("diary.csv", index=False)
        st.success("감정일기가 저장되었습니다! 💚")

st.markdown("### 📊 감정 비율")
try:
    diary = pd.read_csv("diary.csv")
    counts = diary["감정"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)
    st.pyplot(fig)
except:
    st.info("아직 저장된 일기가 없어요.")

st.markdown("### 📂 날짜별 일기 보기")
try:
    dates = diary["날짜"].unique()[::-1]
    for d in dates:
        with st.expander(f"📅 {d}"):
            for _, row in diary[diary["날짜"] == d].iterrows():
                st.markdown(f"**{row['감정']}** - {row['일기']}")
except:
    pass
