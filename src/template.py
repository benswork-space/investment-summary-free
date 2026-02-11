from datetime import datetime


def render_email(briefing: dict, date: datetime) -> str:
    """Turn a structured briefing dict into an HTML email."""
    date_str = date.strftime("%A, %B %d, %Y")
    mood = briefing.get("market_mood", "")
    assets_html = _render_assets(briefing.get("assets", []))
    industries_html = _render_industries(briefing.get("industries", []))
    macro_html = _render_macro(briefing.get("macro", []))

    mood_block = ""
    if mood:
        mood_block = f"""
        <tr>
          <td style="padding:20px 32px;border-bottom:1px solid #eee;">
            <p style="margin:0;color:#444;font-size:15px;line-height:1.5;font-style:italic;">
              {mood}
            </p>
          </td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background-color:#f5f5f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f5f5f5;padding:20px 0;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.1);">

  <!-- Header -->
  <tr>
    <td style="background-color:#1a1a2e;padding:24px 32px;">
      <h1 style="margin:0;color:#ffffff;font-size:20px;font-weight:600;letter-spacing:-0.3px;">
        Daily Investment Briefing
      </h1>
      <p style="margin:6px 0 0;color:#a0a0b0;font-size:13px;">{date_str}</p>
    </td>
  </tr>

  <!-- Market Mood -->
  {mood_block}

  <!-- Portfolio Updates -->
  {assets_html}

  <!-- Industry Outlook -->
  {industries_html}

  <!-- Macro Themes -->
  {macro_html}

  <!-- Footer -->
  <tr>
    <td style="padding:16px 32px;background-color:#fafafa;border-top:1px solid #eee;">
      <p style="margin:0;color:#999;font-size:11px;text-align:center;">
        Generated after NYSE close &middot; Not financial advice
      </p>
    </td>
  </tr>

</table>
</td></tr>
</table>
</body>
</html>"""


# -- helpers -----------------------------------------------------------------

_COLORS = {
    "up": "#16a34a",
    "bullish": "#16a34a",
    "down": "#dc2626",
    "bearish": "#dc2626",
}
_ARROWS = {
    "up": "&#9650;",
    "bullish": "&#9650;",
    "down": "&#9660;",
    "bearish": "&#9660;",
}


def _color(direction: str) -> str:
    return _COLORS.get(direction, "#6b7280")


def _arrow(direction: str) -> str:
    return _ARROWS.get(direction, "&#9644;")


def _section_heading(title: str) -> str:
    return f"""
    <tr>
      <td style="padding:20px 32px 8px;">
        <h2 style="margin:0;font-size:11px;text-transform:uppercase;letter-spacing:1.2px;color:#999;">
          {title}
        </h2>
      </td>
    </tr>"""


def _render_assets(assets: list) -> str:
    if not assets:
        return ""

    rows = ""
    for a in assets:
        d = a.get("direction", "flat")
        c = _color(d)
        arr = _arrow(d)
        pct = a.get("change_pct", 0)
        sign = "+" if pct > 0 else ""
        rows += f"""
    <tr>
      <td style="padding:14px 32px;border-bottom:1px solid #f0f0f0;">
        <table cellpadding="0" cellspacing="0" width="100%"><tr>
          <td style="font-size:14px;font-weight:600;color:#1a1a2e;">
            <span style="color:{c};">{arr}</span> {a.get('ticker','')}
            <span style="font-weight:400;color:#666;">&mdash; {a.get('name','')}</span>
          </td>
          <td align="right" style="font-size:13px;font-weight:600;color:{c};">
            {sign}{pct:.1f}%
          </td>
        </tr></table>
        <p style="margin:6px 0 0;color:#555;font-size:13px;line-height:1.5;">
          {a.get('summary','')}
        </p>
      </td>
    </tr>"""

    return _section_heading("Portfolio Updates") + rows


def _render_industries(industries: list) -> str:
    if not industries:
        return ""

    rows = ""
    for ind in industries:
        d = ind.get("direction", "neutral")
        c = _color(d)
        arr = _arrow(d)
        rows += f"""
    <tr>
      <td style="padding:12px 32px;border-bottom:1px solid #f0f0f0;">
        <span style="font-size:14px;font-weight:600;color:#1a1a2e;">
          <span style="color:{c};">{arr}</span> {ind.get('name','')}
        </span>
        <p style="margin:4px 0 0;color:#555;font-size:13px;line-height:1.5;">
          {ind.get('summary','')}
        </p>
      </td>
    </tr>"""

    return _section_heading("Industry Outlook") + rows


def _render_macro(macro: list) -> str:
    if not macro:
        return ""

    rows = ""
    for m in macro:
        rows += f"""
    <tr>
      <td style="padding:12px 32px;border-bottom:1px solid #f0f0f0;">
        <span style="font-size:14px;font-weight:600;color:#1a1a2e;">
          {m.get('theme','')}
        </span>
        <p style="margin:4px 0 0;color:#555;font-size:13px;line-height:1.5;">
          {m.get('summary','')}
        </p>
      </td>
    </tr>"""

    return _section_heading("Macro Themes") + rows
