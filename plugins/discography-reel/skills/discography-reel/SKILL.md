---
name: discography-reel
description: >
  Create a ≤59s 9:16 discography reel showcasing a band's complete studio discography.
  One video + audio clip per album, chronological oldest to newest, equal duration per album,
  animated album name text overlay at the top, closing 4s end card asking viewers to comment
  their favorite album. Trigger when the user wants a discography reel,
  "band discography video", "all albums reel", or references making a short about a band's
  full catalogue.
---

# Discography Reel Maker

Create a ≤59-second 9:16 discography reel (YouTube Shorts / Instagram Reels) showcasing a
band's complete studio discography — one video + audio clip per album, chronological order,
equal duration per album, animated album name overlay at the top of each section, no
voiceover. The reel closes with a 4-second outro end card ("What is your favorite album?")
that invites comments.

## Workflow Overview

```
Phase 1: Research Discography  ──► Phase 2: Create Folders (PAUSE: populate assets)
  ──► Phase 3: Scan & Validate  ──► Phase 4: Assemble & Export
```

Phases 1, 3, and 4 run automatically. Phase 2 has one pause for the user to populate
the per-album asset folders.

---

## Phase 1: Research Studio Discography

Web-search the band's studio discography using at least two sources (Wikipedia preferred,
plus a corroborating source such as Metal-Archives, AllMusic, or Discogs):

```
"<BAND NAME>" studio discography
"<BAND NAME>" discography site:en.wikipedia.org
```

**Include ONLY studio albums.** Strictly exclude:
- EPs, singles, split releases
- Compilations, best-ofs, anthologies
- Live albums, concert recordings
- Demos, promos, bootlegs
- Box sets, reissues counted as separate entries

Sort chronologically (oldest first). Number them 1…N.

**For each album, research one suggested audio sample** using Last.fm, Spotify charts, or
fan/review sources (AllMusic, Metal-Archives reviews, RateYourMusic). Search:

```
"<BAND NAME>" "<ALBUM NAME>" most popular song
"<BAND NAME>" "<ALBUM NAME>" best track site:last.fm OR site:rateyourmusic.com
```

Pick the track that best satisfies **both** criteria:
1. **Most recognisable** — highest play count, biggest single, or the track the band is
   known for from that album.
2. **Catchy opening** — the hook, riff, or melody hits within the first 3–5 seconds so
   even a short section_sec clip lands immediately. Avoid slow intros, long instrumental
   buildups, or fade-ins.

If two tracks tie on popularity, prefer the one with the more immediately striking opening.

**Compute timing** (4 seconds are reserved at the tail for the outro end card):
```
outro_sec   = 4
section_sec = floor((59 - outro_sec) / N) = floor(55 / N)
content_sec = section_sec * N
total_sec   = content_sec + outro_sec        # always <= 59
```

Reference table:

| N albums | section_sec | content_sec | total_sec | note              |
|----------|-------------|-------------|-----------|-------------------|
| 4        | 13          | 52          | 56        | comfortable       |
| 5        | 11          | 55          | 59        | comfortable       |
| 8        | 6           | 48          | 52        | comfortable       |
| 10       | 5           | 50          | 54        | comfortable       |
| 12       | 4           | 48          | 52        | minimum workable  |
| 13       | 4           | 52          | 56        | minimum workable  |
| 14       | 3           | 42          | 46        | too fast — split  |
| 19       | 2           | 38          | 42        | too fast — split  |

**Minimum viable time per album is 4 seconds.** Below that, the viewer cannot read the album
name overlay, recognise the audio snippet, or appreciate the clip before the crossfade hits.

Show the user a numbered table including the suggested sample track for each album:

```
Studio discography: N albums  →  section_sec s each + 4 s outro  →  total_sec s total

 1. Album Name One (1985)    — Xs   ♪ "Suggested Track Title"
 2. Album Name Two (1987)    — Xs   ♪ "Suggested Track Title"
 ...
```

The ♪ suggestion is a starting point — the user can use any track they prefer.

**Timing checks (evaluate in order):**

1. If `section_sec >= 4`: proceed normally.

