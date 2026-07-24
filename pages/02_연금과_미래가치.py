import math

import streamlit as st

st.set_page_config(page_title="연금과 미래가치", layout="wide")

st.title("2단계 · 탐구: 연금과 미래가치")
st.caption("기말급과 기시급을 비교하며 수열 구조를 이해합니다.")

col1, col2 = st.columns(2)

with col1:
    annuity_mode = st.selectbox("유형 선택", ["주기말(기말급)", "주기초(기시급)"])
    payment = st.number_input("매년 납입/수령액(원)", min_value=0, value=3_000_000, step=100_000)
    years = st.slider("기간(년)", min_value=1, max_value=40, value=10)
    rate = st.slider("연 이율(%)", min_value=1.0, max_value=10.0, value=4.0, step=0.1)

with col2:
    r = rate / 100
    pv_end = payment * (1 - (1 + r) ** (-years)) / r
    fv_end = payment * (((1 + r) ** years - 1) / r)

    if annuity_mode == "주기초(기시급)":
        pv = pv_end * (1 + r)
        fv = fv_end * (1 + r)
    else:
        pv = pv_end
        fv = fv_end

    st.metric("현재가치(PV)", f"{math.floor(pv):,}원")
    st.metric("미래가치(FV)", f"{math.floor(fv):,}원")
    st.caption("주기말 기준 수식: PV = A × [1-(1+r)^(-n)] / r")
    st.caption("주기말 기준 수식: FV = A × [(1+r)^n - 1] / r")
    st.info(f"72의 법칙 근사값: 약 {72 / rate:.1f}년 후에 자산이 2배가 됩니다.")

st.image("../assets/annuity_timeline.svg", use_container_width=True)

st.markdown("### 수학적 의미 정리")
st.write("- 기말급은 매년 말에 납입하는 구조로, 첫 납입이 이자를 한 번 덜 받습니다.")
st.write("- 기시급은 매년 초에 납입하므로, 첫 지불이 즉시 이자를 받게 되어 결과가 더 큽니다.")
st.write("- 연금은 수열의 합과 지수함수 개념이 결합된 대표적인 경제수학 소재입니다.")
