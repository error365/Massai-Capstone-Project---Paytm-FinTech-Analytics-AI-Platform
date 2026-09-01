import numpy as np
import pandas as pd

# 1. Base Unlevered FCFF Inputs (in INR)
ebit = 500_000_000  # ₹50 Cr
tax_rate = 0.25
dna = 50_000_000  # ₹5 Cr
capex = 60_000_000  # ₹6 Cr
delta_nwc = 15_000_000  # ₹1.5 Cr

fcff_0 = ebit * (1 - tax_rate) + dna - capex - delta_nwc
print(f"Base FCFF (Year 0): INR {fcff_0:,.2f}")

# 2. Capital Structure & WACC Parameters
rf = 0.07  # Risk-free rate (7%)
rm = 0.13  # Market return (13%)
beta_tech = 1.55  # PAYTECH beta

cost_of_equity = rf + beta_tech * (rm - rf)  # 16.30%
cost_of_debt_after_tax = 0.09 * (1 - tax_rate)  # 6.75%
w_e, w_d = 0.80, 0.20

wacc_base = (w_e * cost_of_equity) + (w_d * cost_of_debt_after_tax)  # 14.39%
terminal_g_base = 0.04  # 4.0%

# 3. 5-Year Cash Flow Projections
growth_rates = [0.18, 0.16, 0.14, 0.12, 0.10]
fcffs = []
curr_fcff = fcff_0
for g in growth_rates:
  curr_fcff *= 1 + g
  fcffs.append(curr_fcff)


# 4. Valuation Function
def calculate_ev(wacc_val: float, g_val: float) -> float:
  pv_fcff = sum(f / ((1 + wacc_val) ** i) for i, f in enumerate(fcffs, 1))
  terminal_val = (fcffs[-1] * (1 + g_val)) / (wacc_val - g_val)
  pv_tv = terminal_val / ((1 + wacc_val) ** 5)
  return pv_fcff + pv_tv


# 5. Sensitivity Analysis Matrix (3x3 Grid)
wacc_grid = [wacc_base - 0.01, wacc_base, wacc_base + 0.01]
g_grid = [terminal_g_base - 0.01, terminal_g_base, terminal_g_base + 0.01]

# Self-check spread verification
assert min(wacc_grid) - max(g_grid) >= 0.01, (
    "WACC must exceed terminal growth by at least 1pp in all cells!"
)

matrix = np.zeros((3, 3))
for i, w in enumerate(wacc_grid):
  for j, g in enumerate(g_grid):
    matrix[i, j] = calculate_ev(w, g) / 1e7  # Convert to Crores

sens_table = pd.DataFrame(
    matrix,
    index=[f"WACC = {w*100:.2f}%" for w in wacc_grid],
    columns=[f"Terminal g = {g*100:.2f}%" for g in g_grid],
)

print("\n--- DCF Sensitivity Matrix (Enterprise Value in INR Cr) ---")
print(sens_table.round(2))

# 6. EV/EBITDA Multiple Valuation Cross-Check
ebitda = ebit + dna  # ₹55 Cr
multiple = 12.0
implied_ev_multiple = ebitda * multiple

base_dcf_ev = calculate_ev(wacc_base, terminal_g_base)
print(f"\nBase DCF Enterprise Value: INR {base_dcf_ev/1e7:,.2f} Cr")
print(f"EV/EBITDA ({multiple}x) Implied EV: INR {implied_ev_multiple/1e7:,.2f} Cr")