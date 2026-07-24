import math

import pandas as pd
import plotly.graph_objects as go
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
    .small-note {
        font-size: 0.9rem;
        color: #475569;
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
st.subheader("1. 도입: 화폐의 시간가치")

intro_col1, intro_col2 = st.columns(2)
with intro_col1:
    base_year = st.number_input("과거 연도", min_value=1940, max_value=2025, value=1990, step=1)
    base_money = st.number_input("과거 금액(원)", min_value=0, value=1_000_000, step=100_000)
    current_year = st.number_input("현재 연도", min_value=1940, max_value=2050, value=2025, step=1)

with intro_col2:
    cpi_index = {1990: 100, 2000: 112, 2010: 130, 2020: 148, 2025: 171}
    base_index = cpi_index.get(int(base_year), 100)
    current_index = cpi_index.get(int(current_year), cpi_index[2025])
    adjusted_value = base_money * (current_index / base_index)

    st.metric("현재 시점의 가치", f"{math.floor(adjusted_value):,}원")
    st.write(f"짜장면 2,000원 기준: 약 {math.floor(adjusted_value / 2000):,}그릇")
    st.write(f"스마트폰 1,200,000원 기준: 약 {math.floor(adjusted_value / 1_200_000):,}대")
    st.info("이 값은 현실적인 소비자물가 지수 데이터를 단순화한 예시입니다. 수업에서는 실제 지표를 추가로 비교해 보세요.")

years = [1990, 2000, 2010, 2020, 2025]
values = [100, 112, 130, 148, 171]
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=years,
        y=values,
        mode="lines+markers",
        name="소비자물가 지수",
        line=dict(color="#145c9f", width=3),
    )
)
fig.update_layout(title="소비자물가 지수 변화(샘플)", xaxis_title="연도", yaxis_title="지수")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("2. My-CPI 합성기")

categories = [
    "01. 식료품·비주류음료",
    "02. 주류·담배",
    "03. 의류·신발",
    "04. 주택·수도·광열",
    "05. 가정용품·가사서비스",
    "06. 보건",
    "07. 교통",
    "08. 통신",
    "09. 오락·문화",
    "10. 교육",
    "11. 음식·숙박",
    "12. 기타 상품·서비스",
]

national_weights = [142.4, 14.4, 52.1, 170.1, 38.2, 73.6, 113.6, 43.5, 56.7, 72.5, 129.8, 93.1]
example_indices = [122.5, 108.3, 115.0, 128.4, 112.1, 105.8, 118.2, 102.1, 114.5, 107.3, 124.6, 116.8]
default_my_weights = [150, 10, 40, 180, 30, 60, 100, 40, 90, 70, 150, 80]

col_left, col_right = st.columns([1.15, 1])

with col_left:
    weights = []
    indices = []
    with st.expander("지출목적별 지수 및 나의 가중치", expanded=True):
        grid_left, grid_right = st.columns(2)
        for i, cat in enumerate(categories):
            target_col = grid_left if i < 6 else grid_right
            with target_col:
                idx = st.number_input(f"{cat}", value=float(example_indices[i]), key=f"idx_{i}", step=0.1, label_visibility="collapsed")
                w = st.number_input(f"{cat}", value=float(default_my_weights[i]), key=f"w_{i}", step=1.0, label_visibility="collapsed")
                indices.append(idx)
                weights.append(w)

    total_weight = sum(weights)
    if abs(total_weight - 1000.0) > 1e-6:
        st.warning(f"⚠️ 현재 나의 가중치 총합은 {total_weight:.1f}입니다. 계산식은 자동으로 1,000 기준으로 재조정합니다.")

with col_right:
    normalized_weights = [w / total_weight * 1000.0 for w in weights] if total_weight != 0 else weights
    my_cpi = sum(idx * w for idx, w in zip(indices, normalized_weights)) / 1000.0
    national_cpi = sum(idx * weight for idx, weight in zip(indices, national_weights)) / 1000.0

    r_my = ((my_cpi / 100) ** (1 / 5)) - 1
    r_nat = ((national_cpi / 100) ** (1 / 5)) - 1

    st.metric("나만의 물가지수(My-CPI)", f"{my_cpi:.2f}")
    st.metric("국가 CPI", f"{national_cpi:.2f}", delta=f"차이 {my_cpi - national_cpi:+.2f}p")
    st.metric("My-CPI 연평균 상승률(r_My)", f"{r_my * 100:.2f}%", delta=f"국가 대비 {(r_my - r_nat) * 100:+.2f}%p")

    st.latex(r"\text{My-CPI} = \frac{\sum (I_i \times w_i)}{1000}")
    st.latex(r"r_{My} = \left(\frac{\text{My-CPI}}{100}\right)^{\frac{1}{5}} - 1")

summary_df = pd.DataFrame(
    {
        "분류": [c.split(". ", 1)[1] for c in categories],
        "국가 가중치": national_weights,
        "나의 가중치": [round(w, 1) for w in normalized_weights],
        "나의 가중지수": [round(idx * w, 1) for idx, w in zip(indices, normalized_weights)],
    }
)

st.dataframe(summary_df, use_container_width=True, hide_index=True)
st.caption("※ 지수는 2020=100 기준, 가중치는 총합 1,000 기준으로 이해하면 됩니다.")

fig = go.Figure()
fig.add_trace(go.Bar(x=summary_df["분류"], y=summary_df["국가 가중치"], name="국가 표준 가중치", marker_color="#94A3B8"))
fig.add_trace(go.Bar(x=summary_df["분류"], y=summary_df["나의 가중치"], name="나의 가중치", marker_color="#10B981"))
fig.update_layout(
    barmode="group",
    title="가중치 배분 구조 비교",
    template="plotly_white",
    height=340,
    xaxis_tickangle=-20,
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("학습 활동 및 읽기자료")

stage_items = [
    ("1단계 · 도입: 화폐의 시간가치", "pages/00_물가상승률.py", "https://www.kosis.kr/"),
    ("2단계 · 탐구: 연금과 미래가치", "pages/02_연금과_미래가치.py", "https://www.kosis.kr/"),
    ("3단계 · 정리: 실전 재무 설계", "pages/03_노후_설계.py", "https://www.kosis.kr/"),
]

for title, page_path, reading_link in stage_items:
    activity_col, reading_col = st.columns([3, 1])

    with activity_col:
        if st.button(title, use_container_width=True, key=f"activity_{page_path}"):
            st.switch_page(page_path)

    with reading_col:
        st.link_button("읽기자료", reading_link, use_container_width=True)

st.info("각 페이지는 수업 흐름에 맞춰 단계별로 구성되어 있으며, 학생이 질문을 던지고 계산을 직접 바꾸며 생각을 확장할 수 있게 설계했습니다.")