2. If `section_sec == 3` (N = 14–18 albums): suggest splitting into two parts.
   Compute split sizes: `part1 = ceil(N / 2)`, `part2 = N - part1`.
   Show the user:

   > "At 3 s per album the reel will feel very rushed. I recommend splitting into two
   > parts: Part 1 (albums 1–`part1`, `floor(55/part1)` s each) and Part 2
   > (albums `part1+1`–N, `floor(55/part2)` s each).
   > Reply **split** to make two reels, or **single** to continue as one."

   Wait for the user's choice. If **split**, run Phases 2–4 twice — once per part — using
   the same asset folders; each part gets its own outro end card. If **single**, continue
   with `section_sec = 3` and note it will be fast-paced.

3. If `section_sec <= 2` (N ≥ 19 albums): splitting is required.
   Compute split sizes as above and tell the user:

   > "At `section_sec` s per album a single reel is not watchable. I'll produce two parts:
   > Part 1 (albums 1–`part1`) and Part 2 (albums `part1+1`–N).
   > Confirm to continue."

   Wait for confirmation, then run Phases 2–4 twice.

---

## Phase 2: Create Working Directory + Asset Folders (PAUSE)

Create a working directory in the current directory:
```
<Band Name> Discography/
```

For each album i (1…N), create two subfolders. Use the naming convention:
- Zero-pad the index to 2 digits: `01`, `02`, … `NN`
- Replace spaces with underscores in the album name
- Strip special characters (colons, slashes, apostrophes, quotes, asterisks) from the album name

Also create one optional folder `outro/` at the top level for a custom ending clip.

```
<Band Name> Discography/
├── outro/              ← optional: one custom ending clip for the end card
├── 01_<AlbumName>_(<Year>)/
│   ├── video/          ← drop 1_cover.<ext> AND 2_turntable.<ext> here
│   └── audio/
├── 02_<AlbumName>_(<Year>)/
│   ├── video/
│   └── audio/
└── ...
```

Show the complete folder tree to the user.

### PAUSE — Step 1: Populate asset folders

Tell the user:

"Asset folders are ready. Please drop **exactly two video clips** and **exactly one audio sample**
into each album's subfolders:

- `video/1_cover.<ext>` — cover art footage for that album (zoom-pan, static cover shot, etc.)
- `video/2_turntable.<ext>` — LP spinning on the turntable
- `audio/<anything>.<ext>` — audio sample (one file)

Video formats accepted: `.mp4 .mov .avi .mkv .m4v`
Audio formats accepted: `.m4a .mp3 .wav .aac .flac .ogg`

The files are sorted alphabetically, so `1_cover` will always be the cover sub-clip and
`2_turntable` will always be the turntable sub-clip.

For the audio sample, I suggested a track for each album above (♪) — pick a file that starts
at or near the catchy hook so the best seconds land within your section window.

**Optional:** drop a single video clip into `outro/` to use as the ending card background
(where the reel asks 'What is your favorite album?'). Only the first 4 seconds are used, so
pre-trim it if the moment you want isn't at the start. If it has its own audio (e.g. you
asking on camera), that audio is used; if it's silent, the last album's music continues over
it. If you leave `outro/` empty, I'll freeze the last frame of the final album instead.

Confirm here when all folders are populated."

**Wait for the user's confirmation before continuing.**

### PAUSE — Step 2: Cover clip start offsets

After the user confirms assets are in place, show this table and ask for offsets:

"Thanks! One more thing before I start — I need to know **at what timestamp (in seconds)
to begin the 4-second excerpt** from each cover clip. Reply with a comma-separated list of
offsets in album order (e.g. `0, 2, 5, 0`). Leave blank or use `0` for any album where the
clip should start from the beginning.

| # | Album | Cover video |
|---|-------|-------------|
| 1 | <Album 1 name> (<Year>) | `1_cover.*` |
| 2 | <Album 2 name> (<Year>) | `1_cover.*` |
...

Cover offsets (seconds, comma-separated):"

**Wait for the user's reply.** Parse the offsets into a list `cover_offsets[1..N]`.
Defaults to `0` for any album left blank or not provided.

**Continue to Phase 3 once offsets are received.**

---

## Phase 3: Scan & Validate

Read the ffmpeg patterns reference first:
```
Read <skill-path>/references/ffmpeg_patterns.md
```

Then run the scan script:
```bash
python3 <skill-path>/scripts/scan_assets.py "<Band Name> Discography"
```

The script outputs JSON with `errors[]` and per-album asset paths.

