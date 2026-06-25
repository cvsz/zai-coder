from zai_coder.creative_automation.project_types import CreativeProject
from zai_coder.creative_automation.asset_library import build_asset_library, is_safe_asset_path
from zai_coder.creative_automation.approval import transition_status, can_transition
from zai_coder.creative_automation.export_adapters import phaser_export_plan, godot_export_plan, document_export_plan, movie_export_plan
from zai_coder.creative_automation.dashboard import render_creative_dashboard
from zai_coder.creative_automation.web_api import route_status, route_assets, route_export_plan

from zai_coder.game_core_system.models import GameProject
from zai_coder.game_core_system.exporters import export_game_project
from zai_coder.document_core_system.templates import technical_spec_template
from zai_coder.document_core_system.exporters import export_document_project
from zai_coder.movie_system.models import MovieProject
from zai_coder.movie_system.exporters import export_movie_project


def test_creative_project_validation():
    project = CreativeProject(slug="demo", title="Demo", project_type="game")
    assert project.validate() == []


def test_asset_library_safety():
    assert is_safe_asset_path("assets/demo.svg")
    assert not is_safe_asset_path("../secret.svg")
    assert not is_safe_asset_path("apps/zlms/demo.svg")
    assets = build_asset_library(["assets/demo.svg", "../secret.svg"], project_slug="demo")
    assert len(assets) == 1


def test_approval_workflow():
    assert can_transition("draft", "review")
    event = transition_status("draft", "review", "tester", "ready")
    assert event.to_status == "review"


def test_export_plans_are_dry_run():
    assert phaser_export_plan("demo", "Demo").dry_run is True
    assert godot_export_plan("demo", "Demo").dry_run is True
    assert document_export_plan("Doc", "# Doc").dry_run is True
    assert movie_export_plan("Movie", "# Movie").dry_run is True


def test_dashboard_render():
    html = render_creative_dashboard([CreativeProject("demo", "Demo", "game")], build_asset_library(["assets/demo.svg"], "demo"))
    assert "ZAI Creative Automation" in html
    assert "demo" in html


def test_api_routes():
    assert route_status()["ok"] is True
    assert len(route_assets({"paths": ["assets/a.svg", "../x"], "project_slug": "p"})["assets"]) == 1
    assert route_export_plan({"kind": "phaser", "slug": "g", "title": "Game"})["adapter"] == "phaser"


def test_game_document_movie_exporters():
    game_plan = export_game_project(GameProject(slug="g", title="Game", genre="arcade", platform="web"), "phaser")
    assert game_plan.adapter == "phaser"

    doc_plan = export_document_project(technical_spec_template("Spec"))
    assert doc_plan.adapter == "document"

    movie_plan = export_movie_project(MovieProject(title="Film", logline="Original story.", genre="sci-fi"))
    assert movie_plan.adapter == "movie"
