from zai_coder.game_core_system.models import GameProject, GameScene, GameAsset
from zai_coder.game_core_system.design_doc import validate_game_project, render_game_design_doc
from zai_coder.game_core_system.mechanics import Mechanic, validate_mechanics
from zai_coder.game_core_system.assets import is_safe_game_asset_path

from zai_coder.document_core_system.templates import technical_spec_template, runbook_template
from zai_coder.document_core_system.renderer import validate_document, render_markdown, render_html
from zai_coder.document_core_system.library import is_safe_document_path

from zai_coder.movie_system.models import MovieProject, Character, MovieScene
from zai_coder.movie_system.screenplay import validate_movie_project, render_treatment
from zai_coder.movie_system.storyboard import Shot, validate_shots, render_shotlist
from zai_coder.movie_system.production import ProductionTask, validate_production_tasks


def test_game_project_design_doc():
    project = GameProject(
        slug="neon-agent",
        title="Neon Agent",
        genre="platformer",
        platform="web",
        scenes=[GameScene(slug="intro", title="Intro", objective="teach movement", entities=["player"])],
        assets=[GameAsset(path="assets/player.png", kind="sprite")],
    )
    assert validate_game_project(project) == []
    doc = render_game_design_doc(project)
    assert "# Neon Agent" in doc
    assert "teach movement" in doc


def test_game_mechanics_validation_and_asset_safety():
    assert validate_mechanics([Mechanic("Jump", "space", "player moves up", "sound")]) == []
    assert is_safe_game_asset_path("assets/player.png")
    assert not is_safe_game_asset_path("../secret.png")
    assert not is_safe_game_asset_path("apps/zlms/player.png")


def test_document_templates_and_renderers():
    doc = technical_spec_template("ZAI API")
    assert validate_document(doc) == []
    md = render_markdown(doc)
    html = render_html(doc)
    assert "# ZAI API" in md
    assert "<!doctype html>" in html


def test_document_path_safety():
    assert is_safe_document_path("docs/spec.md")
    assert not is_safe_document_path("/etc/passwd")
    assert not is_safe_document_path("apps/zlms/spec.md")


def test_movie_project_treatment():
    movie = MovieProject(
        title="Agent City",
        logline="A local AI agent helps rebuild a broken software city.",
        genre="sci-fi",
        characters=[Character("Zai", "assistant", "protect the project")],
        scenes=[MovieScene("opening", "terminal room", "The first agent wakes up.", ["Zai"])],
    )
    assert validate_movie_project(movie) == []
    treatment = render_treatment(movie)
    assert "# Agent City" in treatment
    assert "The first agent wakes up." in treatment


def test_storyboard_and_production_validation():
    shots = [Shot(scene_slug="opening", shot_type="wide", description="Terminal lights glow", duration_seconds=4)]
    assert validate_shots(shots) == []
    assert "Terminal lights glow" in render_shotlist(shots)
    assert validate_production_tasks([ProductionTask("Render teaser", "media-agent")]) == []
