import numpy as np

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

def calculate_cagr(cfs, user_override=None):
    if user_override is not None:
        return user_override
    if len(cfs) < 2:
        return None
    start = cfs[0]
    end = cfs[-1]
    if start <= 0 or end <= 0:
        return None
    n = len(cfs) - 1
    cagr = (end / start) ** (1 / n) - 1
    return cagr

def project_cash_flows(last_cf, growth_rate, years):
    if growth_rate is None:
        return [last_cf for _ in range(years)]
    return [last_cf * ((1 + growth_rate) ** i) for i in range(1, years + 1)]

def calculate_terminal_value(last_cf, discount_rate, terminal_growth=None, terminal_multiple=None):
    if terminal_multiple:
        return last_cf * terminal_multiple
    if terminal_growth is not None and discount_rate > terminal_growth:
        return last_cf * (1 + terminal_growth) / (discount_rate - terminal_growth)
    raise ValueError("Invalid terminal value parameters.")

def discount_cash_flows(cash_flows, discount_rate):
    pvs = []
    for t, cf in enumerate(cash_flows):
        pv = cf / (1 + discount_rate) ** (t + 1)
        pvs.append(pv)
    return pvs
