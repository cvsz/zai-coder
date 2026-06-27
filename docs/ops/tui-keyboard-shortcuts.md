# TUI Keyboard Shortcuts

The TUI command center is keyboard-first. Phase 2 adds an interactive palette
and immediate template-switch persistence.

## Global Shortcuts

```text
ctrl+k  open and focus the command palette
ctrl+r  refresh status and panels
ctrl+d  toggle dry-run display mode
f1      show help
q       quit
```

## Palette Shortcuts

When the palette is open:

```text
up/down     move through visible actions
enter       run the selected action through the safe command router
escape      close the palette and return focus to the command input
backspace   remove the last search character
typing      filter actions by command, label, or kind
```

Palette execution uses the same router as typed commands. Shell-backed actions
remain dry-run-safe and allowlisted.

## Template Switching

Template switch commands update the active template immediately:

```text
switch command-center
switch agent-hub
switch flow-stream
switch architect-tree
switch creative-canvas
switch operation-gate
```

When TUI state persistence is enabled, template switches are saved to
`.zai-coder/tui-state.json` by default and restored on the next launch unless an
explicit template is passed on the command line.

## Safety Model

The palette does not bypass safety policy. Blocked commands such as broad git
staging, force pushes, `rm -rf`, `APPLY=1`, and pipe-to-bash installers remain
blocked by the TUI router.
