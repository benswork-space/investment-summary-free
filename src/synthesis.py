import json

import anthropic


def synthesize_briefing(
    market_data: dict, news: dict, portfolio: dict, interest_areas: list
) -> dict:
    """Send market data + news to Claude and get a structured briefing back."""
    client = anthropic.Anthropic()

    prompt = f"""You are a concise, sharp investment analyst writing a daily briefing for a sophisticated individual investor.

TODAY'S MARKET DATA:
{_format_market_data(market_data)}

TODAY'S NEWS:
{_format_news(news)}

PORTFOLIO TICKERS: {', '.join(portfolio.keys())}
INTEREST AREAS: {', '.join(interest_areas)}

Write a daily investment briefing following these rules strictly:

1. ASSET UPDATES — Only include assets where something MEANINGFUL happened today:
   - Price move > 2% (up or down)
   - Significant news (earnings, regulatory, partnerships, management changes)
   - Unusual volume or trading activity
   - Important analyst actions
   If nothing meaningful happened, OMIT the asset entirely.

2. INDUSTRY SUMMARIES — Only include industries with a genuine directional signal
   or noteworthy development. Be pithy and directional. Skip quiet industries.

3. MACRO THEMES — Only include genuinely impactful macro developments
   (Fed decisions, major economic data, geopolitical events). Do not manufacture
   themes.

4. MARKET MOOD — One concise sentence capturing today's market character.

STYLE:
- Direct and conversational, not corporate
- No filler ("it's worth noting", "investors should be aware")
- Specific numbers and facts over vague statements
- Short sentences, no fluff
- If it's a quiet day, return mostly empty arrays — that is fine

Return ONLY valid JSON in this exact format:
{{
  "market_mood": "one sentence",
  "assets": [
    {{
      "ticker": "SYM",
      "name": "Company Name",
      "change_pct": 2.4,
      "direction": "up",
      "summary": "2-3 sentences max"
    }}
  ],
  "industries": [
    {{
      "name": "Industry Name",
      "direction": "bullish",
      "summary": "1-2 sentences"
    }}
  ],
  "macro": [
    {{
      "theme": "Theme Name",
      "summary": "1-2 sentences"
    }}
  ]
}}

direction for assets: "up" | "down" | "flat"
direction for industries: "bullish" | "bearish" | "neutral"
Use empty arrays [] for sections with no meaningful content."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        return json.loads(text.strip())

    except json.JSONDecodeError as e:
        print(f"Failed to parse Claude response: {e}")
        return _fallback()
    except Exception as e:
        print(f"Claude API error: {e}")
        return _fallback()


def _fallback() -> dict:
    return {
        "market_mood": "Unable to generate briefing today.",
        "assets": [],
        "industries": [],
        "macro": [],
    }


def _format_market_data(market_data: dict) -> str:
    lines = []
    for ticker, d in market_data.items():
        arrow = "▲" if d["change_pct"] > 0 else "▼" if d["change_pct"] < 0 else "—"
        lines.append(
            f"{ticker} ({d['name']}) | {d['sector']} | "
            f"${d['close']} {arrow} {d['change_pct']:+.2f}% | "
            f"Vol: {d['volume']:,}"
        )
    return "\n".join(lines) if lines else "No market data available."


def _format_news(news: dict) -> str:
    lines = []

    if news.get("tickers"):
        lines.append("=== TICKER NEWS ===")
        for ticker, articles in news["tickers"].items():
            lines.append(f"\n{ticker}:")
            for a in articles:
                lines.append(f"  - [{a.get('source', '?')}] {a.get('title', '')}")
                if a.get("description"):
                    lines.append(f"    {a['description'][:200]}")

    if news.get("industries"):
        lines.append("\n=== INDUSTRY NEWS ===")
        for area, articles in news["industries"].items():
            lines.append(f"\n{area}:")
            for a in articles:
                lines.append(f"  - [{a.get('source', '?')}] {a.get('title', '')}")

    return "\n".join(lines) if lines else "No news available."
