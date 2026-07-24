import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="My-CPI 지수 합성 대시보드", layout="wide")

st.title("🛒 나만의 지출목적별 소비자물가지수(My-CPI) 합성기")
st.caption("KOSIS 12개 지출목적별 지수와 나의 지출 가중치(가중치 총합=1,000)를 반영해 My-CPI를 직접 합성합니다.")

with st.expander("📘 [읽기자료] 국가 CPI는 어떻게 만들어지며, 왜 내 체감 물가와 다를까?", expanded=False):
    st.markdown(
        """
        ### 1. 국가 소비자물가지수(CPI)의 합성 원리
        국가 CPI는 단순히 모든 물건의 가격을 더해서 평균 낸 것이 아닙니다.
        통계청은 대한민국 평균 가구가 한 달 동안 쓰는 돈의 비율을 조사하여 12개 지출목적별 분류에 가중치(총합 1,000)를 나누어 줍니다.

        예를 들어 '주택·수도·광열'은 가계 지출에서 차지하는 비중이 커서 가중치가 약 170인 반면,
        '통신'은 약 43 정도로 설정됩니다.
        이 '지수(가격 변동률)'와 '가중치(지출 비중)'를 곱해 더한 가중평균이 바로 국가 CPI입니다.

        ### 2. '지수(Index)'와 '가중치(Weight)' 구분하기
        - 지수(I_i): 2020년 물가를 100으로 놓았을 때, 지금 물가가 얼마나 변했는지 나타내는 수치
          (예: 오락·문화 지수가 115라면 2020년보다 15% 오른 것)
        - 가중치(w_i): 내 전체 지출(1,000) 중 해당 항목이 차지하는 상대적 비중
          (예: 내가 한 달에 쓰는 돈 중 절반을 사먹는 데 쓴다면 음식·숙박 가중치는 500)

        ### 3. 체감 물가의 격차(Gap)가 발생하는 이유
        통계청이 발표하는 CPI 상승률이 2%인데, 내가 느끼는 물가는 5% 이상 오른 것 같은 이유는
        '지수'가 달라서가 아니라 '가중치'가 다르기 때문입니다.
        국가 CPI는 어른들의 주택비, 보건비 등이 포함된 '전국 평균 가계' 기준이지만,
        학생 여러분은 식료품, 음식·숙박, 오락·문화에 지출이 집중되어 있습니다.
        물가가 많이 오른 항목에 내가 더 높은 가중치를 두고 쓰기 때문에 체감 물가가 더 높게 느껴집니다.

        ### 활동 목표
        - KOSIS의 12개 지출목적별 소비자물가지수 데이터를 수집할 수 있다.
        - 자신의 실제 소비 패턴에 맞추어 나만의 가중치($w_i$, 합 1,000)를 배분하고, 가중평균 산식으로 My-CPI를 합성할 수 있다.
        - 국가 CPI와 My-CPI의 격차를 가중치 구조의 차이 관점에서 수학적·경제적으로 타당화할 수 있다.
        """
    )

