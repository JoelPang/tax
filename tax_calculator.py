import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
plt.rcParams["figure.dpi"] = 80
plt.rcParams['font.size'] = 12
plt.rcParams['font.sans-serif'] = ['Montserrat']
plt.style.use('dark_background')


# =============================================================================
# Tax Calculator for Streamlit
# Determine efficiency of tax savings e.g. CPF contribution
# https://share.streamlit.io/joelpang/tax/main/tax_calculator.py
# =============================================================================


st.set_page_config(page_icon="🏙️", page_title="Tax Savings Calculator", layout='centered')
st.header("""**Tax Savings Calculator**""")
st.text("This app is primarily to see how much savings you get when you top up your CPF or SRS, so you can get a sense of whether it's worth locking in the funds at your tax bracket.")
st.text("CPF Top Up (SA): $7,000, capped at current FRS \nTop up SRS account: $15,300 (Singaporean) or $35,700 (foreigner)")

form = st.form(key="submit-form")
income = form.number_input("Annual Income", min_value=1000, max_value=320_000, value=50_000, step=1000)
deductibles = form.number_input("Total deductibles", min_value=0, max_value=320_000, value=22300, step=100)
calculate = form.form_submit_button("Calculate")


def getTaxPayable(income=0):
    total_tax = 0
    for t in taxDict.keys():
        total_tax += max(income-t,0) * taxDict[t]
    return total_tax


def getTaxSavings(income, deductibles):
    new_income = income - deductibles
    old_tax = getTaxPayable(income)
    new_tax = getTaxPayable(new_income)
    tax_saved = old_tax-new_tax
    print(f'Income: {income}')
    print(f'Deductibles: {deductibles}')
    print(f'Old Tax: {old_tax}')
    print(f'New Tax: {new_tax}')
    print(f'Tax saved: {tax_saved}')
    print(f'Delta: {tax_saved/deductibles:.04}')
    return income, new_income, old_tax, new_tax


# =============================================================================


tiers = [0, 2e4, 3e4, 4e4, 8e4, 12e4, 16e4, 20e4, 24e4, 28e4, 32e4]
tax_increments = [0, 0.02, 0.015, 0.035, 0.045, 0.035, 0.03, 0.01, 0.005, 0.005, 0.02, 0]
taxDict = dict(zip(tiers, tax_increments))
print('Tax Rates:', [f'{x:.2%}' for x in np.add.accumulate(tax_increments)])


x = np.arange(1e3, 24e4, 1e3)
y = [getTaxPayable(i) for i in x]


if calculate:
    income, new_income, old_tax, new_tax = getTaxSavings(income, deductibles)
    
    fig, ax = plt.subplots( figsize=(10,8), tight_layout=True)
    plt.plot( x, y, linewidth=3 )
    
    plt.scatter( income, old_tax, marker='o', c='brown', s=50, zorder=9, label=f'Old Tax [{old_tax:,.0f}]' )
    plt.axvline(income, c='brown', linestyle=':')
    plt.axhline(old_tax, c='brown', linestyle=':')
    
    plt.scatter( new_income, new_tax, marker='o', c='gold', s=50, zorder=9, label=f'New Tax [{new_tax:,.0f}]' )
    plt.axvline(new_income, c='gold', linestyle=':')
    plt.axhline(new_tax, c='gold', linestyle=':')
    
    plt.grid(linestyle='-', color='grey', alpha=0.35)
    plt.xlabel('Taxable Income')
    plt.ylabel('Tax Payable')
    plt.legend()
    ax.get_xaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.savefig("output_image.png", dpi=200, bbox_inches='tight', pad_inches=0.3)
    plt.show()
    


    output_text = ""
    output_text += f"\nIncome: {income}"
    output_text += f"\nDeductibles: {deductibles}"
    output_text += f"\nOld Tax: {old_tax}"
    output_text += f"\nNew Tax: {new_tax}"
    output_text += f"\nTax Saved: {old_tax-new_tax}"
    output_text += f"\nTax Savings Efficiency: {(old_tax-new_tax)/deductibles:.2%}"
    
    st.text(f"{output_text}")

    st.image('output_image.png', output_format='png')


st.caption("Other calculators: [HDB Fair Value](https://share.streamlit.io/joelpang/hdb/main/calculator.py)")











