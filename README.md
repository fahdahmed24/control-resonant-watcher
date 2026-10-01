# Rental game watcher

This repository checks [Samurai Store's rental games](https://samuraistore.site/rental-games) for **CONTROL Resonant** and **SILENT HILL Townfall** about every five minutes. It emails the configured recipient when either game changes to **AVAILABLE NOW** or **CURRENTLY RENTED**. An unchanged status does not send another email. **UNAVAILABLE** is recorded without an alert.

Each game has its own saved status: `state.json` for CONTROL Resonant and `townfall_state.json` for SILENT HILL Townfall. The checker uses the exact game title and status badge on each rental card. Townfall was AVAILABLE NOW when added on October 2, 2026 (Egypt time).

## Email and runs

The GitHub Actions workflow uses the repository secrets `GMAIL_USERNAME`, `GMAIL_APP_PASSWORD`, and `ALERT_TO`. The Gmail password is an app password stored only in GitHub Secrets. The separate **Test rental alert email** workflow sends a clearly labeled test message when run manually.

Open **Actions → Watch CONTROL Resonant and SILENT HILL Townfall** to view checks or run one manually. A check with no status change sends no email.

## Timing

Five minutes is GitHub Actions' shortest schedule interval. GitHub may delay or skip a scheduled run, and a brief change between checks can be missed. If a run fails, check its Actions log. The workflow updates saved timestamps weekly so the public repository remains active.
