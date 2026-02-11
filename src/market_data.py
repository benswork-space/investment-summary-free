import yfinance as yf


def fetch_market_data(portfolio: dict) -> dict:
    """Fetch daily price data for all portfolio tickers."""
    tickers = list(portfolio.keys())
    data = {}

    ticker_str = " ".join(tickers)
    downloads = yf.download(ticker_str, period="5d", group_by="ticker", auto_adjust=True)

    for ticker in tickers:
        try:
            if len(tickers) > 1:
                ticker_data = downloads[ticker]
            else:
                ticker_data = downloads

            ticker_data = ticker_data.dropna()
            if len(ticker_data) < 2:
                continue

            latest = ticker_data.iloc[-1]
            previous = ticker_data.iloc[-2]

            close = float(latest["Close"])
            prev_close = float(previous["Close"])
            change_pct = ((close - prev_close) / prev_close) * 100
            volume = int(latest["Volume"]) if "Volume" in latest else 0

            data[ticker] = {
                "name": portfolio[ticker]["name"],
                "sector": portfolio[ticker]["sector"],
                "close": round(close, 2),
                "prev_close": round(prev_close, 2),
                "change_pct": round(change_pct, 2),
                "volume": volume,
            }
        except Exception as e:
            print(f"  Warning: could not fetch {ticker}: {e}")
            continue

    return data
