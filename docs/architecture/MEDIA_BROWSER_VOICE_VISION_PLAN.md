# Media, Browser, Voice, and Vision Plan

This document outlines the strategic plan for expanding ZAI Coder's capabilities into multimodal interaction, media generation, and browser automation while strictly maintaining safety and determinism.

## Capability Objectives

1. **Browser Automation**
   - Goal: Automate web interactions safely.
   - Status: `planned`.
   - Implementations planned: Local CDP, Browserbase, Browser Use.
   - Restraint: Do not enable by default. Do not allow unrestrained form filling.

2. **Voice & TTS**
   - Goal: Allow voice-driven command and output.
   - Status: `planned`.
   - Implementations planned: ElevenLabs, OpenAI TTS.

3. **Multimodal Vision**
   - Goal: Parse images, screenshots, and visual pastes.
   - Status: `planned`.
   - Implementations planned: GPT-4o Vision, Claude 3.5 Sonnet Vision.

4. **Media Generation (Images, Video, Music)**
   - Goal: Asset generation capabilities.
   - Status: Local primitives `available`, External integrations `requires_integration`.
   - Implementations planned: FAL.ai, OpenAI DALL-E, local SVG/WAV engines.

## Integration Posture

- **Do Not Claim**: Live browser automation, native voice chat, provider image generation, provider TTS unless explicitly implemented and tested.
- **Opt-In Only**: All multimodal integrations are strictly opt-in and disabled by default.
