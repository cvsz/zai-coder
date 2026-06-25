"""Hugging Face integration adapter."""

from __future__ import annotations

from zai_coder.integration_core.models import IntegrationPlan


def model_card(model_name: str, description: str = "Local-first ZAI Coder artifact.") -> str:
    return f"""---
license: mit
tags:
- zai-coder
- local-first
- automation
---

# {model_name}

{description}

## Safety

This artifact was prepared by a dry-run-first workflow. Review all files before publishing.
"""


def dataset_upload_plan(repo_id: str, data_dir: str = "data") -> IntegrationPlan:
    return IntegrationPlan(
        provider="huggingface",
        action="dataset_upload_plan",
        commands=[f"hf repo create {repo_id} --type dataset", f"hf upload {repo_id} {data_dir} . --repo-type dataset"],
        payload={"repo_id": repo_id, "data_dir": data_dir},
        warnings=["No upload is executed by this adapter. Requires explicit operator action."],
    )


def model_publish_plan(repo_id: str, model_dir: str = "model") -> IntegrationPlan:
    return IntegrationPlan(
        provider="huggingface",
        action="model_publish_plan",
        commands=[f"hf repo create {repo_id} --type model", f"hf upload {repo_id} {model_dir} . --repo-type model"],
        files={"README.md": model_card(repo_id)},
        payload={"repo_id": repo_id, "model_dir": model_dir},
    )


def space_scaffold_plan(repo_id: str, sdk: str = "gradio") -> IntegrationPlan:
    app_py = (
        "import gradio as gr\n\n"
        "def hello(name):\n"
        "    return f\"Hello {name} from ZAI Coder\"\n\n"
        "demo = gr.Interface(fn=hello, inputs=\"text\", outputs=\"text\")\n"
        "demo.launch()\n"
    )
    return IntegrationPlan(
        provider="huggingface",
        action="space_scaffold_plan",
        commands=[f"hf repo create {repo_id} --type space --space_sdk {sdk}", f"hf upload {repo_id} app.py app.py --repo-type space"],
        files={"app.py": app_py, "README.md": model_card(repo_id, "ZAI Coder demo Space.")},
        payload={"repo_id": repo_id, "sdk": sdk},
    )
