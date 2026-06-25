"""Local help center search."""

from __future__ import annotations

from .articles import article_by_visibility
from .faq import faq_catalog
from .models import SearchResult


def tokenize(text: str) -> set[str]:
    return {token.strip(".,!?()[]{}:;\"'").lower() for token in text.split() if token.strip()}


def score_text(query: str, text: str, tags: list[str] | tuple[str, ...] = ()) -> float:
    q = tokenize(query)
    hay = tokenize(text)
    tag_tokens = {str(tag).lower() for tag in tags}
    if not q:
        return 0.0
    score = len(q & hay) + 2 * len(q & tag_tokens)
    return float(score)


def help_search(query: str, visibility: str = "customer", limit: int = 10) -> dict:
    results = []
    for article in article_by_visibility(visibility):
        score = score_text(query, f"{article['title']} {article['body']} {' '.join(article['tags'])}", article["tags"])
        if score > 0:
            results.append(SearchResult(article["id"], article["title"], score, "article", article["body"][:180], article["visibility"]).to_dict())
    for faq in faq_catalog():
        if visibility != "private" and faq["visibility"] not in {"customer", "public"}:
            continue
        score = score_text(query, f"{faq['question']} {faq['answer']} {faq['category']}")
        if score > 0:
            results.append(SearchResult(faq["id"], faq["question"], score, "faq", faq["answer"][:180], faq["visibility"]).to_dict())
    return {"query": query, "results": sorted(results, key=lambda row: row["score"], reverse=True)[:limit]}


def search_validation_report() -> dict:
    demo = help_search("billing no charge")
    reports = [{"id": row["id"], "issues": SearchResult(**row).validate()} for row in demo["results"]]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}
