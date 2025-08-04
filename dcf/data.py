import yfinance as yf
import math
import numpy as np

def detect_currency(ticker_obj):
    return ticker_obj.info.get("currency", "USD")

def remove_outliers(data, threshold=2.0):
    arr = np.array(data)
    mean = np.nanmean(arr)
    std = np.nanstd(arr)
    if std == 0 or np.isnan(std):
        return arr.tolist(), []
    z_scores = (arr - mean) / std
    filtered = arr[np.abs(z_scores) < threshold]
    outliers = arr[np.abs(z_scores) >= threshold]
    return filtered.tolist(), outliers.tolist()

def get_valid_years(values, years):
    pairs = [(y, v) for y, v in zip(years, values) if v is not None and not (isinstance(v, float) and math.isnan(v))]
    if not pairs:
        return [], []
    years, values = zip(*pairs)
    return list(years), list(values)

def fetch_financials(ticker, min_years=3):
    ticker_obj = yf.Ticker(ticker)
    currency = detect_currency(ticker_obj)
    shares_out = ticker_obj.info.get("sharesOutstanding", 0)
    company_name = ticker_obj.info.get("shortName", ticker)
    net_debt = _get_net_debt(ticker_obj)

    cf_statement = ticker_obj.get_cashflow()
    annual_dates = list(cf_statement.columns.strftime("%Y")) if cf_statement is not None and not cf_statement.empty else []
    historical_cfs = []
    historical_years = []
    cf_source = ""
    warnings = []
    fallback_used = None

    # Try FreeCashFlow
    if cf_statement is not None and not cf_statement.empty:
        if "FreeCashFlow" in cf_statement.index:
            fcf = cf_statement.loc["FreeCashFlow"]
            values = [float(fcf.iloc[i]) if fcf.iloc[i] is not None and not (isinstance(fcf.iloc[i], float) and math.isnan(fcf.iloc[i])) else None for i in range(len(fcf))]
            years, values = get_valid_years(values, annual_dates)
            if len(values) >= min_years:
                historical_cfs = values[::-1]
                historical_years = years[::-1]
                cf_source = "FreeCashFlow"
        # Fallback to OperatingCashFlow - CapitalExpenditure
        if not historical_cfs and "OperatingCashFlow" in cf_statement.index and "CapitalExpenditure" in cf_statement.index:
            op_cf = cf_statement.loc["OperatingCashFlow"]
            capex = cf_statement.loc["CapitalExpenditure"]
            fcf = op_cf - capex
            values = [float(fcf.iloc[i]) if fcf.iloc[i] is not None and not (isinstance(fcf.iloc[i], float) and math.isnan(fcf.iloc[i])) else None for i in range(len(fcf))]
            years, values = get_valid_years(values, annual_dates)
            if len(values) >= min_years:
                historical_cfs = values[::-1]
                historical_years = years[::-1]
                cf_source = "OperatingCashFlow - CapitalExpenditure"
                fallback_used = "OperatingCashFlow - CapEx"
        # Fallback to Net Income (warn user)
        if not historical_cfs and "NetIncome" in cf_statement.index:
            net_income = cf_statement.loc["NetIncome"]
            values = [float(net_income.iloc[i]) if net_income.iloc[i] is not None and not (isinstance(net_income.iloc[i], float) and math.isnan(net_income.iloc[i])) else None for i in range(len(net_income))]
            years, values = get_valid_years(values, annual_dates)
            if len(values) >= min_years:
                historical_cfs = values[::-1]
                historical_years = years[::-1]
                cf_source = "NetIncome (Warning: Not FCF, use with caution!)"
                fallback_used = "NetIncome"
                warnings.append("Used Net Income as cash flow proxy (FCF unavailable). Results may be less reliable.")
        if not historical_cfs:
            warnings.append("No valid FCF, Operating Cash Flow, or Net Income found in cash flow statement.")
    else:
        warnings.append("No cash flow statement data found.")
    return {
        "currency": currency,
        "shares_out": shares_out,
        "company_name": company_name,
        "net_debt": net_debt,
        "historical_cfs": historical_cfs,
        "historical_years": historical_years,
        "cf_source": cf_source,
        "fallback_used": fallback_used,
        "warnings": warnings,
    }

def _get_net_debt(ticker_obj):
    bs = ticker_obj.get_balance_sheet()
    if bs is not None and not bs.empty:
        try:
            total_debt = float(bs.loc.get("Long Term Debt", 0)) + float(bs.loc.get("Short Long Term Debt", 0))
            cash = float(bs.loc.get("Cash", 0))
            return total_debt - cash
        except Exception:
            return 0
    return 0
