"""Bridge templates to help center article flows."""

from __future__ import annotations


def help_article_template_map() -> dict:
    return {
        "help_article_template": "tpl-help-article",
        "release_note_template": "tpl-release-note",
        "roadmap_update_template": "tpl-roadmap-update",
        "customer_welcome_template": "tpl-welcome-email",
    }


def suggested_template_for_intent(intent: str) -> dict:
    intent = intent.lower()
    if "release" in intent:
        template_id = "tpl-release-note"
    elif "help" in intent or "article" in intent:
        template_id = "tpl-help-article"
    elif "roadmap" in intent:
        template_id = "tpl-roadmap-update"
    elif "welcome" in intent or "onboarding" in intent:
        template_id = "tpl-welcome-email"
    else:
        template_id = "tpl-help-article"
    return {"intent": intent, "template_id": template_id}
