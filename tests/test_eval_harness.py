from __future__ import annotations

import json

from evals.run_local import main


def test_local_eval_harness_writes_results(tmp_path):
    evals_dir = tmp_path / "evals"
    evals_dir.mkdir()
    (evals_dir / "cases.jsonl").write_text(
        '{"id":"planner-1","suite":"planner-contract","kind":"agent","agent":"planner","prompt":"Plan safely","expect_contains":["Create a staged execution plan."]}\n',
        encoding="utf-8",
    )

    output = tmp_path / "evals" / "results" / "latest.json"
    exit_code = main(["--suite", "planner-contract", "--workspace", str(tmp_path), "--output", str(output)])
    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["suite"] == "planner-contract"
    assert payload["report"]["pass_count"] == 1
