import os
import matplotlib.pyplot as plt
import csv

def print_table(title, rows, headers=None, note=None):
    print(f"\n{title}\n{'='*len(title)}")
    if headers:
        hfmt = "|".join([f" {{:<{max(len(h), 20)}}} " for h in headers])
        print(hfmt.format(*headers))
        print("-" * (len(headers) * 24))
    for row in rows:
        print("".join([f"{str(col):>{20}} " for col in row]))
    if note:
        print(f"\n*Note: {note}")

def print_verbose_output(data, calc, dcf, sensitivity, args):
    print(f"\nWelcome to the Enhanced DCF Stock Valuation Tool!")
    print("-"*49)
    print(f"Company: {data['company_name']} ({args.ticker})")
    print(f"Currency: {data['currency']}\n")
    # Assumptions
    print("="*30)
    print("Assumptions & User Inputs")
    print("="*30)
    print(f"Discount Rate:        {args.discount_rate*100:.2f}%")
    print(f"Projection Years:     {args.projection_years}")
    if args.terminal_multiple is not None:
        print(f"Terminal Value:       {args.terminal_multiple}x Final Year FCF")
    else:
        print(f"Terminal Growth:      {args.terminal_growth*100:.2f}%")
    if args.user_growth_override is not None:
        print(f"User Growth Override: {args.user_growth_override*100:.2f}%")
    else:
        print(f"User Growth Override: Not used (calculated from data)")
    print(f"Shares Outstanding:   {data['shares_out']:,}")
    print(f"Net Debt:             {data['currency']} {data['net_debt']:,.0f}")
    # Historical Cash Flows
    hist_rows = [(y, f"{cf:,.0f}") for y, cf in zip(data['historical_years'], data['historical_cfs'])]
    print_table("Historical Cash Flows (Source: "+data['cf_source']+")", hist_rows, headers=["Year", f"FCF ({data['currency']})"])
    if dcf.get("outliers"):
        print(f"\n*Note: Outliers removed: {', '.join([f'{o:,.0f}' for o in dcf['outliers']])}")
    else:
        print("\n*Note: Data from the last", len(data['historical_cfs']), "years was used. No outliers detected. All cash flows positive.")
    if dcf['growth_rate'] is not None:
        print(f"\nCalculated CAGR (FCF Growth): {dcf['growth_rate']*100:.2f}% per year")
    else:
        print("\nWarning: Not enough valid historical cash flow data to estimate growth rate. Projections assume no growth.")
    # Projected FCF
    proj_rows = [(str(i+1), f"{cf:,.0f}") for i, cf in enumerate(dcf['cash_flows'])]
    print_table("Projected Free Cash Flows", proj_rows, headers=["Year", f"Projected FCF ({data['currency']})"])
    # DCF Table
    dcf_rows = [(yr, f"{cf:,.0f}", f"{pv:,.0f}") for yr, cf, pv in dcf['pv_details']]
    print_table("Discounted Cash Flow Calculation", dcf_rows, headers=["Year", "Projected FCF", f"Present Value ({data['currency']})"])
    print(f"\nSum of Present Values (Years 1-{args.projection_years}): {data['currency']} {dcf['present_value']:,.0f}")
    print(f"\nTerminal Value (Year {args.projection_years}, at {args.terminal_growth*100:.2f}% perpetual growth): {data['currency']} {dcf['terminal_value']:,.0f}")
    print(f"Present Value of Terminal Value: {data['currency']} {dcf['pv_terminal']:,.0f}")
    print(f"\nEnterprise Value (Sum): {data['currency']} {dcf['enterprise_value']:,.0f}")
    print(f"Less Net Debt: {data['currency']} {data['net_debt']:,.0f}")
    print(f"Equity Value: {data['currency']} {dcf['equity_value']:,.0f}")
    print(f"\nIntrinsic Value per Share: {data['currency']} {dcf['price_per_share']:,.2f}")
    # Sensitivity
    print("\n"+"="*30)
    print("Sensitivity Analysis Table")
    print("="*30)
    print("This table shows how the value per share changes with different discount and terminal growth rates.\n")
    header_row = [""] + [f"Terminal {tg*100:.1f}%" for tg in sensitivity['tgs']]
    print(" | ".join(header_row))
    for i, dr in enumerate(sensitivity['drs']):
        row = [f"DR {dr*100:.1f}%"]
        for j, tg in enumerate(sensitivity['tgs']):
            pps = sensitivity['table'][i][j]
            row.append(f"{data['currency']} {pps:,.2f}" if not isinstance(pps, str) and not (pps is None or pps != pps) else "N/A")
        print(" | ".join(row))
    # Warnings and recommendations
    print("\n"+"="*30)
    print("Warnings & Recommendations")
    print("="*30)
    if dcf.get("outliers"):
        print("- Outliers in historical cash flows were removed for CAGR calculation.")
    if data.get("fallback_used"):
        print(f"- Fallback used: {data['fallback_used']}. Consider reviewing the appropriateness of this proxy.")
    if data.get("warnings"):
        for w in data["warnings"]:
            print("-", w)
    else:
        print("- No major issues detected in data. Calculations use reported values.")
    print("- If you believe growth will differ from history, consider using the override option.")
    print("- Sensitivity analysis helps you see how results change with small changes in key assumptions.")
    # Export and visualization
    print("\n"+"="*30)
    print("Export & Visualization")
    print("="*30)
    if args.export_csv:
        print(f"- Results exported as CSV to {os.path.abspath(args.csv_path)}")
    if args.plot_graphs:
        print("- Chart visualizing projected cash flows and their present values is displayed below.")
    print("\nThank you for using the Enhanced DCF Calculator!\n")