**If errors exist:** list every error clearly (missing video, missing audio, multiple files
found, unreadable file). Stop. Tell the user to fix the listed folders and confirm again.
Re-run the scan after confirmation. Do NOT proceed with an invalid asset structure.

**If all valid:** echo the scan summary (N albums, total duration), then run two extra
checks (the scan script does not cover `outro/`):

1. **Outro clip (optional):** glob `<WORK_DIR>/outro/` for video files (same extensions as
   album clips). Exactly one → note it will be used for the end card. More than one → ask
   the user which to use. Empty or missing folder → freeze-frame fallback.
2. **Last-album audio length (non-blocking, music-mode outro only):** if the **last**
   album's `audio_duration` (from the scan JSON) is less than `section_sec + outro_sec`,
   warn the user that its music will run out during the outro end card (the tail will be
   silent — `apad` covers it) and offer to proceed anyway or swap in a longer sample. Skip
   this check when a custom outro clip with its own audio is used.

Then continue to Phase 4.

---

## Phase 4: Assemble & Export

Variables established in earlier phases:
- `BAND` — band name (ALL CAPS for metadata, original case for paths)
- `N` — number of albums
- `section_sec` — integer seconds per album
- `outro_sec` — `4` — duration of the outro end card
- `content_sec` — `section_sec * N`; `total_sec = content_sec + outro_sec`
- `cover_sec` — `min(4, section_sec)` — duration of each cover sub-clip
- `turntable_sec` — `section_sec - cover_sec` — duration of each turntable sub-clip
- `cover_offsets[1..N]` — per-album start offset in seconds for cover clip (default 0)
- `YEAR_FIRST` — year of album 1
- `YEAR_LAST` — year of album N
- `WORK_DIR` — `<Band Name> Discography`
- `WORK` — `<WORK_DIR>/.work` (create if needed)
- `OUTRO_CLIP` — the video file in `<WORK_DIR>/outro/`, if any (from Phase 3)
- `SUBSCRIBE` — path to subscribe animation (see 4f)

```bash
mkdir -p "$WORK_DIR/.work"
```

### 4a. Detect Fonts

Check for available fonts:
```bash
fc-list | grep -i "LiberationSans-Bold"
fc-list | grep -i "DejaVuSans-Bold"
fc-list | grep -i "LiberationSans-Regular"
fc-list | grep -i "DejaVuSans"
```

Use the first font found for each weight.

`<bold_font>` fallback order (album labels + outro question line):
1. `/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf`
2. `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`
3. Any bold `.ttf` reported by `fc-list`

`<regular_font>` fallback order (outro CTA line only):
1. `/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf`
2. `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`
3. Reuse `<bold_font>`

### 4b. Build Per-Album Segments

Each album i produces **two sub-clips** (`a` = cover, `b` = turntable). The audio file is
trimmed to match each sub-clip's duration.

Compute per-album:
```
cover_sec      = min(4, section_sec)
turntable_sec  = section_sec - cover_sec
cover_offset_i = cover_offsets[i]   # from Phase 2 Step 2
```

**Sub-clip A — cover (`segment_<NN>a.mp4`):**

The label on sub-clip A is animated: it fades in over 0.35s while rising ~30px into its
resting position (ease-out quad). The `y` and `alpha` expressions contain commas, so they
**must stay single-quoted** or the filtergraph parser splits on them.

```bash
ffmpeg -y \
  -ss <cover_offset_i> -t <cover_sec> -i "<cover_video_file>" \
  -ss 0                -t <cover_sec> -i "<audio_file>" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,
       pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,
       drawtext=fontfile=<bold_font>:\
         text='<Album Name> (<Year>)':\
         fontcolor=white:fontsize=40:\
         x=(w-text_w)/2:y='60+30*pow(1-clip(t/0.35,0,1),2)':\
         alpha='clip(t/0.35,0,1)':\
         box=1:boxcolor=black@0.5:boxborderw=12:\
         shadowcolor=black@0.6:shadowx=2:shadowy=2" \
  -af "apad,atrim=0:<cover_sec>,asetpts=PTS-STARTPTS" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  "<WORK>/segment_<NN>a.mp4"
```

