import math
import random

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
question_cols = st.columns(3)
question_items = [
    (
        "도입",
        "왜 돈의 가치가 변할까?",
        "물가상승과 소비자물가 지수를 통해 화폐의 시간가치 개념을 발견합니다.",
        "물가지수(통계청)",
        "https://kosis.kr/statHtml/statHtml.do?sso=ok&returnurl=https%3A%2F%2Fkosis.kr%3A443%2FstatHtml%2FstatHtml.do%3Fmode%3D%26conn_path%3Di3%26list_id%3D%26dbUser%3DNSI.%26tblId%3DDT_1J22001%26vw_cd%3DMT_ZTITLE%26itm_id%3D%26language%3Dko%26pub%3D%26orgId%3D101%26",
    ),
    (
        "탐구",
        "연금? 미래가치?",
        "연금의 현재가치와 미래가치를 계산하며, 수열 구조와 지수함수 개념을 이해합니다.",
        "하이라이트",
        "./[하이라이트] 강승원 X 최정훈 - 서른 즈음에 [더 시즌즈-이효리의 레드카펫]  KBS 방송.mp4",
    ),
    (
        "정리",
        "나의 노후 설계는 어떻게?",
        "은퇴 필요액과 개인연금 목표를 세우고, 수익과 생활비의 균형을 이해합니다.",
        "잡코리아(진로탐색)",
        "https://www.career.go.kr/cloud/w/job/list",
    ),
]

