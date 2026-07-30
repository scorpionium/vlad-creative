# discography-reel

Creates a ≤59s 9:16 discography reel showcasing a band's complete studio discography. Two video clips + one audio sample per album, chronological oldest to newest, equal duration per album, animated album name overlay at the top. No voiceover — text does the talking. The reel closes with a 4s end card ("What is your favorite album? Let me know in the comments.") — built from your optional custom ending clip (dropped in `outro/`) or a freeze-frame of the last shot — and the total, end card included, stays ≤59s. Outputs a clean version and a YouTube Shorts version with the subscribe button animation.

## Install

```
/plugin marketplace add scorpionium/vlad-creative
/plugin install discography-reel@vlad-creative
```

## Usage

```
/discography-reel Band Name
```

Or describe what you want — "make a discography reel for Drudkh" — and the skill triggers automatically.

## Workflow

1. **Research** — looks up the band's studio discography (Wikipedia + corroboration), computes per-album timing
2. **Create folders + PAUSE** — creates `<Band> Discography/NN_<Album>_(<Year>)/video/` and `audio/` for every studio album; waits for you to drop in two video clips and one audio file per album, then asks for per-album cover start offsets
3. **Scan & validate** — verifies all asset folders before assembly
4. **Assemble & export** — builds per-album segments with animated album labels, appends the 4s outro end card, concatenates with crossfades, exports two MP4s and metadata

## Input folder structure (auto-created in Phase 2)

```
<Band Name> Discography/
├── outro/        # optional: 1 custom ending clip (first 4s used; own audio kept if present)
├── 01_<Album1>_(<Year1>)/
│   ├── video/    # exactly 2 video clips (1_cover.*, 2_turntable.*)
│   └── audio/    # exactly 1 audio sample
├── 02_<Album2>_(<Year2>)/
│   ├── video/
│   └── audio/
└── ...
```

## Outputs

| File | Description |
|------|-------------|
| `BANDNAME_Discography_YEARFIRST-YEARLAST.mp4` | Clean version |
| `BANDNAME_Discography_YEARFIRST-YEARLAST_yt.mp4` | YouTube Shorts with subscribe overlay at t=20s |
| `BANDNAME_Discography_metadata.md` | EN + UA titles, album list, hashtags |

## Requirements

- Python 3
- ffmpeg + ffprobe (with `xfade`, `acrossfade`, `chromakey`, `drawtext` filters)
