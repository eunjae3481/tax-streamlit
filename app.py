import streamlit as st

st.set_page_config(page_title="절세계산기", page_icon="💰", layout="centered")

# -----------------------------
# 꾸미기용 CSS
# -----------------------------
st.markdown("""
<style>
.card {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
h1, h2, h3, h4 {
    color: #FF6B6B;
    font-weight: 700;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 세율표 (2024 기준 단순화)
# -----------------------------
tax_brackets = [
    (0, 14000000, 0.06, 0),
    (14000000, 50000000, 0.15, 1260000),
    (50000000, 88000000, 0.24, 5760000),
    (88000000, 150000000, 0.35, 15160000),
    (150000000, 300000000, 0.38, 37660000),
    (300000000, 500000000, 0.40, 97660000),
    (500000000, float("inf"), 0.42, 177660000)
]

# -----------------------------
# 근로소득공제 계산
# -----------------------------
def calculate_work_income_deduction(income):
    if income <= 5000000:
        return income * 0.7
    elif income <= 15000000:
        return 3500000 + (income - 5000000) * 0.4
    elif income <= 45000000:
        return 7500000 + (income - 15000000) * 0.15
    elif income <= 100000000:
        return 12000000 + (income - 45000000) * 0.05
    else:
        return 14750000 + (income - 100000000) * 0.02


# -----------------------------
# 누진세 계산
# -----------------------------
def calculate_tax(taxable_income):
    for low, high, rate, deduction in tax_brackets:
        if low <= taxable_income <= high:
            return taxable_income * rate - deduction
    return 0


# -----------------------------
# UI 시작
# -----------------------------
st.markdown("<h1>💰 절세계산기</h1>", unsafe_allow_html=True)
st.write("월급을 입력하면 실제 내는 근로소득세를 계산해줘요!")


with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📥 월급 입력")

    monthly_income = st.number_input("월 급여(세전 기준)", min_value=0, step=10000)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# 결과 계산
# -----------------------------
if monthly_income > 0:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 계산 결과")

        annual_income = monthly_income * 12
        deduction = calculate_work_income_deduction(annual_income)
        taxable_income = max(0, annual_income - deduction - 1500000)  # 기본공제(단순화)

        tax = calculate_tax(taxable_income)
        monthly_tax = round(tax / 12)

        real_salary = monthly_income - monthly_tax

        st.write(f"**연봉:** {annual_income:,.0f} 원")
        st.write(f"**근로소득공제:** {deduction:,.0f} 원")
        st.write(f"**과세표준:** {taxable_income:,.0f} 원")
        st.write(f"**연 소득세:** {round(tax):,} 원")
        st.write(f"👉 **월 소득세:** {monthly_tax:,} 원")
        st.markdown("---")
        st.write(f"💡 **월 실수령액:** **{real_salary:,.0f} 원**")

        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("월급을 입력하면 세금을 계산해드릴게요 😊")
