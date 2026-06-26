# TUI Design Tokens

Terminal UIs cannot implement browser backdrop blur. ZAI Coder uses a terminal-native glassmorphism-inspired style instead:

- Layered panels
- Soft rounded borders
- Dim and bright contrast
- Intentional spacing
- Status chips
- Command palette
- Non-blocking async refresh
- Accessible layout with deterministic panel names and readable contrast

## Theme

`zeaz-glass-dark`

```text
background: #061017
panel: #0d1b24
panel_alt: #122836
border_soft: #2b5465
border_bright: #77d7c8
text: #d8fff7
muted: #7aa0a8
accent: #42e8c7
warning: #ffd166
danger: #ff5c7a
success: #6be675
```

## Token Surfaces

- Theme name: `zeaz-glass-dark`
- Panel styles: base panel, alternate panel, bright border, soft border
- Status levels: safe, dry-run, ready, warning, blocked, active
- Text fallback: every template can render a static terminal preview without Textual
