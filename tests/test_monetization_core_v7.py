import sqlite3
import tempfile
from pathlib import Path

import pytest

from zai_coder.monetization_core.plans import get_plan, list_plans
from zai_coder.monetization_core.subscriptions import Subscription
from zai_coder.monetization_core.ledger import CreditLedger
from zai_coder.monetization_core.quota import QuotaService
from zai_coder.monetization_core.usage import UsageStore
from zai_coder.monetization_core.rate_limit import TokenBucket
from zai_coder.monetization_core.reconciliation import reconcile_account
from zai_coder.monetization_core.billing_events import BillingEventStore
from zai_coder.monetization_core.idempotency import IdempotencyStore
from zai_coder.monetization_core.adapters.stripe_sandbox import create_checkout_plan
from zai_coder.admin_dashboard.monetization import render_monetization_dashboard


def test_plan_catalog():
    assert get_plan("free").monthly_price_cents == 0
    assert len(list_plans()) >= 4


def test_subscription_validation():
    sub = Subscription(id="sub_1", account_id="acct_1", plan_slug="builder")
    assert sub.validate() == []
    bad = Subscription(id="", account_id="", plan_slug="", status="bad")
    assert bad.validate()


def test_credit_ledger_append_only_balance_and_idempotency():
    with tempfile.TemporaryDirectory() as td:
        ledger = CreditLedger(Path(td) / "monetization.db")
        ledger.append("acct", "ws", "grant", 100, "initial", "k1")
        ledger.append("acct", "ws", "debit", -25, "run", "k2")
        assert ledger.balance("acct") == 75
        with pytest.raises(sqlite3.IntegrityError):
            ledger.append("acct", "ws", "grant", 10, "duplicate", "k1")


def test_quota_reserve_commit_release():
    with tempfile.TemporaryDirectory() as td:
        quota = QuotaService(Path(td) / "quota.db")
        r1 = quota.reserve("acct", "ws", "agent_run", 1, "q1")
        quota.commit(r1.id)

        r2 = quota.reserve("acct", "ws", "agent_run", 1, "q2")
        quota.release(r2.id)

        with pytest.raises(ValueError):
            quota.commit(r2.id)


def test_usage_and_reconciliation():
    with tempfile.TemporaryDirectory() as td:
        db = Path(td) / "m.db"
        ledger = CreditLedger(db)
        usage = UsageStore(db)
        ledger.append("acct", "ws", "grant", 100, "initial", "l1")
        usage.record("acct", "ws", "credit_unit", 10, "agent_run")
        result = reconcile_account(ledger, usage, "acct")
        assert result.ledger_balance == 100
        assert result.usage_units == 10
        assert result.issues == []


def test_rate_limit_token_bucket():
    bucket = TokenBucket(capacity=2, refill_per_second=0)
    assert bucket.allow()
    assert bucket.allow()
    assert not bucket.allow()


def test_billing_event_replay_protection():
    with tempfile.TemporaryDirectory() as td:
        store = BillingEventStore(Path(td) / "billing.db")
        store.record("sandbox", "evt_1", "checkout.completed", {"ok": True})
        with pytest.raises(sqlite3.IntegrityError):
            store.record("sandbox", "evt_1", "checkout.completed", {"ok": True})


def test_idempotency_store():
    with tempfile.TemporaryDirectory() as td:
        store = IdempotencyStore(Path(td) / "idem.db")
        assert not store.exists("abc")
        store.record("abc", "quota.reserve", '{"x":1}', '{"ok":true}')
        assert store.exists("abc")


def test_stripe_sandbox_does_not_call_live_api():
    plan = create_checkout_plan("acct", "builder")
    assert plan.dry_run is True
    assert plan.provider == "stripe_sandbox"


def test_monetization_dashboard_render():
    html = render_monetization_dashboard(list_plans(), {"agent_runs": 5})
    assert "ZAI Monetization Admin" in html
    assert "agent_runs" in html
