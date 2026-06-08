# Algorithmic Volume Breakout Scanner

A Python-based time-series analysis tool that scans five years of historical stock data and automatically identifies the dates when a volume-driven breakout occurred.

---

## The Problem

Raw stock price and volume data is noisy. Looking at daily price movement alone gives an unclear picture — prices fluctuate constantly without any meaningful signal.

In technical analysis, a breakout is considered significant when trading volume spikes well above its recent average. A sudden price move on 3× normal volume carries far more weight than the same move on average volume. This scanner finds those dates automatically, for any stock you choose.

---

## How It Works

1. Data Extraction & Caching

The scanner takes a stock ticker as input at runtime and appends .NS automatically for NSE-listed stocks. Historical OHLCV data is pulled using yfinance for the period 2021–2026.

To avoid repeated downloads, the script checks if a local CSV already exists for that ticker using Python's os module. If it does, the cached file is loaded directly. If not, fresh data is downloaded and saved locally before proceeding. Each ticker saves to its own file so multiple stocks don't overwrite each other.

2. Cleaning

Only closing price and volume are retained. Rows with null values and days with zero trading volume — market holidays recorded incorrectly — are dropped before any calculations are done.

3. Signal Calculation

Since raw daily prices and volumes carry a lot of noise, a 20-day Simple Moving Average (SMA) is computed for both price and volume using pandas .rolling(20).mean(). This smooths out short-term fluctuations and creates a stable baseline.

A breakout is flagged on any day where:

Volume > 3 × 20-Day Volume SMA
This means trading activity was at least 3× above its recent average — a strong signal that something significant drove that session. The flagged dates are extracted into a separate dataframe with a Vol_increase_by column showing exactly how many times above average the volume was.

4. Visualization

The scanner produces a twin y-axis chart using matplotlib:

- Left axis — Daily closing price and 20-day Price SMA
- Right axis — 20-day Volume SMA (in millions)
- Breakout triggers — overlaid as red scatter points directly on the price line, so you can immediately see whether each breakout pushed price up or down

---

## Tech Stack

- Python
- pandas
- NumPy
- matplotlib
- yfinance

---

## How to Run

Install dependencies:

    pip install -r requirements.txt

Run the scanner:

    python scanner.py
When prompted, enter any NSE stock ticker without the .NS suffix:

Enter the stock ticker for which you want to detect the breakouts: TCS
The script handles the .NS suffix automatically. On first run, data is downloaded and cached locally. On subsequent runs for the same ticker, the cached file is used directly.

---

## Limitations

The 3× volume threshold is a fixed heuristic. It works well for large-cap stocks like TCS with stable average volumes but may need tuning for mid or small-cap stocks where volume is more erratic by nature. This is a historical scanner, not a predictor — it identifies when breakouts happened, not whether the price moved favourably afterward.