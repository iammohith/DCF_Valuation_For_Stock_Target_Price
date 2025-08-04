import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Comprehensive DCF Stock Valuation CLI"
    )
    parser.add_argument("ticker", type=str, help="Ticker symbol (e.g., AAPL)")
    parser.add_argument("--discount-rate", type=float, default=0.1, help="Discount rate (e.g., 0.1 for 10%)")
    parser.add_argument("--projection-years", type=int, default=5, help="Number of years for projection (min 3)")
    parser.add_argument("--terminal-type", type=str, choices=["g", "m"], default="g", help="Terminal value method: growth (g) or multiple (m)")
    parser.add_argument("--terminal-growth", type=float, default=0.03, help="Terminal growth rate (e.g., 0.03 for 3%)")
    parser.add_argument("--terminal-multiple", type=float, default=None, help="Terminal FCF multiple (if using multiple method)")
    parser.add_argument("--user-growth-override", type=float, default=None, help="Override calculated growth rate (e.g., 0.05)")
    parser.add_argument("--summary", action="store_true", help="Summary output only")
    parser.add_argument("--export-csv", action="store_true", help="Export results to CSV")
    parser.add_argument("--csv-path", type=str, default="dcf_results.csv", help="CSV file path")
    parser.add_argument("--plot-graphs", action="store_true", help="Show FCF/PV chart")
    return parser.parse_args()
