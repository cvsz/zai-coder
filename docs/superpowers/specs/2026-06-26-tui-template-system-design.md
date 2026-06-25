# Design Specification: ZAI Coder TUI Template System

**Date:** 2026-06-26
**Status:** Draft for Review

## Overview
This design establishes a modular, extensible Text User Interface (TUI) system for the ZAI Coder Control Plane. The system leverages a factory pattern to switch between distinct visual templates while maintaining a shared, non-blocking Python runtime.

## Architecture
- **Core Controller (`zai_coder.core`):** Manages Agent logic, Sessions, Skills, and Memory. Runs asynchronously to ensure UI responsiveness.
- **Template Loader (`tui.loader`):** A factory that selects the active TUI template defined in `config/zai-coder.config.json`.
- **View Layer (`textual`):** A high-performance, async-native TUI framework.
- **Communication:** Async message bus between Core Controller and View Layer to handle status updates (e.g., loading states, progress bars) without blocking the terminal.

## Visual Templates

### Template 01: Command Center (The "Focus" Template)
- **Goal:** Minimalist, high-focus interface for deep work.
- **Design:** Centralized, clean chat-centric view.
- **Navigation:** Uses a context-aware "Floating Command Palette" (invoked via `Ctrl+K`) for session switching, command execution, and task management.
- **Aesthetic:** Minimalist, glassmorphism, heavy use of backdrop blur.

### Template 02: Agent-Hub (The "Operator" Template)
- **Goal:** Comprehensive monitoring for complex system orchestration.
- **Design:** Tile-based (Grid) layout showing the status of multiple active agents.
- **Interactivity:** Contextual drill-down; focus on a specific grid tile expands it into the primary working area for that agent.
- **Aesthetic:** Symmetrical, dense data presentation (metrics, logs, progress), clear color-coded indicators.

## Safety & UX Standards
- **Typography:** Outfit (primary), Inter (fallback).
- **Transitions:** Micro-animations (min 200ms) for all interactive element state changes.
- **Dry-Run-First:** All command-triggered mutations through the TUI must require a dry-run confirmation phase before `APPLY=1` is authorized.
- **Responsiveness:** Asynchronous UI updates to prevent terminal lockup during heavy Agent compute cycles.

## Compliance
- Adheres to existing `zai-coder` GitOps safety, secret redaction, and non-mutation mandates.