**Sub-clip B — turntable (`segment_<NN>b.mp4`):**
```bash
ffmpeg -y \
  -ss 0 -t <turntable_sec> -i "<turntable_video_file>" \
  -ss <cover_sec> -t <turntable_sec> -i "<audio_file>" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,
       pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,
       drawtext=fontfile=<bold_font>:\
         text='<Album Name> (<Year>)':\
         fontcolor=white:fontsize=40:\
         x=(w-text_w)/2:y=60:\
         box=1:boxcolor=black@0.5:boxborderw=12:\
         shadowcolor=black@0.6:shadowx=2:shadowy=2" \
  -af "apad,atrim=0:<turntable_sec>,asetpts=PTS-STARTPTS" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  "<WORK>/segment_<NN>b.mp4"
```

Notes:
- **Label animation (carry-over rule):** sub-clip A is the entrance — fade-in + 30px
  ease-out rise over 0.35s, fully settled at `y=60`/`alpha=1` long before `cover_sec` ends,
  so the 0.3s A→B crossfade over the identical static label on B is invisible. Sub-clip B
  is the continuation — static, no `alpha`. The exit is handled for free by the 0.5s
  album-boundary (or outro) xfade dissolving the whole frame. The same animated A expression
  applies unchanged when sub-clip B is skipped (`turntable_sec == 0`).
- The drawtext `alpha` expression also fades the `box=1` background and shadow, so box and
  text rise and fade in together — this is the intended look.
- This produces `2N` segments total: `segment_01a.mp4`, `segment_01b.mp4`, `segment_02a.mp4`, …
- `-ss <cover_offset_i>` on the cover input seeks to the user-specified start offset (fast
  demuxer seek). For sources shorter than `cover_sec` after the offset, add `tpad=stop_mode=clone`
  to `-vf` and `apad` to `-af` (already present).
- For the turntable sub-clip, `-ss <cover_sec>` on the audio input continues where cover left off
  so the audio plays continuously across both sub-clips.
- If `turntable_sec == 0` (i.e. `section_sec <= 4`), skip sub-clip B; only sub-clip A exists
  for that album. Adjust the segment list and transition chain accordingly.
- Escape special characters in album names: apostrophes → `'\''`, colons → `\:`.

### 4c. Build Outro Segment (End Card)

A 4-second end card closes the reel, darkened 45% with two animated text lines inviting
comments. The background is the user's **custom outro clip** (`OUTRO_CLIP` from Phase 3)
when one was provided, otherwise a **freeze-frame** of the final album's footage. The
treatment (darken + text) is identical in both variants.

`<last_audio>` = the last album's audio file.

**Determine the audio mode first:**
```bash
# custom clip present — does it carry audio?
ffprobe -v quiet -select_streams a -show_entries stream=index -of csv=p=0 "$OUTRO_CLIP"
```
```
outro_audio = clip    if OUTRO_CLIP exists AND the probe printed anything
            = music   otherwise (last album's music continues into the card)
```
Record `outro_audio` — 4e picks its fade duration from it.

#### Variant A — custom outro clip

Single command. Only the first 4 seconds of the clip are used (`-ss 0 -t 4`); if the clip
is shorter, `tpad`/`apad` freeze-fill the remainder.

In **clip audio mode** there is one input — video and audio both come from `$OUTRO_CLIP`:
```bash
ffmpeg -y \
  -ss 0 -t 4 -i "$OUTRO_CLIP" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,
       pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,
       drawbox=x=0:y=0:w=iw:h=ih:color=black@0.45:t=fill,
       drawtext=fontfile=<bold_font>:\
         text='What is your favorite album?':\
         fontcolor=white:fontsize=56:\
         x=(w-text_w)/2:y='h*0.42+30*pow(1-clip((t-0.6)/0.35,0,1),2)':\
         alpha='clip((t-0.6)/0.35,0,1)':\
         shadowcolor=black@0.7:shadowx=4:shadowy=4,
       drawtext=fontfile=<regular_font>:\
         text='Let me know in the comments.':\
         fontcolor=white@0.9:fontsize=44:\
         x=(w-text_w)/2:y='h*0.42+100+30*pow(1-clip((t-0.72)/0.35,0,1),2)':\
         alpha='clip((t-0.72)/0.35,0,1)':\
         shadowcolor=black@0.7:shadowx=3:shadowy=3" \
  -af "apad,atrim=0:4,asetpts=PTS-STARTPTS" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  "<WORK>/segment_outro.mp4"
```

