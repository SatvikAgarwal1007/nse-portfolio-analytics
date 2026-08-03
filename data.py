import yfinance as yf
import pandas as pd
import os

TICKERS = ["DLF.NS", "MEESHO.NS", "AXISBANK.NS", "SUMICHEM.NS", "TATAPOWER.NS", "SWIGGY.NS", "WIPRO.NS", "DLF.NS", "MCLOUD.NS", "ANGELONE.NS","URBANCO.NS"]

def fetch_data(tickers, start_date, end_date):
    raw_data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True) #auto adjust fixes price for splits and dividends
    prices = raw_data['Close']
    return prices

prices = fetch_data(TICKERS, "2025-08-01", "2026-08-01")
print(prices.tail())
print(prices.isna().sum()) #checks amount of empty columns (cuz meesho and urban co are new listings)
print(prices.apply(lambda col: col.first_valid_index()))

returns = prices.pct_change() #percentage change calculation
print(returns.head())

vol = returns.std() * (252 ** 0.5) # multiplying by square root of 252 to annualize the volatility
                                    # square root of 252 is used because there are approximately 252 trading days in a year and volatility moves proportional to the square root of time. This is a common practice in finance to annualize daily volatility.
print(vol.sort_values(ascending=False)) 

def load_weights():
    path = "holdings.csv" if os.path.exists("holdings.csv") else "holdings_example.csv"
    print(f"Using: {path}")
    values = pd.read_csv(path, index_col="ticker")["value"]
    return values / values.sum()

weights = load_weights()
print((weights * 100).round(1).sort_values(ascending=False))


corr = returns.corr() #correlation matrix
corr.round(2).to_csv("correlations.csv") #write correlation matrix to csv file
print(corr.__round__(2)) #rounding to 2 decimal places

nifty = yf.download("^NSEI", start="2025-08-01", end="2026-08-01", auto_adjust=True)["Close"]
market_returns = nifty.pct_change()

betas = {}

for t in returns.columns:
    joined = pd.concat([returns[t], market_returns], axis=1).dropna()
    betas[t] = joined.cov().iloc[0, 1] / joined.iloc[:, 1].var() #covariance of stock and market divided by variance of market

print(pd.Series(betas).sort_values(ascending=False)) #printing betas of all stocks sorted in descending order



#stress testing the portfolio by simulating a market crash of 10%

b = pd.Series(betas)
portfolio_beta = (weights * b).sum()
print(f"Portfolio beta: {portfolio_beta:.2f}")
print(f"If Nifty falls 10%, portfolio falls ~{portfolio_beta * 10:.1f}%")