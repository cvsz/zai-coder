# Media Provider Matrix

This matrix tracks the planned status of media and multimodal providers in ZAI Coder.

| ID | Label | Capability | Status | Local Only | Needs API Key | Enabled by Default |
|---|---|---|---|---|---|---|
| `local-svg` | Local SVG | Image Generation | `available` | Yes | No | Yes |
| `local-wav` | Local WAV | Voice/Audio Generation | `available` | Yes | No | Yes |
| `local-story` | Local Storyboard | Vision/Video primitive | `available` | Yes | No | Yes |
| `fal-ai` | FAL.ai | Image/Video | `requires_integration` | No | Yes | No |
| `elevenlabs` | ElevenLabs | Voice/TTS | `requires_integration` | No | Yes | No |
| `openai-tts` | OpenAI TTS | Voice/TTS | `requires_integration` | No | Yes | No |
| `gemini-multimodal` | Gemini | Vision/Browser | `requires_integration` | No | Yes | No |
| `xai-multimodal` | xAI | Vision/Browser | `requires_integration` | No | Yes | No |
| `browserbase` | Browserbase | Browser | `requires_integration` | No | Yes | No |
| `browser-use` | Browser Use | Browser | `requires_integration` | No | Yes | No |
| `local-cdp` | Local CDP | Browser | `requires_integration` | Yes | No | No |

*Note: Integrations marked `requires_integration` are explicitly DO NOT CLAIM until fully implemented and verified.*
