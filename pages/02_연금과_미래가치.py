import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="연금과 미래가치", layout="wide")

st.title("2단계 · 탐구: 미래가치")
st.caption("주기말(기말급)과 주기초(기시급)을 비교하며 수열 구조를 이해합니다.")

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

    pv_due = pv_end * (1 + r)
    fv_due = fv_end * (1 + r)

    if annuity_mode == "주기초(기시급)":
        pv = pv_due
        fv = fv_due
    else:
        pv = pv_end
        fv = fv_end

    st.metric("현재가치(PV)", f"{math.floor(pv):,}원")
    st.metric("미래가치(FV)", f"{math.floor(fv):,}원")
    st.caption("주기말 기준 수식: PV = A × [1-(1+r)^(-n)] / r")
    st.caption("주기말 기준 수식: FV = A × [(1+r)^n - 1] / r")
    st.info(f"72의 법칙 근사값: 약 {72 / rate:.1f}년 후에 자산이 2배가 됩니다.")

st.markdown("### 기말급·기시급 누적 비교 그래프")

end_values = []
due_values = []

for n in range(1, years + 1):
    fv_end_n = payment * (((1 + r) ** n - 1) / r)
    fv_due_n = fv_end_n * (1 + r)

    end_values.append(fv_end_n)
    due_values.append(fv_due_n)

graph_df = pd.DataFrame(
    {
        "연도": list(range(1, years + 1)),
        "기말급 미래가치": end_values,
        "기시급 미래가치": due_values,
        "차이": [d - e for e, d in zip(end_values, due_values)],
    }
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=graph_df["연도"],
        y=graph_df["기말급 미래가치"],
        mode="lines+markers",
        name="주기말(기말급)",
        line=dict(color="#2563eb", width=3),
        marker=dict(size=7),
    )
)

fig.add_trace(
    go.Scatter(
        x=graph_df["연도"],
        y=graph_df["기시급 미래가치"],
        mode="lines+markers",
        name="주기초(기시급)",
        line=dict(color="#10b981", width=3),
        marker=dict(size=7),
    )
)

fig.update_layout(
    title="연도별 누적 미래가치 비교",
    xaxis_title="연도",
    yaxis_title="미래가치(원)",
    template="plotly_white",
    height=420,
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

final_gap = fv_due - fv_end
st.metric("최종 차이(기시급 - 기말급)", f"{math.floor(final_gap):,}원")

st.markdown("### 납입 시점 이해하기")
if annuity_mode == "주기말(기말급)":
    st.write("- 기말급은 매년 말에 납입하므로, 각 납입금이 이자를 받는 기간이 상대적으로 짧습니다.")
    st.write("- 따라서 같은 금액을 같은 횟수 납입해도 기시급보다 미래가치가 작습니다.")
else:
    st.write("- 기시급은 매년 초에 납입하므로, 각 납입금이 한 기간 더 이자를 받습니다.")
    st.write("- 따라서 같은 금액을 같은 횟수 납입하면 기말급보다 미래가치가 더 큽니다.")

st.markdown("### 연도별 비교 표")
display_df = graph_df.copy()
display_df["기말급 미래가치"] = display_df["기말급 미래가치"].round(0).astype(int)
display_df["기시급 미래가치"] = display_df["기시급 미래가치"].round(0).astype(int)
display_df["차이"] = display_df["차이"].round(0).astype(int)

st.dataframe(display_df, use_container_width=True, hide_index=True)

st.markdown("### 수학적 의미 정리")
st.write("- 기말급은 매년 말에 납입하는 구조로, 첫 납입이 이자를 한 번 덜 받습니다.")
st.write("- 기시급은 매년 초에 납입하므로, 첫 지불이 즉시 이자를 받게 되어 결과가 더 큽니다.")
st.write("- 연금은 수열의 합과 지수함수 개념이 결합된 대표적인 경제수학 소재입니다.")