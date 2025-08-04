# DCF_Valuation_For_Stock_Target_Price

**A robust, professional-grade Python CLI tool for Discounted Cash Flow (DCF) stock valuation.**  
This tool provides comprehensive, transparent, and customizable DCF analysis for both casual investors and financial professionals.

---

## 🚀 Features

- **Accurate DCF Valuation:** Calculates intrinsic stock value using Free Cash Flow, with robust fallback logic (Operating Cash Flow - CapEx, Net Income).
- **Outlier Handling:** Automatically detects and removes outlier cash flow years for more realistic growth estimates.
- **Growth Rate Calculation:** Computes FCF CAGR or allows user override.
- **Flexible Terminal Value:** Supports both perpetual growth and terminal multiple methods.
- **Sensitivity Analysis:** Interactive tables show valuation impact across discount and terminal growth rates.
- **Data Provenance:** Clearly reports all data sources and fallback logic.
- **Comprehensive Output:** Step-by-step explanations, tabular breakdowns, warnings, recommendations, and visualizations.
- **CSV Export:** Save detailed results for further analysis.
- **Charting:** Visualizes projected cash flows and present values.
- **CLI & Scripting:** All features accessible from the command line for integration into research pipelines or investment dashboards.

---

## 🗂️ Folder Structure

```
dcf_valuation/
│
├── dcf/
│   ├── __init__.py
│   ├── data.py           # Data fetching and validation
│   ├── calculations.py   # DCF math & projections
│   ├── output.py         # Formatting, tables, charts, CSV
│   └── cli.py            # CLI argument parsing
│
├── main.py               # CLI entry point
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation

**Python 3.8+ is required.**

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/dcf_valuation.git
    cd dcf_valuation
    ```

2. **Set up the Python environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚡ Quick Start Example

```bash
python main.py AAPL --discount-rate 0.1 --projection-years 5 --terminal-type g --terminal-growth 0.03 --plot-graphs
```

---

## 🧑‍💻 Usage and CLI Options

Run `python main.py --help` for all options.

| Argument                 | Description                                                                                 | Example                       |
|--------------------------|---------------------------------------------------------------------------------------------|-------------------------------|
| `ticker`                 | Stock ticker symbol (required)                                                              | `AAPL`                        |
| `--discount-rate`        | Discount rate, as decimal                                                                   | `0.1` for 10%                 |
| `--projection-years`     | Years to project FCF (minimum 3 recommended)                                                | `5`                           |
| `--terminal-type`        | Terminal value method: `g` for perpetual growth, `m` for FCF multiple                      | `g` or `m`                    |
| `--terminal-growth`      | Terminal growth rate (required if using `g`)                                                | `0.03`                        |
| `--terminal-multiple`    | Terminal FCF multiple (required if using `m`)                                               | `15`                          |
| `--user-growth-override` | Manually override calculated FCF CAGR (decimal, optional)                                   | `0.05`                        |
| `--summary`              | Show summary output only (default is detailed breakdown)                                    | `--summary`                   |
| `--export-csv`           | Save valuation results to CSV                                                               | `--export-csv`                |
| `--csv-path`             | Path to CSV output                                                                          | `results.csv`                 |
| `--plot-graphs`          | Show chart of projected FCF and PV                                                          | `--plot-graphs`               |

---

## 📖 Example Workflows

### **Full, Verbose Valuation with Charts**
```bash
python main.py MSFT --discount-rate 0.09 --projection-years 6 --terminal-type g --terminal-growth 0.025 --plot-graphs
```

### **Summary Output, Custom Growth, Multiple Terminal Value**
```bash
python main.py TSLA --discount-rate 0.12 --projection-years 5 --terminal-type m --terminal-multiple 18 --user-growth-override 0.22 --summary
```

### **Export to CSV for Analysis**
```bash
python main.py V --discount-rate 0.08 --projection-years 7 --terminal-type g --terminal-growth 0.028 --export-csv --csv-path visa_dcf.csv
```

