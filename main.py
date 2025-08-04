from dcf.cli import parse_args
from dcf.data import fetch_financials, remove_outliers
from dcf.calculations import calculate_cagr, project_cash_flows, calculate_terminal_value, discount_cash_flows
from dcf.output import print_verbose_output, print_summary_output, export_to_csv, plot_fcf_chart

def main():
    args = parse_args()
    fin = fetch_financials(args.ticker)
    if not fin["historical_cfs"] or fin["shares_out"] == 0:
        print("Not enough valid data to perform DCF.")
        return

    # Outlier removal
    filtered_cfs, outliers = remove_outliers(fin["historical_cfs"])
    # Growth calculation
    growth_rate = calculate_cagr(filtered_cfs, args.user_growth_override)
    # Projections
    last_cf = filtered_cfs[-1] if filtered_cfs else fin["historical_cfs"][-1]
    cash_flows = project_cash_flows(last_cf, growth_rate, args.projection_years)
    # DCF math
    pvs = discount_cash_flows(cash_flows, args.discount_rate)
    pv_details = [(i+1, cf, pv) for i, (cf, pv) in enumerate(zip(cash_flows, pvs))]
    present_value = sum(pvs)
    # Terminal value
    terminal_value = calculate_terminal_value(cash_flows[-1], args.discount_rate, terminal_growth=args.terminal_growth if args.terminal_type=="g" else None, terminal_multiple=args.terminal_multiple if args.terminal_type=="m" else None)
    pv_terminal = terminal_value / (1 + args.discount_rate) ** len(cash_flows)
    enterprise_value = present_value + pv_terminal
    equity_value = enterprise_value - fin["net_debt"]
    price_per_share = equity_value / fin["shares_out"]

    # Sensitivity table
    drs = [args.discount_rate - 0.01, args.discount_rate, args.discount_rate + 0.01]
    tgs = [args.terminal_growth - 0.01, args.terminal_growth, args.terminal_growth + 0.01]
    table = []
    for dr in drs:
        row = []
        for tg in tgs:
            try:
                tv = calculate_terminal_value(cash_flows[-1], dr, terminal_growth=tg)
                pv_tv = tv / (1 + dr) ** len(cash_flows)
                ev = present_value + pv_tv
                eqv = ev - fin["net_debt"]
                pps = eqv / fin["shares_out"]
                row.append(pps)
            except Exception:
                row.append("N/A")
        table.append(row)
    sensitivity = {"drs": drs, "tgs": tgs, "table": table}

    dcf = {
        "outliers": outliers,
        "growth_rate": growth_rate,
        "cash_flows": cash_flows,
        "pv_details": pv_details,
        "present_value": present_value,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "price_per_share": price_per_share,
        "net_debt": fin["net_debt"],
    }

    if args.export_csv:
        export_to_csv(pv_details, terminal_value, pv_terminal, price_per_share, args.csv_path)
    if args.plot_graphs:
        plot_fcf_chart(cash_flows, [pv for _, _, pv in pv_details], list(range(1, args.projection_years + 1)), fin["company_name"], args.ticker, fin["currency"])

    if args.summary:
        print_summary_output(fin, dcf, sensitivity, args)
    else:
        print_verbose_output(fin, dcf, dcf, sensitivity, args)

if __name__ == "__main__":
    main()
