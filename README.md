# CONTROL Resonant rental watcher

This repository checks the CONTROL Resonant card on [Samurai Store](https://samuraistore.site/rental-games) every five minutes. It emails the configured recipient when the card changes to CURRENTLY RENTED or AVAILABLE NOW. Repeated checks of the same status do not send more email.

The starting status was AVAILABLE NOW when checked on October 2, 2026 (Egypt time). The latest known status is recorded in state.json. UNAVAILABLE is recorded but does not trigger an email.

## Finish email setup

In Settings > Secrets and variables > Actions, add a repository secret named GMAIL_APP_PASSWORD. Use a Gmail app password for the account named by GMAIL_USERNAME. Do not use the normal Google password, and do not put the app password in a file or chat. ALERT_TO and GMAIL_USERNAME are already stored as repository secrets.

Gmail app passwords require two-step verification. Create the app password in your Google Account and enter it directly into GitHub Secrets. Then use Actions > Watch CONTROL Resonant > Run workflow to test the checker. A normal check while the status remains available does not send email.

## Timing and limits

Five minutes is GitHub Actions' shortest schedule interval. GitHub can delay or drop scheduled runs, so an alert is best effort rather than instant. A brief status change between checks may be missed. If the store blocks automated browsers or changes its page structure, a run fails without changing the saved status. Check the Actions run history for failures.

The workflow makes a weekly state update so the public repository continues to have activity. GitHub may disable scheduled workflows in public repositories after 60 days without activity.
