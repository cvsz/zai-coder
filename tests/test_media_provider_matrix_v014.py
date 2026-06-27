from zai_coder.media.providers import get_default_media_matrix

def test_media_provider_matrix_defaults():
    matrix = get_default_media_matrix()
    
    # Check local svg
    local_svg = matrix.providers["local-svg"]
    assert local_svg.capability == "image"
    assert local_svg.status == "available"
    assert local_svg.local_only is True
    assert local_svg.enabled_by_default is True
    
    # Check requiring integration
    fal = matrix.providers["fal-ai"]
    assert fal.status == "requires_integration"
    assert fal.requires_api_key is True
    assert fal.enabled_by_default is False

    # Check getters
    vision_providers = matrix.get_providers_by_capability("vision")
    assert len(vision_providers) >= 3 # local-story, gemini, xai
    
    available_image = matrix.get_available_providers("image")
    assert len(available_image) == 1
    assert available_image[0].provider_id == "local-svg"
