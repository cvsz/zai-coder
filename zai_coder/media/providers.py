from __future__ import annotations

from dataclasses import dataclass

@dataclass
class MediaProvider:
    provider_id: str
    label: str
    capability: str # image, voice, tts, transcription, browser, vision
    status: str # available, planned, requires_integration, do_not_claim
    local_only: bool = False
    requires_api_key: bool = False
    env_var: str | None = None
    enabled_by_default: bool = False

class MediaProviderMatrix:
    def __init__(self):
        self.providers: dict[str, MediaProvider] = {}
        
    def register(self, provider: MediaProvider):
        self.providers[provider.provider_id] = provider
        
    def get_providers_by_capability(self, capability: str) -> list[MediaProvider]:
        return [p for p in self.providers.values() if p.capability == capability]
        
    def get_available_providers(self, capability: str) -> list[MediaProvider]:
        return [p for p in self.get_providers_by_capability(capability) if p.status == "available"]

# Default Matrix Initialization
def get_default_media_matrix() -> MediaProviderMatrix:
    matrix = MediaProviderMatrix()
    
    # Local
    matrix.register(MediaProvider("local-svg", "Local SVG", "image", "available", local_only=True, enabled_by_default=True))
    matrix.register(MediaProvider("local-wav", "Local WAV", "voice", "available", local_only=True, enabled_by_default=True))
    matrix.register(MediaProvider("local-story", "Local Storyboard", "vision", "available", local_only=True, enabled_by_default=True))
    
    # Integrations
    matrix.register(MediaProvider("fal-ai", "FAL.ai", "image", "requires_integration", requires_api_key=True))
    matrix.register(MediaProvider("elevenlabs", "ElevenLabs", "tts", "requires_integration", requires_api_key=True))
    matrix.register(MediaProvider("openai-tts", "OpenAI TTS", "tts", "requires_integration", requires_api_key=True))
    matrix.register(MediaProvider("gemini-multimodal", "Gemini", "vision", "requires_integration", requires_api_key=True))
    matrix.register(MediaProvider("xai-multimodal", "xAI", "vision", "requires_integration", requires_api_key=True))
    matrix.register(MediaProvider("browserbase", "Browserbase", "browser", "requires_integration", requires_api_key=True))
    matrix.register(MediaProvider("browser-use", "Browser Use", "browser", "requires_integration", requires_api_key=True))
    matrix.register(MediaProvider("local-cdp", "Local CDP", "browser", "requires_integration", local_only=True))
    
    return matrix
