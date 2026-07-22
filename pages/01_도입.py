import math

import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="도입 · 화폐의 시간가치", layout="wide")

st.title("1단계 · 도입: 돈의 가치가 왜 달라질까?")
st.caption("물가상승과 구매력 변화의 관계를 수학적으로 탐구해 봅니다.")

col1, col2 = st.columns(2)
with col1:
    base_year = st.number_input("과거 연도", min_value=1940, max_value=2025, value=1990, step=1)
    base_money = st.number_input("과거 금액(원)", min_value=0, value=1_000_000, step=100_000)
    current_year = st.number_input("현재 연도", min_value=1940, max_value=2050, value=2025, step=1)

with col2:
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
st.plotly_chart(fig, width="stretch")

st.subheader("확인 문제")
q1 = st.radio("Q1. 물가가 상승하면 같은 금액의 구매력은 어떻게 되나요?", ["강해진다", "약해진다"]) 
if q1 == "약해진다":
    st.success("정답입니다. 같은 돈으로 살 수 있는 재화의 양이 줄어듭니다.")
else:
    st.warning("다시 생각해 보세요. 물가가 올라가면 같은 돈의 구매력이 줄어듭니다.")

q2 = st.radio("Q2. 왜 돈의 시간가치가 중요할까요?", ["미래 돈과 현재 돈이 다른 가치를 가지기 때문이다", "돈이 항상 같은 값이기 때문이다"])
if q2 == "미래 돈과 현재 돈이 다른 가치를 가지기 때문이다":
    st.success("정답입니다. 화폐는 시간에 따라 가치가 달라지기 때문입니다.")
else:
    st.warning("핵심은 시간에 따라 현금의 가치가 달라진다는 점입니다.")