---

## 📊 Output Details

### **Verbose Mode (Default)**

- **Assumptions:** All user inputs and detected data, with explanations
- **Historical Free Cash Flows:** Tabular, with outlier notes and fallback explanations
- **Growth Rate:** Calculated CAGR or user override
- **Projections:** Year-by-year FCF projections
- **DCF Calculation:** Full table showing FCF, PV, present value sum, terminal value, and equity value
- **Sensitivity Table:** Price per share for a range of discount and terminal growth rates
- **Warnings/Recommendations:** Data caveats, suggestions, fallback usage
- **Export/Visualization:** CSV file path and chart shown if requested

### **Summary Mode**

- Condensed snapshot of intrinsic value, sensitivity table, and key warnings.

---

## 🧠 How It Works

1. **Data Fetching:** Financials (FCFs, shares outstanding, debts) pulled via [yfinance](https://github.com/ranaroussi/yfinance).
2. **Cleaning:** Outliers in FCF history are automatically detected/removed.
3. **Growth Rate:** By default, calculated as CAGR of (cleaned) FCFs. You can override this.
4. **Projection:** Next N years of FCF are projected using the growth rate.
5. **Terminal Value:** Choose perpetual growth or terminal multiple method.
6. **Discounting:** All future cash flows and terminal value are discounted to present value.
7. **Valuation:** Adds up discounted cash flows, subtracts net debt, divides by shares outstanding.
8. **Sensitivity:** Valuation recalculated for a grid of discount/terminal growth rates, shown in table.
9. **Output:** All steps, calculations, and warnings are clearly presented. Optional CSV/chart export.

---

## 🏆 Best Practices & Recommendations

- **Always review the warnings.** If fallback data is used or outliers removed, check the reasonableness of results.
- **Sensitivity analysis** is your friend: see how robust your valuation is to small changes in assumptions.
- **Override the growth rate** if you have a strong thesis the future will differ from the past.
- **Use the CSV export** to compare multiple companies or scenarios in Excel/Sheets.
- **Visualize** with the built-in chart for intuition.
- **Keep Python and dependencies up to date** for best data and security.

---

## ⚙️ Customization & Extension

- **Change outlier thresholds:** Edit `dcf/data.py` and `dcf/calculations.py` for stricter/looser filtering.
- **Add new output formats:** Enhance `dcf/output.py` for PDF, HTML, or Excel.
- **Plug in alternative data sources:** Swap out `yfinance` calls in `dcf/data.py`.
- **Batch or automated runs:** Integrate with your own scripts or research pipeline.

---

## 🛡️ Limitations

- Relies on public financial data. Always double-check results versus primary sources.
- Only as accurate as the underlying assumptions (growth, terminal value, discount rate).
- Does not model debt/equity raises, buybacks, or other advanced scenarios.

---

## 🧑‍🔬 For Developers

- Modular, PEP8-compliant codebase
- Add new valuation models easily (see `dcf/calculations.py`)
- CLI interface is argparse-based for easy extension
- PRs and feature requests are welcome!

---

## 📝 License

MIT License

---

## 🤝 Contributing

1. Fork this repo
2. Create a feature branch (`git checkout -b my-feature`)
3. Commit your changes
4. Push and open a PR

For questions, open an issue or contact the maintainer.

---

## 🙋 FAQ

**Q: Why does the tool sometimes use Net Income instead of FCF?**  
A: If Free Cash Flow is missing, we fall back to Operating Cash Flow minus CapEx, then Net Income as a last resort. Any fallback is clearly reported in the output.

**Q: Can I run this for non-US tickers?**  
A: Yes! The tool detects currency from the ticker and reports all numbers in that currency.

**Q: Can I use this as a Python library?**  
A: Yes! Import modules from `dcf/` into your own scripts for custom workflows.

---

## 📬 Contact

Maintainer: [Mohith Sai Gorla](mohithsaigorla4@email.com)

---

Happy Valuing! 🚀
