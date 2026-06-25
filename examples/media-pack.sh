#!/usr/bin/env bash
set -euo pipefail
./zai-coder media image --prompt "ZAI multi-agent neon dashboard" --out out/demo-image.svg
./zai-coder media voice --text "ZAI Coder is online" --out out/demo-voice.wav
./zai-coder media music --prompt "calm cyber coding loop" --out out/demo-music.wav
./zai-coder media animation --prompt "planner coder reviewer ship" --out out/demo-animation.svg
./zai-coder media video --prompt "ZAI Coder launch" --out out/demo-video-storyboard.json
find out -maxdepth 1 -type f -print
