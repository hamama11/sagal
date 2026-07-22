import math

import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="노후 설계", layout="wide")

st.title("3단계 · 정리: 실전 노후 설계")
st.caption("은퇴 필요액과 개인연금 목표액을 수치로 설계합니다.")

col1, col2 = st.columns(2)

with col1:
    retire_age = st.slider("희망 은퇴 연령", min_value=50, max_value=70, value=60)
    life_expectancy = st.slider("기대 수명", min_value=70, max_value=95, value=85)
    inflation_rate = st.slider("물가상승률(%)", min_value=1.0, max_value=6.0, value=2.5, step=0.1)
    current_salary = st.number_input("현재 연봉(원)", min_value=0, value=45_000_000, step=1_000_000)

with col2:
    retire_years = max(life_expectancy - retire_age, 1)
    annual_living_cost = current_salary * 0.7
    future_need = annual_living_cost * ((1 + inflation_rate / 100) ** retire_years)
    total_need = future_need * retire_years

    public_pension = current_salary * 0.12
    retirement_pension = current_salary * 0.08
    personal_annuity_goal = max(total_need - public_pension - retirement_pension, 0)
    monthly_personal_need = personal_annuity_goal / (retire_years * 12)

    st.metric("은퇴 시 필요한 총액", f"{math.floor(total_need):,}원")
    st.metric("월 개인연금 목표 납입액", f"{math.floor(monthly_personal_need):,}원")
    st.metric("개인연금 목표액", f"{math.floor(personal_annuity_goal):,}원")

labels = ["은퇴 시 필요 총액", "공적연금", "퇴직연금", "개인연금 목표액"]
values = [total_need, public_pension, retirement_pension, personal_annuity_goal]
fig = go.Figure(go.Bar(x=labels, y=values, marker_color=["#145c9f", "#6ea6d7", "#f0b24b", "#0f9d75"]))
fig.update_layout(title="재무 설계 구성 요소 비교")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 정리 질문")
st.write("1. 노후 준비는 단순히 '저축'만으로 해결되는가?")
st.write("2. 인플레이션이 반영되지 않으면 노후 필요액은 어떻게 달라지는가?")
st.write("3. 공적연금과 개인연금의 역할은 각각 무엇인가?")
