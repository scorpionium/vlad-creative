# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a Claude Code plugin that automates the production of 9:16 vertical vinyl unboxing reels (YouTube Shorts / Instagram Reels) from raw phone footage and audio samples. The workflow is bilingual (English + Ukrainian) and outputs three MP4 files plus YouTube metadata.

## Plugin Architecture

This is a **declarative workflow plugin**, not a traditional application. There is no build step, no package manager, and no test runner. The plugin runs entirely within Claude Code using:

- `skills/vinyl-reel/SKILL.md` — the authoritative 6-phase workflow specification
- `commands/vinyl-reel.md` — defines the `/vinyl-reel` slash command
- `skills/vinyl-reel/scripts/` — Python and bash utilities invoked during the workflow
- `skills/vinyl-reel/references/` — ffmpeg patterns and voiceover style guides Claude reads during execution
- `skills/vinyl-reel/assets/` — bundled green-screen subscribe overlay video

## Running the Skill

Trigger the skill by either:
- `/vinyl-reel /path/to/Album-Folder`
- Describing a vinyl reel task in natural language (skill auto-triggers)

Expected input folder layout:
```
Album Name/
├── video/    # raw clips (.mp4 .mov .avi .mkv .m4v)
└── audio/    # background music samples (.m4a .mp3 .wav .aac .flac .ogg)
```

## System Dependencies

The scripts require: **Python 3**, **ffmpeg**, and **ffprobe**. The ffmpeg build must include the filters: `silencedetect`, `acrossfade`, `adelay`, `volume`, `afade`, `alimiter`, `chromakey`, `drawtext`. Text overlays use `LiberationSans` or `DejaVuSans`.

## 6-Phase Workflow Summary

| Phase | Tool | Pause? |
|-------|------|--------|
| 1. Scan & catalog clips | `analyze_clips.py` (ffprobe) | No |
| 2. Research album | Web search | No |
| 3. Write EN + UA voiceover scripts | Claude | **Yes — user approves scripts** |
| 4. Record voiceover | User records & drops MP3s in folder | **Yes — wait for user confirmation** |
| 5. Arrange, mix, assemble video | ffmpeg + `mix_audio.sh` | No |
| 6. Export 3 outputs + metadata | ffmpeg + chromakey | No |

## Key Scripts

**`scripts/analyze_clips.py`** — Phases 1 inventory: probes each video with ffprobe, extracts a thumbnail at t=1s, outputs a JSON catalog with duration, dimensions, orientation.

**`scripts/mix_audio.sh`** — Phase 5 audio mixing:
1. Concatenates all audio samples with 1-second crossfades
2. Detects silence/speech boundaries in the voiceover via `silencedetect`
3. Builds a piecewise-linear volume envelope: background ducks to **10%** during speech, rises to **100%** during pauses; 0.5s smooth transitions
4. Voiceover starts at the **3-second mark** (music-only intro)
5. Outputs a 44.1 kHz stereo WAV

## Reference Guides (read during execution)

- `references/ffmpeg_patterns.md` — canonical ffmpeg commands for scaling to 1080×1920, two-line text overlays with shadows, segment concat, chromakey overlay, CRF-18 H.264 encoding
- `references/voiceover_style.md` — script structure (hook → significance → band → edition → vinyl reveal → closer), ~30s speech + 2–3 × 5s pauses, bilingual tone guidance

## Outputs

| File | Description |
|------|-------------|
| `*_yt_shorts_en.mp4` | YouTube Shorts (EN) with green-screen subscribe overlay at t=30s |
| `*_instagram_en.mp4` | Instagram Reels (EN), clean version |
| `*_yt_shorts_ua.mp4` | YouTube Shorts (UA) |
| `*_metadata.md` | EN + UA titles, descriptions, hashtags ready to paste |