st.markdown(
    """
    <style>
    .block-container { padding-top: 1rem; }
    .card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.9rem;
        padding: 1rem;
        margin-bottom: 0.9rem;
    }
    .small-note {
        font-size: 0.9rem;
        color: #475569;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

# 국가 표준 가중치(합=1,000) - KOSIS 지출목적별 소비자물가지수 수업 자료 기준
national_weights = [142.4, 14.4, 52.1, 170.1, 38.2, 73.6, 113.6, 43.5, 56.7, 72.5, 129.8, 93.1]

# 2025년 예시 지수값(2020=100 기준). 학생이 직접 조정 가능
example_indices = [122.5, 108.3, 115.0, 128.4, 112.1, 105.8, 118.2, 102.1, 114.5, 107.3, 124.6, 116.8]
example_index_changes = [idx - 100 for idx in example_indices]

# 학생용 기본 가중치(총합 100%)
default_my_weights = [15.0, 1.0, 4.0, 18.0, 3.0, 6.0, 10.0, 4.0, 9.0, 7.0, 15.0, 8.0]

default_weights = default_my_weights.copy()
base_indices = example_indices.copy()
base_total_weight = sum(default_weights)
base_normalized_weights = [w / base_total_weight * 1000.0 for w in default_weights]
base_my_cpi = sum(idx * w for idx, w in zip(base_indices, base_normalized_weights)) / 1000.0
base_national_cpi = sum(idx * weight for idx, weight in zip(base_indices, national_weights)) / 1000.0
base_r_my = ((base_my_cpi / 100) ** (1 / 5)) - 1
base_r_nat = ((base_national_cpi / 100) ** (1 / 5)) - 1

st.subheader("CPI 비교")
compare_cols = st.columns(3)
with compare_cols[0]:
    st.metric("나만의 물가지수(My-CPI)", f"{base_my_cpi:.2f}")
with compare_cols[1]:
    st.metric("국가 CPI", f"{base_national_cpi:.2f}", delta=f"차이 {base_my_cpi - base_national_cpi:+.2f}p")
with compare_cols[2]:
    st.metric("My-CPI 연평균 상승률(r_My)", f"{base_r_my * 100:.2f}%", delta=f"국가 대비 {(base_r_my - base_r_nat) * 100:+.2f}%p")

st.latex(r"\text{My-CPI} = \frac{\sum (I_i \times w_i)}{1000}")
st.latex(r"r_{My} = \left(\frac{\text{My-CPI}}{100}\right)^{\frac{1}{5}} - 1")
st.caption("학생의 체감물가가 국가 공식 CPI와 다르게 나타나는 이유는, 각 항목의 가격 상승률과 그 항목에 부여한 개인 가중치가 곱해져서 산출되기 때문입니다.")

st.subheader("비율변화 상호작용")
st.info("지수는 2020=100 기준으로, 가중치는 전체 총량 100% 안에서 비율로 입력합니다. 각 항목의 비중을 바꾸면 가중평균과 연평균 상승률이 바로 갱신됩니다.")

with st.expander("12개 지출목적별 세부 수치 입력", expanded=True):
    grid_left, grid_right = st.columns(2)
    weights = []
    indices = []
    for i, cat in enumerate(categories):
        target_col = grid_left if i < 6 else grid_right
        with target_col:
            idx_change = st.number_input(
                f"{cat} 지수 변화율(%)",
                value=float(example_index_changes[i]),
                key=f"idx_{i}",
                step=0.1,
            )
            w_pct = st.number_input(
                f"{cat} 가중치 비율(%)",
                value=float(default_my_weights[i]),
                key=f"w_{i}",
                step=0.1,
            )
            indices.append(100 + idx_change)
            weights.append(w_pct)

    total_weight = sum(weights)
    if abs(total_weight - 100.0) > 1e-6:
        st.warning(f"⚠️ 현재 나의 가중치 총합은 {total_weight:.1f}%입니다. 계산식은 자동으로 100% 기준으로 재조정합니다.")

normalized_weights = [w / total_weight * 1000.0 for w in weights] if total_weight != 0 else weights
my_cpi = sum(idx * w for idx, w in zip(indices, normalized_weights)) / 1000.0
national_cpi = sum(idx * weight for idx, weight in zip(indices, national_weights)) / 1000.0

r_my = ((my_cpi / 100) ** (1 / 5)) - 1
r_nat = ((national_cpi / 100) ** (1 / 5)) - 1

st.subheader("가중치 결과표")
summary_df = pd.DataFrame(
    {
        "분류": [c.split(". ", 1)[1] for c in categories],
        "국가 가중치(%)": [round(w / 1000 * 100, 1) for w in national_weights],
        "나의 가중치(%)": [round(w, 1) for w in weights],
        "나의 가중지수": [round(idx * w, 1) for idx, w in zip(indices, normalized_weights)],
    }
)
st.dataframe(summary_df, use_container_width=True, hide_index=True)

st.subheader("그래프")
fig = go.Figure()
fig.add_trace(go.Bar(x=summary_df["분류"], y=summary_df["국가 가중치(%)"], name="국가 표준 가중치", marker_color="#94A3B8"))
fig.add_trace(go.Bar(x=summary_df["분류"], y=summary_df["나의 가중치(%)"], name="나의 가중치", marker_color="#10B981"))
fig.update_layout(
    barmode="group",
    title="가중치 배분 구조 비교",
    template="plotly_white",
    height=340,
    xaxis_tickangle=-20,
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    f"""
    <div class="card">
        <strong>💡 타당화 도출 요약</strong><br>
        나의 My-CPI는 <strong>{my_cpi:.2f}</strong>이며, 국가 CPI <strong>{national_cpi:.2f}</strong>보다
        <strong>{my_cpi - national_cpi:+.2f}p</strong> 차이가 납니다.
        이는 식료품·음식·숙박 등 상승률이 높은 항목에 국가보다 더 큰 가중치를 두었기 때문입니다.
        즉, <strong>가중치 배분 구조</strong>와 <strong>개별 지수 수준</strong>이 동시에 반영된 결과로 체감 물가가 달라집니다.
    </div>
    """,
    unsafe_allow_html=True,
)
