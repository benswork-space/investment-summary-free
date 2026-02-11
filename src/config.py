import os

PORTFOLIO = {
# your portfolio goes here
    "SPY": {"name": "S&P 500 ETF", "sector": "Market Index"},
}

INTEREST_AREAS = [
# your interests go here
    "US Tech",
]

# this is where you put your credentials
EMAIL_RECIPIENT = "example@youremail.com"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
