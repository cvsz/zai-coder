#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.integration_core.adapters.notifications import email_draft, slack_payload_draft, discord_payload_draft, telegram_payload_draft
print(email_draft("admin@example.com", "ZAI Done", "Integration plan ready").to_dict())
print(slack_payload_draft("#ops", "ZAI done").to_dict())
print(discord_payload_draft("ZAI done").to_dict())
print(telegram_payload_draft("123", "ZAI done").to_dict())
PY
