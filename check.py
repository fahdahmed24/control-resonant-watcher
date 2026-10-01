"""Email when a watched rental game changes status."""
import json
import os
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "https://samuraistore.site/rental-games"
TITLE = os.environ.get("GAME_TITLE", "CONTROL Resonant")
STATE = Path(os.environ.get("GAME_STATE", "state.json"))


def get_status():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(locale="en-US")
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            card = page.locator("article.rental-game-card").filter(
                has=page.get_by_role("heading", name=TITLE, exact=True)
            )
            card.wait_for(state="visible", timeout=75000)
            if card.count() != 1:
                raise RuntimeError(f"Expected exactly one {TITLE} card")
            badge = card.locator(".rental-stock-badge")
            if badge.count() != 1:
                raise RuntimeError("Expected exactly one rental status badge")
            label = " ".join(badge.inner_text().casefold().split())
            statuses = {
                "available now": "available",
                "currently rented": "rented",
                "unavailable": "unavailable",
            }
            if label not in statuses:
                raise RuntimeError(f"Unknown rental status: {label!r}")
            buttons = {
                " ".join(text.casefold().split())
                for text in card.locator("button").all_text_contents()
            }
            expected_button = "add to cart" if label == "available now" else label
            if expected_button not in buttons:
                raise RuntimeError("Status badge and rental button disagree")
            return statuses[label]
        finally:
            browser.close()


def email_change(old, new):
    sender = os.environ["GMAIL_USERNAME"]
    recipient = os.environ["ALERT_TO"]
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = f"{TITLE}: {new.upper()}"
    message.set_content(
        f"{TITLE} changed from {old} to {new}." + chr(10) * 2
        + "Rental page: " + URL + chr(10)
    )
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(sender, os.environ["GMAIL_APP_PASSWORD"])
        smtp.send_message(message)


def main():
    previous_data = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    previous = previous_data.get("status")
    current = get_status()
    print(f"{TITLE}: {previous or 'unknown'} -> {current}")
    if previous is not None and current != previous and current in {"available", "rented"}:
        email_change(previous, current)
        print("Change email sent")
    checked = datetime.now(timezone.utc)
    saved_at = previous_data.get("checked_at")
    old_check = datetime.fromisoformat(saved_at) if saved_at else None
    if current != previous or old_check is None or (checked - old_check).days >= 7:
        STATE.write_text(
            json.dumps({"status": current, "checked_at": checked.isoformat(timespec="seconds")}, indent=2)
            + chr(10), encoding="utf-8"
        )
        print("State saved")


if __name__ == "__main__":
    main()