In **music mode** (clip has no audio stream), add the last album's audio as a second input
right after the clip input — the rest of the command is identical:
```bash
  -ss 0 -t 4 -i "$OUTRO_CLIP" \
  -ss <section_sec> -t 4 -i "<last_audio>" \
```
If the clip is shorter than 4s, append `tpad=stop_mode=clone` to the `-vf` chain (before
`drawbox`) so the last frame holds; `apad` already covers the audio.

The chain's final 0.5s `acrossfade` (4d) blends the last album's music into whichever audio
the outro carries — no extra handling needed at the boundary.

#### Variant B — freeze-frame (no custom clip)

Built in two steps.

**Step 1 — extract the freeze-frame.** Extract from the **raw source video**, not the
encoded segment — the segment has the album label burned in, and the end card must stay
clean of it:
```
<last_video> = the last album's 2_turntable file
               (or its 1_cover file when turntable_sec == 0)
<last_t>     = turntable_sec - 0.1
               (or cover_offset + cover_sec - 0.1 when turntable_sec == 0)
```
```bash
ffmpeg -y -ss <last_t> -i "<last_video>" -frames:v 1 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,
       pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -update 1 "<WORK>/outro_frame.png"
```
If no frame is produced (e.g. the source is shorter than `<last_t>` because the segment was
tpad-padded), retry with `-sseof -0.5 -i "<last_video>"` in place of the `-ss` seek.

**Step 2 — build the outro segment:**
```bash
ffmpeg -y \
  -loop 1 -framerate 30 -t 4 -i "<WORK>/outro_frame.png" \
  -ss <section_sec> -t 4 -i "<last_audio>" \
  -vf "drawbox=x=0:y=0:w=iw:h=ih:color=black@0.45:t=fill,
       drawtext=fontfile=<bold_font>:\
         text='What is your favorite album?':\
         fontcolor=white:fontsize=56:\
         x=(w-text_w)/2:y='h*0.42+30*pow(1-clip((t-0.6)/0.35,0,1),2)':\
         alpha='clip((t-0.6)/0.35,0,1)':\
         shadowcolor=black@0.7:shadowx=4:shadowy=4,
       drawtext=fontfile=<regular_font>:\
         text='Let me know in the comments.':\
         fontcolor=white@0.9:fontsize=44:\
         x=(w-text_w)/2:y='h*0.42+100+30*pow(1-clip((t-0.72)/0.35,0,1),2)':\
         alpha='clip((t-0.72)/0.35,0,1)':\
         shadowcolor=black@0.7:shadowx=3:shadowy=3" \
  -af "apad,atrim=0:4,asetpts=PTS-STARTPTS" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  "<WORK>/segment_outro.mp4"
```

Notes (both variants):
- In Variant B the freeze-frame is scale/padded to 1080x1920 during extraction, so the
  outro build applies no further scaling; in Variant A the scale/pad runs on the clip.
- `-ss <section_sec>` on a music-mode audio input continues the last album's music exactly
  where sub-clip B stopped; `apad` fills with silence if the sample runs short.
- The text delays (0.6s / 0.72s) let the incoming 0.5s crossfade settle before the lines
  animate in (fade + slide-up, staggered like the album labels).
- **No fade-out on the text** — the card holds to the last frame: it is the comment prompt
  and the loop point of the Short.

### 4d. Concatenate Segments with Crossfades

Use chained `xfade` + `acrossfade` filter_complex for smooth transitions between all `2N`
content segments (`segment_01a`, `segment_01b`, `segment_02a`, …) plus `segment_outro` as
the final chain element (`2N + 1` inputs when every album has both sub-clips).

**Crossfade durations:**
- **Within-album** (A→B, i.e. cover→turntable): `0.3s`
- **Album-boundary** (B→A, i.e. turntable of album i → cover of album i+1): `0.5s`
- **Into the outro** (last content segment → `segment_outro`): `0.5s` (boundary-style)

**Segment sequence (0-indexed):** `[01a, 01b, 02a, 02b, …, NNa, NNb, outro]`
- Even-indexed transitions (0, 2, 4, …) are within-album: `x = 0.3`
- Odd-indexed transitions (1, 3, 5, …) are album-boundary: `x = 0.5`
- The final transition (into the outro) is always `x = 0.5`

**Segment durations:** `d[2k] = cover_sec`, `d[2k+1] = turntable_sec` (for album k+1);
`d[last] = outro_sec = 4`