def print_summary_output(data, dcf, sensitivity, args):
    print(f"\nDCF SUMMARY for {data['company_name']} ({args.ticker}) in {data['currency']}")
    print("-" * 44)
    print(f"Value per Share: {data['currency']} {dcf['price_per_share']:,.2f}")
    print(f"Discount Rate: {args.discount_rate*100:.2f}%")
    if args.terminal_multiple is not None:
        print(f"Terminal Value: {args.terminal_multiple}x FCF")
    else:
        print(f"Terminal Growth: {args.terminal_growth*100:.2f}%")
    print(f"FCF CAGR (used): {dcf['growth_rate']*100:.2f}%" if dcf['growth_rate'] is not None else "FCF growth: flat")
    print(f"Net Debt: {data['currency']} {data['net_debt']:,.0f}")
    print(f"Cash Flows sourced from: {data['cf_source']}")
    print("\nSensitivity Table (price per share):")
    print(f"{'':>12}", end=" | ")
    for tg in sensitivity['tgs']:
        print(f"Terminal {tg*100:.1f}%", end=" | ")
    print()
    for i, dr in enumerate(sensitivity['drs']):
        print(f"DR {dr*100:.1f}%", end=" | ")
        for j, tg in enumerate(sensitivity['tgs']):
            pps = sensitivity['table'][i][j]
            print(f"{data['currency']} {pps:,.2f}" if not isinstance(pps, str) and not (pps is None or pps != pps) else "N/A", end=" | ")
        print()
    if data.get("warnings"):
        print("\nWarnings:")
        for w in data["warnings"]:
            print(" -", w)
    print("-" * 44)
    if args.export_csv:
        print(f"Results exported to {os.path.abspath(args.csv_path)}")
    if args.plot_graphs:
        print("Chart visualizing projected cash flows and present values shown below.")

def export_to_csv(pv_details, terminal_value, pv_terminal, price_per_share, csv_path):
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Projected FCF", "Present Value"])
        for yr, cf, pv in pv_details:
            writer.writerow([yr, cf, pv])
        writer.writerow(["Terminal Value", terminal_value, pv_terminal])
        writer.writerow(["Intrinsic Value per Share", price_per_share])

def plot_fcf_chart(cash_flows, pvs, years, company_name, ticker, currency):
    plt.figure(figsize=(10, 6))
    plt.bar(years, cash_flows, alpha=0.6, label='Projected FCF')
    plt.plot(years, pvs, color='red', marker='o', label='Present Value')
    plt.xlabel('Year')
    plt.ylabel(f'Cash Flow ({currency})')
    plt.title(f'DCF for {company_name} ({ticker.upper()})')
    plt.legend()
    plt.tight_layout()
    plt.show()
