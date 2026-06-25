# ZAI Coder Control Plane v4 — Creative Core Requirements

## Scope

Add three creative production systems:

1. Game Core System
2. Document Core System
3. Movie System

## Game Core System

### Requirements

- Game project model.
- Scene model.
- Asset registry.
- Mechanics registry.
- Game design document renderer.
- Safe asset path validation.
- Future export adapters:
  - Godot
  - Unity
  - Phaser
  - Three.js
  - Pygame

### Future CLI

```bash
./zai-coder game create --title "Neon Agent"
./zai-coder game design-doc --out docs/game/GDD.md
./zai-coder game mechanics validate
./zai-coder game assets scan
```

## Document Core System

### Requirements

- Document project model.
- Section model.
- Templates:
  - technical spec
  - runbook
  - product requirement document
  - release notes
  - pitch deck outline
- Markdown renderer.
- HTML renderer.
- Safe document library.
- Future DOCX/PDF export adapters.

### Future CLI

```bash
./zai-coder document new --template technical-spec --title "ZAI API"
./zai-coder document render --format md
./zai-coder document validate
./zai-coder document library scan
```

## Movie System

### Requirements

- Movie project model.
- Character model.
- Scene outline model.
- Treatment renderer.
- Storyboard shot model.
- Shot list renderer.
- Production task planner.
- Future video generation adapters:
  - storyboard JSON
  - subtitles
  - ffmpeg render
  - Remotion render
  - avatar pipeline

### Future CLI

```bash
./zai-coder movie new --title "Agent City"
./zai-coder movie treatment --out docs/movie/treatment.md
./zai-coder movie storyboard --out out/storyboard.json
./zai-coder movie shotlist --out docs/movie/shotlist.md
```

## Safety Requirements

- Default dry-run.
- Use original user-owned content.
- Do not include copyrighted scripts or franchise material.
- Block unsafe paths.
- Block apps/zlms/**.
- Block generated artifacts.
- Require explicit adapters for external engines/services.
