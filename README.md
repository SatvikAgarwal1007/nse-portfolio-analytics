# nse-portfolio-analytics

Risk analytics for a portfolio of NSE-listed equities. Computes annualised volatility, the correlation structure across holdings, and beta against the Nifty 50 — then uses those to estimate how the portfolio behaves in a market drawdown.

Built from scratch with pandas and yfinance to understand how the standard portfolio risk measures actually work, rather than reading them off a broker's app.

---

## What it does

| Measure | Question it answers |
|---|---|
| **Annualised volatility** | How far does each stock typically swing in a year? |
| **Correlation matrix** | Which holdings move together, and which are independent? |
| **Beta vs Nifty 50** | How much of a stock's movement comes from the market itself? |
| **Portfolio beta** | If the index falls 10%, roughly what happens to the whole book? |

---

## Findings

Ten NSE-listed stocks, daily closes from August 2025 to August 2026, split- and dividend-adjusted.

### 1. Volatility spans a 3x range

| Stock | Annualised volatility |
|---|---|
| MCLOUD | 69% |
| MEESHO | 59% |
| URBANCO | 43% |
| ANGELONE | 41% |
| SWIGGY | 38% |
| SUMICHEM | 36% |
| DLF | 29% |
| WIPRO | 25% |
| AXISBANK | 24% |
| TATAPOWER | 21% |

The most volatile holding swings more than three times as hard as the calmest. Equal position sizes therefore do **not** mean equal risk contribution — a point that only becomes visible once you weight each position by its own volatility.

### 2. The diversification was the opposite of what I expected

My prior was that the three consumer-internet holdings (Swiggy, Meesho, Urban Company) were effectively one bet in three names, since they share a business model and an investor narrative.

The data disagreed:

- Swiggy ↔ Meesho: **0.12**
- Meesho ↔ Urban Company: **0.16**
- Swiggy ↔ Urban Company: **0.34**

Those are low. The genuine cluster is among the established, index-heavy names, with DLF at the centre:

- DLF ↔ Angel One: **0.54**
- DLF ↔ Axis Bank: **0.52**
- DLF ↔ Tata Power: **0.49**
- DLF ↔ Sumichem: **0.45**

Meesho is close to uncorrelated with everything in the book (0.02 with Sumichem, 0.03 with Tata Power, **−0.07** with Wipro).

**The lesson:** shared narrative is not shared risk. The stocks that felt like one bet were independent; the stocks that felt safe moved as a bloc.

### 3. Volatility and beta measure different things

| Stock | Volatility | Beta |
|---|---|---|
| ANGELONE | 41% | 1.74 |
| DLF | 29% | 1.71 |
| MCLOUD | 69% | 1.36 |
| SWIGGY | 38% | 1.23 |
| AXISBANK | 24% | 1.21 |
| SUMICHEM | 36% | 1.17 |
| URBANCO | 43% | 0.96 |
| TATAPOWER | 21% | 0.78 |
| WIPRO | 25% | 0.72 |
| MEESHO | 59% | 0.50 |

Meesho has the second-highest volatility and the lowest beta: it moves a great deal, but almost none of that movement comes from the market. MCLOUD is similar — very high total volatility, moderate market sensitivity, low correlation with everything else.

Angel One's 1.74 has a clean economic explanation: it is a retail broker, so its revenue *is* market activity. It is the index, geared up.

### 4. Portfolio-level result

Weighting each beta by position size gives a portfolio beta of approximately **1.23**.

Six of the ten holdings have beta above 1, including both of the positions that intuitively felt like the "safe" part of the book. The portfolio is more market-sensitive than the index in both directions.

---

## Caveats

- Meesho (~157 trading days) and Urban Company (~214) listed part-way through the sample window. Their volatility, correlation and beta estimates rest on fewer observations and are correspondingly less stable. Newly listed stocks also tend to be unusually volatile early on.
- Missing values from pre-listing dates are **left as NaN, not filled**. Imputing them would invent prices for days on which the shares could not be bought at any price, and would silently corrupt every downstream calculation.
- Beta and correlation are backward-looking. They describe the sample period, not the future.
- A single year of daily data is a short sample for estimating any of these quantities.

---

## Running it

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install yfinance pandas
python data.py
```

Portfolio weights are read from `holdings.csv` if present, and otherwise fall back to `holdings_example.csv`. The committed example file contains **illustrative** weights, not real positions. All outputs are expressed as percentages and weights rather than currency amounts.

---

## Next

This is the data and risk layer of a larger project. The same price pipeline feeds a backtesting engine, where the risk measures above become the evaluation framework for a strategy rather than a description of a static book.