**Offset formula** (the offsets must be strictly increasing and in output-timeline seconds):
```
O[0] = d[0] - x[0]
O[i] = O[i-1] + (d[i] - x[i-1]) - x[i]    for i >= 1
     = sum(d[0..i]) - sum(x[0..i])
```

Compute all offsets before writing the filter_complex. Round to 2 decimal places.

Build the filter_complex dynamically. Example for N=2 albums (5 segments, 4 transitions):
```
# segments: 01a(cover_sec), 01b(turntable_sec), 02a(cover_sec), 02b(turntable_sec), outro(4)
# transitions: 0=within(0.3), 1=boundary(0.5), 2=within(0.3), 3=outro(0.5)
-filter_complex "
  [0:v][1:v]xfade=transition=fade:duration=0.3:offset=<O0>[v01];
  [v01][2:v]xfade=transition=fade:duration=0.5:offset=<O1>[v02];
  [v02][3:v]xfade=transition=fade:duration=0.3:offset=<O2>[v03];
  [v03][4:v]xfade=transition=fade:duration=0.5:offset=<O3>[vout];
  [0:a][1:a]acrossfade=d=0.3:c1=tri:c2=tri[a01];
  [a01][2:a]acrossfade=d=0.5:c1=tri:c2=tri[a02];
  [a02][3:a]acrossfade=d=0.3:c1=tri:c2=tri[a03];
  [a03][4:a]acrossfade=d=0.5:c1=tri:c2=tri[aout]
" -map "[vout]" -map "[aout]"
```

**Special cases:**
- If `turntable_sec == 0` for some albums, those albums have only one segment (sub-clip A).
  Adjust the segment list and transition types accordingly.
- N=1: the chain is `[01a, 01b, outro]` (or `[01a, outro]` when `turntable_sec == 0`).
  The outro means there are always at least 2 chain elements — the single-segment copy
  case no longer occurs.

Full assemble command:
```bash
ffmpeg -y \
  -i "<WORK>/segment_01a.mp4" \
  -i "<WORK>/segment_01b.mp4" \
  -i "<WORK>/segment_02a.mp4" \
  -i "<WORK>/segment_02b.mp4" \
  ... \
  -i "<WORK>/segment_outro.mp4" \
  -filter_complex "<generated_filter_complex>" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  "<WORK>/assembled.mp4"
```

### 4e. Clean Export with Audio Fade-Out

Pick the fade duration from the outro audio mode (4c):
```
FADE_DUR = 3    if outro_audio == music  (music breathes out across the end card)
         = 1    if outro_audio == clip   (don't fade a spoken ask down — just avoid an
                                          abrupt ending)
```

Derive the fade-out start from the **actual** assembled duration (do NOT use `total_sec` —
the assembled file is shorter than `total_sec` by the crossfade overlap, so a
`total_sec`-based start can land past end-of-file and silently apply no fade):

```bash
D=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "<WORK>/assembled.mp4")
FADE_START=$(python3 -c "print(max(0, float('$D') - <FADE_DUR>))")
```

Re-encode assembled.mp4 applying the fade-out to the audio:
```bash
ffmpeg -y \
  -i "<WORK>/assembled.mp4" \
  -af "afade=t=out:st=$FADE_START:d=<FADE_DUR>" \
  -c:v copy \
  -c:a aac -b:a 192k \
  "<WORK_DIR>/<BAND_SLUG>_Discography_<YEAR_FIRST>-<YEAR_LAST>.mp4"
```

Where `<BAND_SLUG>` = band name with spaces replaced by underscores, special chars stripped.

### 4f. YouTube Shorts Export (subscribe overlay at t=20s)

Read the audio fade-out from the 4e output (not assembled.mp4 directly) so the fade is
inherited automatically via `-c:a copy`.

Locate the subscribe animation:
```bash
SUBSCRIBE="<skill-path>/assets/subscribe_btn_animation_small.mp4"
```

The `<skill-path>` is the directory containing this SKILL.md file.

Apply overlay starting at t=20s using `-itsoffset 20`:
```bash
ffmpeg -y \
  -i "<WORK_DIR>/<BAND_SLUG>_Discography_<YEAR_FIRST>-<YEAR_LAST>.mp4" \
  -itsoffset 20 -i "$SUBSCRIBE" \
  -filter_complex " \
    [1:v]chromakey=0x00FF00:0.3:0.1,scale=1080:-1[sub]; \
    [0:v][sub]overlay=(W-w)/2:(H-h)/2:eof_action=pass[out]" \
  -map "[out]" -map "0:a" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a copy \
  "<WORK_DIR>/<BAND_SLUG>_Discography_<YEAR_FIRST>-<YEAR_LAST>_yt.mp4"
```

