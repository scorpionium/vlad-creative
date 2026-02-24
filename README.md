# vlad-creative-plugin

Vinyl unboxing reel creator. Turns a folder of raw phone clips and audio samples into a polished 9:16 short-form video with AI voiceover, background music, text overlays, and platform-specific exports for YouTube Shorts and Instagram Reels.

## Components

| Component | Name | Purpose |
|-----------|------|---------|
| Skill | `vinyl-reel` | Full reel production workflow — triggered automatically when you describe a vinyl unboxing task |
| Command | `/vinyl-reel` | Slash command to start reel creation directly, optionally passing a folder path |

## Setup

The voiceover generation requires an ElevenLabs API key.

1. After installing the plugin, open `skills/vinyl-reel/.env.example`
2. Copy it to `skills/vinyl-reel/.env`
3. Replace `your_api_key_here` with your actual ElevenLabs API key

The `ELEVENLABS_VOICE_ID` is pre-filled with the cloned voice — leave it as-is unless you want to use a different voice.

## Usage

**Via skill (automatic):** Just describe what you want — "make a reel for this album", "vinyl unboxing video", "create a YouTube Short from my clips" — and the skill triggers automatically.

**Via command:** Type `/vinyl-reel /path/to/your/album-folder` to start immediately.

### Expected folder structure

Your album folder should look like this:

```
Album Name/
├── video/        # Raw clips (.mp4, .mov, etc.)
├── audio/        # Background music samples (.mp3, .m4a, .wav)
```

The subscribe button animation overlay is bundled in the plugin — no need to include it.

## Workflow

The skill runs 6 phases:

1. **Scan & Catalog** — inventories and thumbnails all clips
2. **Research Album** — web searches for artist/album/edition context
3. **Write Voiceover Script** — pauses here for your review and approval
4. **Generate Voiceover** — calls ElevenLabs with the approved script
5. **Arrange & Mix** — edits clips, adds text overlays, mixes audio
6. **Export** — outputs `<Album>_Reel.mp4` (YouTube, with subscribe overlay) and `<Album>_Reel_Clean.mp4` (Instagram), plus `youtube_metadata.md`
