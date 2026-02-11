"""Daily investment briefing — fetches market data and news after NYSE close,
synthesises them with Claude, and emails a concise summary."""

from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

from src.config import EMAIL_RECIPIENT, PORTFOLIO, INTEREST_AREAS
from src.market_data import fetch_market_data
from src.news import fetch_news
from src.synthesis import synthesize_briefing
from src.email_sender import send_email
from src.template import render_email


def main():
    et = ZoneInfo("America/New_York")
    now = datetime.now(et)

    if now.weekday() >= 5:
        print("Market closed (weekend). Skipping.")
        return

    print("Fetching market data ...")
    market_data = fetch_market_data(PORTFOLIO)

    print("Fetching news ...")
    news = fetch_news(PORTFOLIO, INTEREST_AREAS)

    print("Synthesising briefing with Claude ...")
    briefing = synthesize_briefing(market_data, news, PORTFOLIO, INTEREST_AREAS)

    has_content = (
        briefing.get("assets")
        or briefing.get("industries")
        or briefing.get("macro")
    )
    if not has_content:
        print("No meaningful developments today. Skipping email.")
        return

    html = render_email(briefing, now)

    print(f"Sending email to {EMAIL_RECIPIENT} ...")
    send_email(
        to=EMAIL_RECIPIENT,
        subject=f"Investment Briefing — {now.strftime('%B %d, %Y')}",
        html=html,
    )
    print("Done.")


if __name__ == "__main__":
    main()
