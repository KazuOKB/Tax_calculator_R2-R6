import streamlit as st
from utils import floor_to_4000, calc_salary_deduction, determine_tax_rate, format_num

# ページ設定
st.set_page_config(page_title="ホーム", layout="wide")
st.title("所得税・住民税計算アプリ")

# サイドバー
salary        = st.sidebar.number_input("給与収入（円）",   min_value=0,     value=0,    step=10_000)
insurance     = st.sidebar.number_input("社会保険料（円）", min_value=0,     value=0,    step=1_000)
misc_income   = st.sidebar.number_input("雑所得（円）",     min_value=0,     value=0,    step=1_000)
resident_rate = st.sidebar.number_input("住民税率（％）",   min_value=0.0,   value=10.0, step=0.1)

# ボタン押下時の計算
if st.button("税率、税金の計算"):
    # 給与所得控除
    salary_deduction = calc_salary_deduction(salary)
    # 給与所得控除後の給与所得
    salary_r4 = floor_to_4000(salary)
    salary_net = salary_r4 - salary_deduction
    # 全所得(控除後給与所得 + 雑所得)
    total_income = salary_net + misc_income

    # 基礎控除と社会保険料等を除いたものが課税所得（普通は48万円）
    basic_deduction = 480000
    taxable = total_income - (insurance + basic_deduction)

    # 住民税用の課税所得（住民税に対する基礎控除は43万円）
    basic_deduction_resident= 430000
    taxable_resident = total_income - (insurance + basic_deduction_resident)

    # 真の課税所得
    # 1000円未満を切り捨てる(一応負の値も対処)
    taxable = int(max(0, taxable // 1000 * 1000))
    taxable_resident = int(max(0, taxable_resident // 1000 * 1000))
    # 所得税率と所得税控除額の算出
    tax_rate, tax_deduction = determine_tax_rate(taxable)
    tax_rate_resident, tax_deduction_resident = determine_tax_rate(taxable_resident) 
    # 所得税の計算
    income_tax = int(taxable * tax_rate - tax_deduction)
    # 住民税
    resident_tax = int(taxable_resident * (resident_rate / 100))
    # 復興特別所得税(所得税×2.1%)
    surcharge = int(income_tax * 0.021)
    # 合計所得税(源泉徴収相当)
    total_income_tax   = income_tax + surcharge

    st.header("計算結果")
    
    st.subheader("・控除額に関して")
    st.write(f"給与所得控除後の金額: {format_num(int(salary_net))} 円")

    out1, out2 = st.columns(2)
    with out1:
        st.subheader("・所得税")
        st.write(f"所得控除額 (基礎控除や保険料): {format_num(insurance + basic_deduction)} 円")
        st.write(f"課税所得: {format_num(taxable)} 円")
        st.write(f"税率: {tax_rate*100:.1f}%")
        st.write(f"所得税控除額 {format_num(tax_deduction)} 円")
        st.write(f"所得税: {format_num(income_tax)} 円")
        st.write(f"復興特別所得税: {format_num(surcharge)} 円 (所得税額×2.1％)")
        st.write(f"合計所得税: {format_num(total_income_tax)} 円")

    with out2:
        st.subheader("・住民税")
        st.write(f"所得控除額 (基礎控除や保険料): {format_num(insurance + basic_deduction_resident)} 円")
        st.write(f"課税所得: {format_num(taxable_resident)} 円")
        st.write(f"住民税率: {resident_rate:.1f}％")
        st.write(f"住民税額: {format_num(resident_tax)} 円")

