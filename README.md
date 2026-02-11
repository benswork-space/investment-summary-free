# Daily Investment Briefing

An automated daily email that summarizes what happened in the markets that matters to **your** portfolio. It fetches price data and news after NYSE close, uses Claude to synthesize a concise briefing, and emails it to you.

## How It Works

1. **Market data** — pulls closing prices and volume via Yahoo Finance for every ticker in your portfolio.
2. **News** — aggregates headlines from Google News RSS (and optionally NewsAPI) for your tickers and interest areas.
3. **Synthesis** — sends the raw data to Claude, which returns a structured briefing covering only meaningful moves (>2% swings, earnings, macro events, etc.). Quiet days produce short emails.
4. **Email** — renders the briefing as a clean HTML email and sends it via Gmail SMTP.

Runs automatically Monday–Friday at 4:30 PM EST via GitHub Actions.

## Setup

### 1. Configure Your Portfolio and Interests

Edit **`src/config.py`** — this is where you personalize the briefing:

```python
# Add your tickers and their metadata
PORTFOLIO = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology"},
    "MSFT": {"name": "Microsoft", "sector": "Technology"},
    "VTI":  {"name": "Vanguard Total Stock Market ETF", "sector": "Market Index"},
    # ... add as many as you like
}

# Topics you want industry-level news coverage for
INTEREST_AREAS = [
    "US Tech",
    "Clean Energy",
    "Semiconductors",
    # ... add your areas of interest
]

# The email address that receives the daily briefing
EMAIL_RECIPIENT = "you@example.com"
```

### 2. Set Up Credentials

You need three required credentials (and one optional):

| Secret | Required | Where to get it |
|--------|----------|----------------|
| `ANTHROPIC_API_KEY` | Yes | [Anthropic Console](https://console.anthropic.com/settings/keys) |
| `GMAIL_ADDRESS` | Yes | The Gmail address that will *send* the briefing |
| `GMAIL_APP_PASSWORD` | Yes | [Google App Passwords](https://myaccount.google.com/apppasswords) (not your normal password) |
| `NEWSAPI_KEY` | No | [NewsAPI](https://newsapi.org/register) — enhances news coverage, but the app works without it |

**For local development**, copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

**For GitHub Actions** (recommended for daily automation), add each secret under your repo's **Settings > Secrets and variables > Actions**.

### 3. Install and Run Locally

```bash
pip install -r requirements.txt
python main.py
```

### 4. Enable GitHub Actions

The included workflow (`.github/workflows/daily-briefing.yml`) runs automatically at 4:30 PM EST, Monday–Friday. After adding your secrets to the repo, it will just work. You can also trigger it manually from the Actions tab.

## Project Structure

```
├── main.py                  # Entry point
├── src/
│   ├── config.py            # Portfolio, interests, and credentials
│   ├── market_data.py       # Yahoo Finance price fetcher
│   ├── news.py              # Google News RSS + NewsAPI fetcher
│   ├── synthesis.py         # Claude-powered briefing generation
│   ├── email_sender.py      # Gmail SMTP sender
│   └── template.py          # HTML email renderer
├── .env.example             # Environment variable template
├── .github/workflows/
│   └── daily-briefing.yml   # Scheduled GitHub Actions workflow
└── requirements.txt
```

## Requirements

- Python 3.11+
- An Anthropic API key (Claude)
- A Gmail account with an App Password

## License

MIT