for i, (label, title, description, button_label, button_target) in enumerate(question_items):
    with question_cols[i]:
        card_col, action_col = st.columns([4, 1])
        with card_col:
            st.markdown(
                f"""
                <div class="card">
                    <div class="section-label">{label}</div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with action_col:
            if label == "탐구":
                if st.button(button_label, use_container_width=True):
                    st.video(button_target, format="video/mp4", start_time=0)
            else:
                st.link_button(button_label, button_target, use_container_width=True)

st.markdown("---")
st.subheader("1. 도입: 화폐의 시간가치")

intro_col1, intro_col2 = st.columns(2)
with intro_col1:
    base_year = st.slider("과거 연도", min_value=1940, max_value=2025, value=1990, step=1)
    base_money = st.slider("과거 금액(원)", min_value=0, max_value=10_000_000, value=1_000_000, step=100_000)
    current_year = st.slider("현재 연도", min_value=1940, max_value=2050, value=2025, step=1)

with intro_col2:
    cpi_index = {1990: 100, 2000: 112, 2010: 130, 2020: 148, 2025: 171}
    base_index = cpi_index.get(int(base_year), 100)
    current_index = cpi_index.get(int(current_year), cpi_index[2025])
    adjusted_value = base_money * (current_index / base_index)

    st.metric("현재 시점의 가치", f"{math.floor(adjusted_value):,}원")

    sample_items = pd.DataFrame(
        {
            "품목": ["짜장면", "라면", "스마트폰", "교과서", "배달음식", "지하철 1개월권"],
            "기준가격": [2000, 1200, 1200000, 18000, 9000, 65000],
            "가격지수_1990": [100, 100, 100, 100, 100, 100],
            "가격지수_2000": [104, 108, 122, 110, 116, 113],
            "가격지수_2010": [108, 112, 135, 117, 125, 121],
            "가격지수_2020": [114, 121, 148, 124, 132, 129],
            "가격지수_2025": [120, 128, 162, 130, 139, 136],
        }
    )
    sample_items["현재가격추정"] = (sample_items["기준가격"] * sample_items["가격지수_2025"] / 100).round(0)

    st.caption("예시 품목의 가격 변화 지수(1990=100)")
    st.dataframe(sample_items, use_container_width=True, hide_index=True)

    item_fig = go.Figure()
    for item in sample_items["품목"]:
        item_series = sample_items.loc[sample_items["품목"] == item, ["가격지수_1990", "가격지수_2000", "가격지수_2010", "가격지수_2020", "가격지수_2025"]].iloc[0]
        item_fig.add_trace(
            go.Scatter(
                x=[1990, 2000, 2010, 2020, 2025],
                y=item_series.tolist(),
                mode="lines+markers",
                name=item,
            )
        )

    item_fig.update_layout(
        title="예시 품목의 가격 변화 지수 추이",
        xaxis_title="연도",
        yaxis_title="지수(1990=100)",
        template="plotly_white",
        height=330,
        xaxis_tickangle=-15,
    )
    st.plotly_chart(item_fig, use_container_width=True)

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


def generate_random_scenario():
    rng = random.Random()
    base_weights = [max(1.0, w * rng.uniform(0.65, 1.45)) for w in default_my_weights]
    total_weight = sum(base_weights)
    normalized_weights = [round(w / total_weight * 1000.0, 1) for w in base_weights]
    shifted_indices = [round(idx * rng.uniform(0.92, 1.10), 1) for idx in example_indices]
    return normalized_weights, shifted_indices


if "my_weights" not in st.session_state:
    st.session_state.my_weights = default_my_weights.copy()
if "my_indices" not in st.session_state:
    st.session_state.my_indices = example_indices.copy()
if "scenario_history" not in st.session_state:
    st.session_state.scenario_history = []

weights = st.session_state.my_weights
indices = st.session_state.my_indices

col_right = st.columns(1)[0]

normalized_weights = [w / sum(weights) * 1000.0 for w in weights] if sum(weights) != 0 else weights
my_cpi = sum(idx * w for idx, w in zip(indices, normalized_weights)) / 1000.0
national_cpi = sum(idx * weight for idx, weight in zip(indices, national_weights)) / 1000.0

r_my = ((my_cpi / 100) ** (1 / 5)) - 1
r_nat = ((national_cpi / 100) ** (1 / 5)) - 1

with col_right:
    st.metric("나만의 물가지수(My-CPI)", f"{my_cpi:.2f}")
    st.metric("국가 CPI", f"{national_cpi:.2f}", delta=f"차이 {my_cpi - national_cpi:+.2f}p")
    st.metric("My-CPI 연평균 상승률(r_My)", f"{r_my * 100:.2f}%", delta=f"국가 대비 {(r_my - r_nat) * 100:+.2f}%p")

    st.latex(r"\text{My-CPI} = \frac{\sum (I_i \times w_i)}{1000}")
    st.latex(r"r_{My} = \left(\frac{\text{My-CPI}}{100}\right)^{\frac{1}{5}} - 1")

st.subheader("랜덤 시나리오 속성")
scenario_col, reset_col = st.columns([1, 1])
with scenario_col:
    if st.button("랜덤 시나리오 확인", use_container_width=True):
        random_weights, random_indices = generate_random_scenario()
        st.session_state.my_weights = random_weights
        st.session_state.my_indices = random_indices
        weights = random_weights
        indices = random_indices
        st.session_state.scenario_history.append(
            {
                "scenario": len(st.session_state.scenario_history) + 1,
                "나만의 물가지수": round(sum(idx * w for idx, w in zip(indices, weights)) / 1000.0, 2),
                "국가 CPI": round(sum(idx * weight for idx, weight in zip(indices, national_weights)) / 1000.0, 2),
            }
        )
with reset_col:
    if st.button("기록 초기화", use_container_width=True):
        st.session_state.scenario_history = []
        st.session_state.my_weights = default_my_weights.copy()
        st.session_state.my_indices = example_indices.copy()
        weights = st.session_state.my_weights
        indices = st.session_state.my_indices

normalized_weights = [w / sum(weights) * 1000.0 for w in weights] if sum(weights) != 0 else weights
my_cpi = sum(idx * w for idx, w in zip(indices, normalized_weights)) / 1000.0
national_cpi = sum(idx * weight for idx, weight in zip(indices, national_weights)) / 1000.0
summary_df = pd.DataFrame(
    {
        "분류": [c.split(". ", 1)[1] for c in categories],
        "국가 가중치": national_weights,
        "나의 가중치": [round(w, 1) for w in normalized_weights],
        "나의 가중지수": [round(idx * w, 1) for idx, w in zip(indices, normalized_weights)],
    }
)

st.dataframe(summary_df, use_container_width=True, hide_index=True)
st.caption("※ 각 시나리오는 랜덤하게 새 패턴을 생성하며, 누적 그래프에 기록됩니다.")

if st.session_state.scenario_history:
    history_df = pd.DataFrame(st.session_state.scenario_history)
    history_fig = go.Figure()
    history_fig.add_trace(
        go.Scatter(
            x=history_df["scenario"],
            y=history_df["나만의 물가지수"],
            mode="lines+markers",
            name="나만의 물가지수(My-CPI)",
            line=dict(color="#10B981", width=3),
            marker=dict(size=8),
        )
    )
    history_fig.add_trace(
        go.Scatter(
            x=history_df["scenario"],
            y=history_df["국가 CPI"],
            mode="lines+markers",
            name="국가 CPI",
            line=dict(color="#94A3B8", width=3, dash="dash"),
            marker=dict(size=8),
        )
    )
    history_fig.update_layout(
        title="랜덤 시나리오 누적 변화 추적",
        xaxis_title="시나리오 번호",
        yaxis_title="지수 수준",
        template="plotly_white",
        height=360,
    )
    st.plotly_chart(history_fig, use_container_width=True)

st.info("각 페이지는 수업 흐름에 맞춰 단계별로 구성되어 있으며, 학생이 질문을 던지고 계산을 직접 바꾸며 생각을 확장할 수 있게 설계했습니다.")
