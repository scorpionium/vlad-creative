# discography-reel

Creates a ≤59s 9:16 discography reel showcasing a band's discography — studio albums only, or studio albums + EPs. Two or three video clips + one audio sample per album, chronological oldest to newest, equal duration per album, big animated album name overlay at the top. No voiceover — text does the talking. The reel opens with a "Full BAND NAME Discography" title — over your optional 3s intro clip (dropped in `intro/`) or over the first album — and closes with a 4s end card ("What is your favorite album? Let me know in the comments.") — built from your optional custom ending clip (dropped in `outro/`) or a freeze-frame of the last shot — and the total, intro and end card included, stays ≤59s. Outputs a clean version and a YouTube Shorts version with the subscribe button animation.

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

1. **Research** — asks whether to cover studio albums only or albums + EPs, looks up the discography (Wikipedia + corroboration), computes per-album timing
2. **Create folders + PAUSE** — asks clips per album (2: cover + turntable, or 3: showing + cover + turntable) and whether you'll add a 3s intro clip; creates `<Band> Discography/NN_<Album>_(<Year>)/video/` and `audio/` for every release plus `intro/` and `outro/`; waits for you to drop in the clips and one audio file per album, then asks for per-album cover start offsets
3. **Scan & validate** — verifies all asset folders before assembly
4. **Assemble & export** — builds per-album segments with animated album labels, opens with the intro/title, appends the 4s outro end card, concatenates with crossfades, exports two MP4s and metadata

## Input folder structure (auto-created in Phase 2)

```
<Band Name> Discography/
├── intro/        # optional: 1 intro clip (first 3s used; own audio kept if present)
├── outro/        # optional: 1 custom ending clip (first 4s used; own audio kept if present)
├── 01_<Album1>_(<Year1>)/
│   ├── video/    # 2 clips (1_cover.*, 2_turntable.*) or 3 clips (1_showing.*, 2_cover.*, 3_turntable.*)
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
