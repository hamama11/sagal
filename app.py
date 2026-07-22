import streamlit as st

st.set_page_config(page_title="경제수학 · 수열과 금융", layout="wide")

st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(135deg, #0c4a6e, #0f766e);
        padding: 1.5rem 1.6rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1rem;
    }
    .card {
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 1rem;
        padding: 1rem;
        background: #f8fafc;
        height: 100%;
    }
    .section-label {
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #0f766e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1 style="margin-bottom: 0.2rem;">경제수학 · 수열과 금융</h1>
        <p style="margin: 0;">학생이 자신의 진로와 노후를 연결하며 수열·금융 개념을 탐구하는 인터랙티브 학습 페이지</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("이번 수업에서 학생들이 탐구할 핵심 질문")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <div class="section-label">도입</div>
            <h3>왜 돈의 가치가 변할까?</h3>
            <p>물가상승과 소비자물가 지수를 통해 화폐의 시간가치 개념을 발견합니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <div class="section-label">탐구</div>
            <h3>연금의 수학은 무엇을 말할까?</h3>
            <p>현재가치, 미래가치, 매년 납입액을 직접 바꾸며 수열과 금융의 관계를 비교합니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <div class="section-label">정리</div>
            <h3>나의 노후 설계는 어떻게?</h3>
            <p>은퇴 필요액과 개인연금 목표를 세우고, 수익과 생활비의 균형을 이해합니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.subheader("학습 페이지 이동")

if st.button("1단계 · 도입: 화폐의 시간가치", use_container_width=True):
    st.switch_page("pages/01_도입.py")

if st.button("2단계 · 탐구: 연금과 미래가치", use_container_width=True):
    st.switch_page("pages/02_연금과_미래가치.py")

if st.button("3단계 · 정리: 실전 재무 설계", use_container_width=True):
    st.switch_page("pages/03_노후_설계.py")

st.info("각 페이지는 수업 흐름에 맞춰 단계별로 구성되어 있으며, 학생이 질문을 던지고 계산을 직접 바꾸며 생각을 확장할 수 있게 설계했습니다.")
