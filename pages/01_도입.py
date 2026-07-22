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
st.plotly_chart(fig, use_container_width=True)

st.subheader("학문 간의 융합")
st.markdown(
    """
    1. 학문 간의 융합: 수학적 원리와 경제·사회 지표의 결합
    가장 핵심적인 융합은 경제 현상을 수학적 언어로 해석하고 해결하는 과정에서 일어납니다.

    - 경제지표와 수의 체계: 물가 지수, 실업률, 고용률, GDP 등 복잡한 사회 경제 지표를 비와 비율, 백분율의 개념을 통해 수치화하고 해석합니다.
    - 금융과 수열: 예금, 적금, 연금과 같은 금융 상품의 원리합계와 현재가치를 등차수열과 등비수열(및 급수)의 합 공식을 통해 산출합니다.
    - 경제 현상과 함수·미분: 생산, 비용, 수요·공급의 관계를 함수로 모델링하고, 미분을 통해 한계비용이나 최적 생산량, 탄력성 등을 분석하여 합리적 의사결정의 근거를 마련합니다.
    - 데이터와 행렬: 다량의 경제 데이터를 행렬로 구조화하고, 역행렬 연산을 통해 투입-산출 분석이나 시장 점유율 예측(마르코프 체인)을 수행합니다.
    """
)