If `total_sec <= 20`, skip the subscribe overlay (the animation would not appear within
the video duration). Mention this to the user.

### 4g. Generate Metadata

Write `<WORK_DIR>/<BAND_SLUG>_Discography_metadata.md` with English and Ukrainian sections.

**BAND NAME in ALL CAPS** everywhere in titles and descriptions.
**No em dashes (—) anywhere.** Use plain hyphens `-` as separators.

```markdown
# BAND NAME - Full Discography (<YEAR_FIRST>-<YEAR_LAST>)

---

## English

**Title:** BAND NAME - Full Discography (<YEAR_FIRST>-<YEAR_LAST>) #vinyl

**Description:**
BAND NAME is a <genre> band from <country>, active since <year>.
This reel covers their complete studio discography — N albums from <YEAR_FIRST> to <YEAR_LAST>.

Albums:
1. Album Name (YEAR)
2. Album Name (YEAR)
...

Subscribe for weekly metal vinyl from my collection.

#BandName #Discography #vinyl #vinylcollection #youtubeShorts #metal #<genre>

---

## Ukrainian

**Назва:** BAND NAME - Повна дискографія (<YEAR_FIRST>-<YEAR_LAST>) #vinyl

**Опис:**
BAND NAME — <genre> гурт з <country>, заснований у <year>.
Цей ролик охоплює повну студійну дискографію — N альбомів від <YEAR_FIRST> до <YEAR_LAST>.

Альбоми:
1. Album Name (YEAR)
2. Album Name (YEAR)
...

Підписуйтесь — щотижня метал-вінілова колекція.

#BandName #Discography #vinyl #vinylcollection #youtubeShorts #metal #<genre>
```

---

## Summary Output

After Phase 4 completes, tell the user:

```
Done! Outputs saved to: <WORK_DIR>/

  <BAND_SLUG>_Discography_<YEAR_FIRST>-<YEAR_LAST>.mp4     — clean version
  <BAND_SLUG>_Discography_<YEAR_FIRST>-<YEAR_LAST>_yt.mp4  — YouTube Shorts (subscribe at t=20s)
  <BAND_SLUG>_Discography_metadata.md                       — EN + UA titles and descriptions

Both videos end with a 4 s end card asking viewers to comment their favorite album.
```

---

## Error Handling

- **Source clip shorter than section_sec:** Add `tpad=stop_mode=clone` to freeze the last
  frame for the remaining duration. Add `apad` for audio (already in the segment command).
- **Font not found:** Try `fc-list` to find any available bold TTF. If none, omit
  `fontfile=` — ffmpeg will use its default font (text will still render, just less styled).
- **Crossfade offset calculation:** If the filter_complex fails with offset errors,
  double-check that the O_i values are strictly increasing and rounded to 2 decimal places.
- **assembled.mp4 duration check:** After assembly, verify duration with ffprobe. When every
  album has both sub-clips, it should be approximately
  `content_sec + 4 - (0.3 * N + 0.5 * N)` due to crossfade overlap. This is expected.
- **outro_frame.png empty or missing:** Retry the extraction with `-sseof -0.5` on the raw
  source (replacing the `-ss <last_t>` seek).
- **Multiple files in `outro/`:** ask the user which one to use (Phase 3 should have
  caught this).
- **Custom outro clip shorter than 4s:** `tpad=stop_mode=clone` in `-vf` holds the last
  frame; `apad` covers the audio.
- **Last album audio shorter than `section_sec + 4`:** `apad` fills the outro tail with
  silence — acceptable for an end card. The Phase 3 check should already have warned the user.
- **Subscribe asset not found:** If `<skill-path>/assets/subscribe_btn_animation_small.mp4`
  is missing, skip the `_yt.mp4` export and tell the user — the asset should be bundled
  with the plugin.
- **N=1 (band with only 1 studio album):** The chain is `[01a, 01b, outro]` with
  transitions `0.3, 0.5` — or `[01a, outro]` with a single `0.5` when turntable_sec == 0.
  Subscribe overlay still applied if total_sec > 20.
