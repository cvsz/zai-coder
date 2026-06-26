# Prompt: Media, Browser, Voice, and Vision Plan

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4+ Planning/Implementation PR — Media, Browser, Voice, and Vision Plan

Branch:
docs/v0.1.4-media-browser-voice-vision-plan

Goal:
Create a safe, claim-controlled plan for media generation, browser automation, voice mode, TTS, transcription, and multimodal vision. Only implement local metadata/interfaces in this phase unless explicitly scoped and tested.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not add paid provider dependencies as mandatory dependencies.
- Do not add real API keys.
- Do not claim provider support unless adapter exists and is documented as configured-by-user.
- Do not enable browser automation by default.
- Do not browse, fill forms, or automate websites in tests.
- Do not commit generated media outputs.
- Stage exact files only.

Step 1: Sync baseline

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short

git switch -c docs/v0.1.4-media-browser-voice-vision-plan

Step 2: Inspect current media modules

find zai_coder/media tests docs -maxdepth 4 -type f | sort
grep -R "generate_svg_image\|generate_voice_wav\|generate_music_wav\|generate_animation_svg\|generate_video_storyboard\|browser\|vision\|tts\|voice" -n zai_coder tests docs 2>/dev/null | head -600

Step 3: Create plan docs

Create:
- docs/architecture/MEDIA_BROWSER_VOICE_VISION_PLAN.md
- docs/product/MEDIA_PROVIDER_MATRIX.md

Status classifications:
- available: local SVG/image, local WAV primitives, storyboard primitives if already implemented.
- planned: browser automation, voice mode, image paste, multimodal vision.
- requires_integration: FAL.ai, ElevenLabs, OpenAI TTS, Gemini, xAI, Browserbase, Browser Use, local CDP.
- do_not_claim: live browser automation, native voice chat, provider image generation, provider TTS unless implemented.

Step 4: Optional interface-only implementation

Only if small and safe, create:
- zai_coder/media/providers.py
- tests/test_media_provider_matrix_v014.py

Provider matrix fields:
- id
- label
- capability: image, voice, tts, transcription, browser, vision
- status
- requires_api_key
- env_var
- local_only
- enabled_by_default false

Step 5: Validation

python3 -m pytest tests/test_media_provider_matrix_v014.py -q || true
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

Step 6: Stage exact files only

git add docs/architecture/MEDIA_BROWSER_VOICE_VISION_PLAN.md
git add docs/product/MEDIA_PROVIDER_MATRIX.md
# If implemented:
git add zai_coder/media/providers.py
git add tests/test_media_provider_matrix_v014.py

Step 7: Commit and PR

git commit -S -m "docs: plan media browser voice and vision capabilities"
git push -u origin docs/v0.1.4-media-browser-voice-vision-plan

gh pr create \
  --base main \
  --head docs/v0.1.4-media-browser-voice-vision-plan \
  --draft \
  --title "docs: plan media browser voice and vision capabilities" \
  --body "Adds a claim-controlled plan for media, browser, voice, TTS, transcription, and vision capabilities."

Report:
1. branch
2. current media capabilities found
3. planned provider capabilities
4. requires-integration list
5. do-not-claim list
6. validation result
7. commit hash
8. draft PR URL
```
