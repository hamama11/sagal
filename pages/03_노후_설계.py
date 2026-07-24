import math

import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="노후 설계", layout="wide")

st.markdown(
    """
    <style>
    .activity-box {
        border: 1px solid #d1d5db;
        border-radius: 12px;
        padding: 16px;
        background: #f8fafc;
        margin-bottom: 14px;
    }
    .question-box {
        border-left: 6px solid #2563eb;
        background: #eff6ff;
        padding: 14px 16px;
        border-radius: 10px;
        margin: 10px 0 14px 0;
    }
    .summary-box {
        border-left: 6px solid #16a34a;
        background: #f0fdf4;
        padding: 14px 16px;
        border-radius: 10px;
        margin-top: 12px;
    }
    .answer-card {
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 18px;
        background: white;
        margin-top: 16px;
    }
    .small-text {
        color: #475569;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("3단계 · 정리: 실전 노후 설계")
st.caption("은퇴 필요액과 개인연금 목표액을 계산하며, 연금의 3층 구조를 이해합니다.")

st.markdown(
    """
    <div class="activity-box">
        <h3 style="margin-top:0;">생각 열기</h3>
        <p>노후 준비는 단순히 한 번에 큰돈을 모으는 일이 아니라, 
        <strong>국민연금·퇴직연금·개인연금</strong>이 서로 역할을 나누어 준비하는 과정입니다.</p>
        <p class="small-text">
        아래 계산기를 이용해 나의 은퇴 이후 필요한 생활비와, 그중 개인이 추가로 준비해야 할 금액을 확인해 보세요.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input("이름", placeholder="이름을 입력하세요")
    retire_age = st.slider("희망 은퇴 연령", min_value=50, max_value=70, value=60)
    life_expectancy = st.slider("기대 수명", min_value=70, max_value=95, value=85)
    inflation_rate = st.slider("물가상승률(%)", min_value=1.0, max_value=6.0, value=2.5, step=0.1)
    current_salary = st.number_input("현재 연봉(원)", min_value=0, value=45_000_000, step=1_000_000)

with col2:
    retire_years = max(life_expectancy - retire_age, 1)
    annual_living_cost = current_salary * 0.7
    future_need = annual_living_cost * ((1 + inflation_rate / 100) ** retire_years)
    total_need = future_need * retire_years

    public_pension = current_salary * 0.12 * retire_years
    retirement_pension = current_salary * 0.08 * retire_years
    personal_annuity_goal = max(total_need - public_pension - retirement_pension, 0)
    monthly_personal_need = personal_annuity_goal / (retire_years * 12)

    st.metric("은퇴 시 필요한 총액", f"{math.floor(total_need):,}원")
    st.metric("개인연금 목표액", f"{math.floor(personal_annuity_goal):,}원")
    st.metric("월 개인연금 목표 납입액", f"{math.floor(monthly_personal_need):,}원")

st.markdown("### 활동 1. 계산 결과를 읽고 답해 보기")

q1_col1, q1_col2 = st.columns(2)

with q1_col1:
    st.markdown(
        f"""
        <div class="question-box">
            <strong>질문 1.</strong> 은퇴 후 생활 기간은 몇 년인가?<br>
            계산: {life_expectancy}세 - {retire_age}세 = <strong>{retire_years}년</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    answer1 = st.text_input("학생 답안 1: 은퇴 후 생활 기간", placeholder="예: 25년")

    st.markdown(
        f"""
        <div class="question-box">
            <strong>질문 2.</strong> 현재 연봉의 70%를 1년 생활비로 보면 얼마인가?<br>
            계산: {current_salary:,.0f} × 0.7 = <strong>{annual_living_cost:,.0f}원</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    answer2 = st.text_input("학생 답안 2: 1년 생활비", placeholder="예: 31,500,000원")

with q1_col2:
    st.markdown(
        f"""
        <div class="question-box">
            <strong>질문 3.</strong> 물가상승률 {inflation_rate:.1f}%를 반영하면 은퇴 시점 필요 생활비는 얼마인가?<br>
            계산 결과: <strong>{future_need:,.0f}원</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    answer3 = st.text_input("학생 답안 3: 은퇴 시점의 1년 필요 생활비", placeholder="예: 58,000,000원")

    st.markdown(
        f"""
        <div class="question-box">
            <strong>질문 4.</strong> 개인이 추가로 준비해야 할 개인연금 목표액은 얼마인가?<br>
            계산 결과: <strong>{personal_annuity_goal:,.0f}원</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    answer4 = st.text_input("학생 답안 4: 개인연금 목표액", placeholder="예: 800,000,000원")

st.subheader("활동 2. 연금 3층 구조로 보기")

fig = go.Figure()

fig.add_trace(go.Bar(x=["노후 필요자금"], y=[public_pension], name="1층 국민연금", marker_color="#34a853"))
fig.add_trace(go.Bar(x=["노후 필요자금"], y=[retirement_pension], name="2층 퇴직연금", marker_color="#4285f4"))
fig.add_trace(go.Bar(x=["노후 필요자금"], y=[personal_annuity_goal], name="3층 개인연금", marker_color="#fbbc05"))
fig.add_trace(
    go.Scatter(
        x=["노후 필요자금"],
        y=[total_need],
        mode="markers+text",
        name="총 필요액",
        marker=dict(color="#111827", size=12),
        text=[f"총 필요액 {math.floor(total_need):,}원"],
        textposition="top center",
    )
)

fig.update_layout(
    barmode="stack",
    title="연금 3층 구조와 노후 필요자금",
    xaxis_title="구분",
    yaxis_title="금액(원)",
    template="plotly_white",
    height=450,
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 활동 3. 나의 생각 적기")

thought1 = st.text_area(
    "1. 왜 국민연금과 퇴직연금만으로는 노후 준비가 부족할 수 있을까요?",
    placeholder="자신의 생각을 2~3문장으로 써 보세요.",
    height=100,
)

thought2 = st.text_area(
    "2. 물가상승률이 높아질수록 개인연금 목표액은 어떻게 달라질까요?",
    placeholder="그래프와 계산 결과를 바탕으로 설명해 보세요.",
    height=100,
)

thought3 = st.text_area(
    "3. 나의 희망 은퇴연령이 빨라질수록 노후 준비는 왜 더 중요해질까요?",
    placeholder="은퇴 후 생활 기간과 연결해서 써 보세요.",
    height=100,
)

final_statement = st.text_input(
    "나의 한 줄 결론",
    placeholder="예: 국민연금만으로는 부족하므로 개인연금을 일찍 준비해야 한다.",
)

report_text = f"""
[노후 설계 활동지 답안]

이름: {student_name if student_name else '미입력'}

1. 계산 답안
- 은퇴 후 생활 기간: {answer1 if answer1 else '미입력'}
- 1년 생활비: {answer2 if answer2 else '미입력'}
- 은퇴 시점의 1년 필요 생활비: {answer3 if answer3 else '미입력'}
- 개인연금 목표액: {answer4 if answer4 else '미입력'}

2. 계산 결과
- 희망 은퇴 연령: {retire_age}세
- 기대 수명: {life_expectancy}세
- 은퇴 후 생활 기간: {retire_years}년
- 현재 연봉: {current_salary:,.0f}원
- 은퇴 시 필요한 총액: {math.floor(total_need):,}원
- 개인연금 목표액: {math.floor(personal_annuity_goal):,}원
- 월 개인연금 목표 납입액: {math.floor(monthly_personal_need):,}원

3. 나의 생각
- 질문 1: {thought1 if thought1 else '미입력'}
- 질문 2: {thought2 if thought2 else '미입력'}
- 질문 3: {thought3 if thought3 else '미입력'}

4. 한 줄 결론
- {final_statement if final_statement else '미입력'}
"""

report_html = f"""
<html>
<head>
<meta charset="utf-8">
<title>노후 설계 활동지 답안</title>
<style>
body {{
    font-family: Arial, sans-serif;
    padding: 24px;
    line-height: 1.6;
}}
h1, h2 {{
    color: #1e3a8a;
}}
.card {{
    border: 1px solid #d1d5db;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 14px;
    background: #f8fafc;
}}
</style>
</head>
<body>
    <h1>노후 설계 활동지 답안</h1>
    <div class="card">
        <h2>기본 정보</h2>
        <p><strong>이름:</strong> {student_name if student_name else '미입력'}</p>
    </div>
    <div class="card">
        <h2>계산 답안</h2>
        <p>은퇴 후 생활 기간: {answer1 if answer1 else '미입력'}</p>
        <p>1년 생활비: {answer2 if answer2 else '미입력'}</p>
        <p>은퇴 시점의 1년 필요 생활비: {answer3 if answer3 else '미입력'}</p>
        <p>개인연금 목표액: {answer4 if answer4 else '미입력'}</p>
    </div>
    <div class="card">
        <h2>계산 결과</h2>
        <p>희망 은퇴 연령: {retire_age}세</p>
        <p>기대 수명: {life_expectancy}세</p>
        <p>은퇴 후 생활 기간: {retire_years}년</p>
        <p>현재 연봉: {current_salary:,.0f}원</p>
        <p>은퇴 시 필요한 총액: {math.floor(total_need):,}원</p>
        <p>개인연금 목표액: {math.floor(personal_annuity_goal):,}원</p>
        <p>월 개인연금 목표 납입액: {math.floor(monthly_personal_need):,}원</p>
    </div>
    <div class="card">
        <h2>나의 생각</h2>
        <p>1. {thought1 if thought1 else '미입력'}</p>
        <p>2. {thought2 if thought2 else '미입력'}</p>
        <p>3. {thought3 if thought3 else '미입력'}</p>
    </div>
    <div class="card">
        <h2>한 줄 결론</h2>
        <p>{final_statement if final_statement else '미입력'}</p>
    </div>
</body>
</html>
"""

st.markdown("### 답변 확인 및 저장")

with st.container():
    st.markdown(
        f"""
        <div class="answer-card">
            <h3 style="margin-top:0;">답변 요약 카드</h3>
            <p><strong>이름:</strong> {student_name if student_name else '미입력'}</p>
            <p><strong>은퇴 후 생활 기간:</strong> {answer1 if answer1 else '미입력'}</p>
            <p><strong>1년 생활비:</strong> {answer2 if answer2 else '미입력'}</p>
            <p><strong>은퇴 시점의 1년 필요 생활비:</strong> {answer3 if answer3 else '미입력'}</p>
            <p><strong>개인연금 목표액:</strong> {answer4 if answer4 else '미입력'}</p>
            <p><strong>질문 1 생각:</strong> {thought1 if thought1 else '미입력'}</p>
            <p><strong>질문 2 생각:</strong> {thought2 if thought2 else '미입력'}</p>
            <p><strong>질문 3 생각:</strong> {thought3 if thought3 else '미입력'}</p>
            <p><strong>한 줄 결론:</strong> {final_statement if final_statement else '미입력'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

download_col1, download_col2 = st.columns(2)

with download_col1:
    st.download_button(
        label="답변 TXT 저장",
        data=report_text,
        file_name="retirement_activity_report.txt",
        mime="text/plain",
    )

with download_col2:
    st.download_button(
        label="답변 HTML 저장",
        data=report_html,
        file_name="retirement_activity_report.html",
        mime="text/html",
    )