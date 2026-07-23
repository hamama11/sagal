import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
# 0. 기본 페이지 설정 및 UI 스타일링
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="경제 수학: CPI와 연금 설계 대시보드",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS 적용 (폰트 가독성 및 디자인 강화)
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #0F172A; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; color: #475569; margin-bottom: 20px; }
    .card-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 20px; border-radius: 10px; margin-bottom: 15px; }
    .highlight { color: #10B981; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🎓 경제 수학: 데이터로 읽는 경제 지표와 수열</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">소비자물가지수(CPI)로 화폐의 시간가치를 이해하고, 수열의 원리로 나의 미래 가치를 설계합니다.</p>', unsafe_allow_html=True)

# 탭 구성 (1차시, 2차시, 3차시, 읽기자료)
tab1, tab2, tab3, tab_docs = st.tabs([
    "📍 [1차시] My-CPI & 실질 구매력", 
    "📈 [2차시] 복리와 연금 수학", 
    "🏛️ [3차시] 3층 연금 재무 설계", 
    "📚 공식 읽기자료 & 출처"
])

# -----------------------------------------------------------------------------
# [읽기자료 탭] 공식 출처 제공
# -----------------------------------------------------------------------------
with tab_docs:
    st.header("📚 공식 읽기자료 및 출처")
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        st.subheader("[읽기자료 1] KOSIS")
        st.markdown("**통계청 국가통계포털 (품목별 CPI)**")
        st.write("학생들이 영화관람료, 짜장면 등 관심 품목의 과거-현재 지수 데이터를 검색하는 1차 출처입니다.")
        st.link_button("KOSIS 품목별 물가지수 바로가기", "https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1J20001B")

    with col_d2:
        st.subheader("[읽기자료 2] 한국은행")
        st.markdown("**소비자물가지수와 체감물가의 차이**")
        st.write("전체 CPI(가중평균)와 내가 느낀 체감 물가가 왜 다른지 비판적으로 읽고 이유를 탐구합니다.")
        st.link_button("한국은행 경제교육 자료", "https://www.bok.or.kr")

    with col_d3:
        st.subheader("[읽기자료 3] 통계청")
        st.markdown("**소비자물가지수 산출 개요**")
        st.write("라스파이레스 산식(가중평균)과 구간 연평균 상승률(기하평균/CAGR)의 수리적 개념을 이해합니다.")
        st.link_button("통계청 물가통계 안내", "https://kostat.go.kr")

# -----------------------------------------------------------------------------
# [1차시 탭] My-CPI & 실질 구매력 타임머신
# -----------------------------------------------------------------------------
with tab1:
    st.header("📍 [1차시] 내가 만드는 품목별 물가지수(My-CPI)와 실질 구매력")
    st.info("KOSIS 데이터를 기반으로 특정 품목의 연평균 상승률(CAGR)을 구하고, 국가 CPI와의 격차(Gap)를 분석합니다.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("1. 데이터 입력 (기하평균 계산)")
        item_name = st.text_input("조사 품목명", value="영화 관람료")
        years_n = st.slider("조사 기간 (년, n)", min_value=1, max_value=30, value=10)
        p0 = st.number_input("구간 시작 가격 (P₀, 원)", value=8000, step=500)
        pn = st.number_input("구간 끝 가격 (Pₙ, 원)", value=12000, step=500)

        # 기하평균 기반 연평균 상승률(r_item) 계산: r = (P_n / P_0)^(1/n) - 1
        r_item = ((pn / p0) ** (1 / years_n)) - 1
        st.success(f"💡 **{item_name}**의 연평균 상승률(r_품목): **{r_item*100:.2f}%**")

        st.markdown("---")
        st.subheader("2. 국가 전체 CPI 비교")
        r_cpi_input = st.number_input("동 기간 국가 CPI 연평균 상승률 (%)", value=1.50, step=0.1) / 100

        gap = (r_item - r_cpi_input) * 100
        error_rate = abs(r_item - r_cpi_input) / r_cpi_input * 100
        
        st.metric(label="품목 vs 전체 CPI 격차 (Gap)", value=f"{gap:+.2f}%p")
        st.metric(label="오차율", value=f"{error_rate:.1f}%")

    with col2:
        st.subheader("3. 미래 1,000만 원의 실질 구매력 감소 곡선 (등비수열)")
        st.caption("PV = FV / (1 + r)ⁿ 공식을 적용하여, 물가상승률에 따른 실질 구매력 하락을 비교합니다.")

        future_years = np.arange(0, 31)
        base_amount = 10000000 # 1,000만 원

        # 등비수열 감소 곡선 계산
        pv_item = base_amount / ((1 + r_item) ** future_years)
        pv_cpi = base_amount / ((1 + r_cpi_input) ** future_years)

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=future_years, y=pv_item, name=f'{item_name} 상승률 ({r_item*100:.2f}%)', line=dict(color='#F59E0B', width=3)))
        fig1.add_trace(go.Scatter(x=future_years, y=pv_cpi, name=f'국가 CPI ({r_cpi_input*100:.2f}%)', line=dict(color='#06B6D4', width=2, dash='dash')))

        fig1.update_layout(
            xaxis_title="경과 연도 (년 후)",
            yaxis_title="1,000만 원의 실질 구매력 (원)",
            hovermode="x unified",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown(f"""
        > **수학적 정당화 요약:**  
        > {item_name}의 연평균 상승률(**{r_item*100:.2f}%**)은 국가 전체 CPI(**{r_cpi_input*100:.2f}%**)보다 **{gap:+.2f}%p** 다릅니다.  
        > 20년 뒤 1,000만 원의 실질 구매력은 국가 CPI 기준으로는 **{int(pv_cpi[20]):,}원**이지만, {item_name} 물가 기준으로는 **{int(pv_item[20]):,}원** 수준으로 하락합니다.
        """)

# -----------------------------------------------------------------------------
# [2차시 탭] 복리의 마법과 연금 수학
# -----------------------------------------------------------------------------
with tab2:
    st.header("📈 [2차시] 복리의 마법과 연금 수학 (Part 1 ➔ Part 2 연결)")
    st.info("1차시에서 구한 물가상승률(r)을 적용하여 실질 이자율을 도출하고, 등비수열의 합 공식으로 연금의 현재가치(PV)를 산출합니다.")

    col2_1, col2_2 = st.columns([1, 2])

    with col2_1:
        st.subheader("1. 피셔 방정식을 통한 실질 수익률 유도")
        nominal_r = st.slider("명목 연 이자율/수익률 (i, %)", min_value=1.0, max_value=12.0, value=5.0, step=0.1) / 100
        inflation_r = st.slider("1차시 적용 물가상승률 (r, %)", min_value=0.5, max_value=8.0, value=float(r_item*100), step=0.1) / 100

        # 피셔 방정식: (1 + i) = (1 + r_real)(1 + r) => r_real = (1 + i)/(1 + r) - 1
        real_r = ((1 + nominal_r) / (1 + inflation_r)) - 1
        st.warning(f"📊 **실질 수익률 (r_real): {real_r*100:.2f}%**")

        st.markdown("---")
        st.subheader("2. 연금 현재가치(PV) 조건")
        monthly_annuity = st.number_input("매월 수령 희망 연금액 (원)", value=2000000, step=100000)
        pay_years = st.slider("연금 수령 기간 (년)", min_value=5, max_value=40, value=20)
        payment_type = st.radio("수령 시점 선택", ["주기말 수령 (기말급)", "주기초 수령 (기시급)"])

    with col2_2:
        st.subheader("3. 단리(등차수열) vs 복리(등비수열) 성장 및 연금 PV 계산")

        years_seq = np.arange(0, pay_years + 1)
        base_p = 100000000 # 1억 원 기준
        
        # 단리(등차수열) & 복리(등비수열) 비교
        simple_growth = base_p * (1 + nominal_r * years_seq)
        compound_growth = base_p * ((1 + nominal_r) ** years_seq)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=years_seq, y=simple_growth, name="단리 (등차수열)", line=dict(color='#06B6D4', dash='dash')))
        fig2.add_trace(go.Scatter(x=years_seq, y=compound_growth, name="복리 (등비수열)", line=dict(color='#10B981', width=3)))
        
        fig2.update_layout(
            title="1억 원의 시간 경과에 따른 단리 vs 복리 자산 가치 변화",
            xaxis_title="경과 연도 (년)",
            yaxis_title="가치 (원)",
            template="plotly_white",
            height=350
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 연금 현재가치(PV) 계산 공식을 등비수열의 합으로 구함
        # PV = A * [(1 - (1+r)^-n) / r]
        r_m = real_r / 12 # 월 실질 할인율
        n_m = pay_years * 12 # 총 월수
        
        if r_m > 0:
            pv_annuity = monthly_annuity * ((1 - (1 + r_m)**(-n_m)) / r_m)
        else:
            pv_annuity = monthly_annuity * n_m

        if payment_type == "주기초 수령 (기시급)":
            pv_annuity *= (1 + r_m) # (1+r)배 추가 증명 반영

        st.success(f"✨ **{pay_years}년간 매월 {monthly_annuity:,}원**을 수령하기 위해 은퇴 시점에 필요한 **연금의 현재가치(PV) 총액**: **{int(pv_annuity):,} 원**")

# -----------------------------------------------------------------------------
# [3차시 탭] 나의 3층 연금 탑 쌓기
# -----------------------------------------------------------------------------
with tab3:
    st.header("🏛️ [3차시] 나의 3층 연금 탑 쌓기 (실전 재무 설계)")
    st.info("희망 진로 소득 기반으로 3층 보장 체계를 수립하고, 운용 수익률 변화에 따른 민감도(Sensitivity)를 분석합니다.")

    col3_1, col3_2 = st.columns([1, 2])

    with col3_1:
        st.subheader("1. 진로 및 노후 가계 설정")
        job_title = st.text_input("희망 직업 (커리어넷 참조)", value="데이터 분석가")
        start_salary = st.number_input("희망 초봉 (연봉, 원)", value=40000000, step=1000000)
        
        st.markdown("---")
        st.subheader("2. 3층 연금 보장 비율 설정")
        p1_rate = st.slider("1층: 국민연금 커버율 (%)", 10, 50, 30) / 100
        p2_rate = st.slider("2층: 퇴직연금 커버율 (%)", 10, 50, 20) / 100
        
        p3_rate = 1.0 - (p1_rate + p2_rate)
        st.caption(f"3층: **개인연금 필요 커버율: {p3_rate*100:.1f}%**")

        target_monthly = (start_salary / 12) * 0.7 # 은퇴 전 월소득의 70% 목표
        st.write(f"🎯 목표 월 노후 생활비 (현재가치): **{int(target_monthly):,}원**")

    with col3_2:
        st.subheader("3. 3층 연금 구조 시각화 및 수익률 민감도 분석")

        # 3층 연금 분해
        p1_val = target_monthly * p1_rate
        p2_val = target_monthly * p2_rate
        p3_val = target_monthly * p3_rate

        fig3 = go.Figure(data=[
            go.Bar(name='1층: 국민연금', x=['노후 월 생활비'], y=[p1_val], marker_color='#06B6D4'),
            go.Bar(name='2층: 퇴직연금', x=['노후 월 생활비'], y=[p2_val], marker_color='#F59E0B'),
            go.Bar(name='3층: 개인연금 (목표)', x=['노후 월 생활비'], y=[p3_val], marker_color='#10B981')
        ])
        fig3.update_layout(barmode='stack', title="3층 보장 체계별 월 수령 목표액 분해", template="plotly_white", height=300)
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("### 📊 운용 수익률 ±1%p 민감도 분석")
        st.write("개인연금 목표액 달성을 위해 매월 적립해야 하는 금액이 수익률 변동에 따라 어떻게 달라지는지 분석합니다.")

        rates = [nominal_r - 0.01, nominal_r, nominal_r + 0.01]
        req_monthly = []
        
        # 30년 적립, 20년 수령 기준 간이 계산
        for r_val in rates:
            if r_val > 0:
                # 미래 필요 자금 할인
                future_pv = (p3_val * 12 * 20) / ((1 + r_val) ** 30)
                # 매월 납입액 산출 (등비수열 적립)
                pmt = (future_pv * (r_val / 12)) / (((1 + r_val / 12) ** 360) - 1)
            else:
                pmt = p3_val
            req_monthly.append(int(pmt))

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("수익률 -1%p 비상 시", f"{req_monthly[0]:,} 원/월", delta=f"{req_monthly[0] - req_monthly[1]:+,}원", delta_color="inverse")
        col_m2.metric("기본 설계 (기준)", f"{req_monthly[1]:,} 원/월")
        col_m3.metric("수익률 +1%p 달성 시", f"{req_monthly[2]:,} 원/월", delta=f"{req_monthly[2] - req_monthly[1]:+,}원", delta_color="normal")

        st.markdown(f"""
        <div class="card-box">
            <h4>📋 나의 미래 가치 재무 설계 리포트</h4>
            <ul>
                <li><b>희망 직업:</b> {job_title} (예상 초봉: {start_salary:,}원)</li>
                <li><b>은퇴 후 필요 월 생활비:</b> {int(target_monthly):,}원 (현재가치)</li>
                <li><b>3층 개인연금 달성을 위한 매월 필요 적립액:</b> 약 <span class="highlight">{req_monthly[1]:,}원</span> (연 수익률 {nominal_r*100:.1f}% 가정 시)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)