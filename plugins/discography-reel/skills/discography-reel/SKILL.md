---
name: discography-reel
description: >
  Create a ≤59s 9:16 discography reel showcasing a band's discography (studio albums,
  optionally including EPs). Two or three video clips + one audio sample per album,
  chronological oldest to newest, equal duration per album, animated album name text
  overlay at the top, optional 3s intro clip under a "Full BAND Discography" opening
  title, closing 4s end card asking viewers to comment their favorite album. Trigger
  when the user wants a discography reel, "band discography video", "all albums reel",
  or references making a short about a band's full catalogue.
---

# Discography Reel Maker

Create a ≤59-second 9:16 discography reel (YouTube Shorts / Instagram Reels) showcasing a
band's discography (studio albums, optionally including EPs) — two or three video clips +
one audio sample per album, chronological order, equal duration per album, animated album
name overlay at the top of each section, no voiceover. The reel can open with a 3-second
intro clip under a "Full BAND NAME Discography" title and closes with a 4-second outro end
card ("What is your favorite album?") that invites comments.

## Workflow Overview

```
Phase 1: Research Discography  ──► Phase 2: Create Folders (PAUSE: populate assets)
  ──► Phase 3: Scan & Validate  ──► Phase 4: Assemble & Export
```

Phases 1, 3, and 4 run automatically. Phase 1 opens with one question (album scope).
Phase 2 opens with one question (clips per album + intro clip) and has one pause for the
user to populate the per-album asset folders.

---

## Phase 1: Research Discography

**First, ask the album scope** (AskUserQuestion, single question):

> Which releases should the reel cover?
> - **Studio albums only** (default) — the classic full-length discography.
> - **Studio albums + EPs** — LPs and EPs merged chronologically into one timeline.

Record `include_eps` (true/false). Singles, split releases, compilations, best-ofs,
anthologies, live albums, concert recordings, demos, promos, bootlegs, box sets, and
reissues counted as separate entries are **strictly excluded in both modes**.

Web-search the band's discography using at least two sources (Wikipedia preferred,
plus a corroborating source such as Metal-Archives, AllMusic, or Discogs):

```
"<BAND NAME>" studio discography
"<BAND NAME>" discography site:en.wikipedia.org
"<BAND NAME>" EPs discography          # only when include_eps
```

Sort chronologically (oldest first) — in EP mode, albums and EPs interleave in one
timeline. Number them 1…N. Record `N_albums` and `N_eps` (EP mode) for metadata, and tag
each EP entry so it can be annotated `[EP]` later.

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

**Compute timing** (4 seconds are reserved at the tail for the outro end card; 3 more at
the head when an intro clip is used):
```
outro_sec   = 4
intro_sec   = 3 if an intro clip is planned/present else 0
section_sec = floor((59 - outro_sec - intro_sec) / N)   # floor(55/N) or floor(52/N)
content_sec = section_sec * N
total_sec   = intro_sec + content_sec + outro_sec       # always <= 59
```

> **Phase 1 timing is provisional.** The intro clip and clips-per-album choices are made
> at the start of Phase 2, so compute this first pass with `intro_sec = 0` and 2-clip
> thresholds. Only a forced split (`section_sec <= 2`) is final here; Phase 2 re-runs the
> checks with the real parameters before creating folders.

Reference table — no intro, 2 clips (`floor(55/N)`):

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

Reference table — with intro, 2 clips (`floor(52/N)`):

| N albums | section_sec | content_sec | total_sec | note              |
|----------|-------------|-------------|-----------|-------------------|
| 4        | 13          | 52          | 59        | comfortable       |
| 5        | 10          | 50          | 57        | comfortable       |
| 8        | 6           | 48          | 55        | comfortable       |
| 10       | 5           | 50          | 57        | comfortable       |
| 12       | 4           | 48          | 55        | minimum workable  |
| 13       | 4           | 52          | 59        | minimum workable  |
| 14       | 3           | 42          | 49        | too fast — split  |
| 18       | 2           | 36          | 43        | too fast — split  |

**3-clip mode split** (showing / cover / turntable — see Phase 2):
```
showing_sec   = 2                                # fixed
cover_sec     = min(4, max(2, section_sec - 4))
turntable_sec = section_sec - showing_sec - cover_sec
```
Every sub-clip is ≥ 2s whenever `section_sec >= 6` — the **minimum viable section in
3-clip mode is 6 seconds** (vs 4 in 2-clip mode). Sub-clips are never skipped in 3-clip
mode.

Reference table — no intro, 3 clips (`floor(55/N)`):

| N albums | section_sec | split (show/cover/turn) | total_sec | note                          |
|----------|-------------|-------------------------|-----------|-------------------------------|
| 4        | 13          | 2 / 4 / 7               | 56        | comfortable                   |
| 5        | 11          | 2 / 4 / 5               | 59        | comfortable                   |
| 7        | 7           | 2 / 3 / 2               | 53        | comfortable                   |
| 8        | 6           | 2 / 2 / 2               | 52        | minimum workable              |
| 9        | 6           | 2 / 2 / 2               | 58        | minimum workable              |
| 10       | 5           | —                       | —         | too fast — split or 2-clip    |
| 14       | 3           | —                       | —         | forced split                  |

Reference table — with intro, 3 clips (`floor(52/N)`):

| N albums | section_sec | split (show/cover/turn) | total_sec | note                          |
|----------|-------------|-------------------------|-----------|-------------------------------|
| 4        | 13          | 2 / 4 / 7               | 59        | comfortable                   |
| 5        | 10          | 2 / 4 / 4               | 57        | comfortable                   |
| 6        | 8           | 2 / 4 / 2               | 55        | comfortable                   |
| 8        | 6           | 2 / 2 / 2               | 55        | minimum workable              |
| 9        | 5           | —                       | —         | too fast — split or 2-clip    |
| 14       | 3           | —                       | —         | forced split                  |

**Minimum viable time per album is 4 seconds (2-clip) / 6 seconds (3-clip).** Below that,
the viewer cannot read the album name overlay, recognise the audio snippet, or appreciate
the clips before the crossfade hits.

Show the user a numbered table including the suggested sample track for each album:

```
Discography: N albums  →  section_sec s each + 4 s outro  →  total_sec s total

 1. Album Name One (1985)         — Xs   ♪ "Suggested Track Title"
 2. Album Name Two (1987) [EP]    — Xs   ♪ "Suggested Track Title"
 ...
```

The ♪ suggestion is a starting point — the user can use any track they prefer.
(Annotate `[EP]` only in EP mode.)

**Timing checks (evaluate in order; thresholds depend on clip mode — 2-clip in this
provisional Phase 1 pass, the chosen mode when re-run in Phase 2):**

1. **2-clip:** if `section_sec >= 4`, proceed normally.
   **3-clip:** if `section_sec >= 6`, proceed normally.

2. **2-clip:** if `section_sec == 3`: suggest splitting into two parts.
   Compute split sizes: `part1 = ceil(N / 2)`, `part2 = N - part1`.
   Show the user:

   > "At 3 s per album the reel will feel very rushed. I recommend splitting into two
   > parts: Part 1 (albums 1–`part1`, `floor((55 - intro_sec)/part1)` s each) and Part 2
   > (albums `part1+1`–N, `floor((55 - intro_sec)/part2)` s each).
   > Reply **split** to make two reels, or **single** to continue as one."

   Wait for the user's choice. If **split**, run Phases 2–4 twice — once per part — using
   the same asset folders; each part gets its own outro end card (and its own intro, if an
   intro clip is used). If **single**, continue with `section_sec = 3` and note it will be
   fast-paced.

   **3-clip:** if `section_sec` is `4` or `5`: offer the same split, **plus a second way
   out — dropping to 2-clip mode** (which is workable down to `section_sec = 4`). The user
   picks split, 2-clip, or single-and-rushed is not offered (below the 3-clip minimum the
   turntable clip would hit 0–1s).

3. **2-clip:** if `section_sec <= 2` — **3-clip:** if `section_sec <= 3` — splitting is
   required. Compute split sizes as above and tell the user:

   > "At `section_sec` s per album a single reel is not watchable. I'll produce two parts:
   > Part 1 (albums 1–`part1`) and Part 2 (albums `part1+1`–N).
   > Confirm to continue."

   Wait for confirmation, then run Phases 2–4 twice.

---

## Phase 2: Create Working Directory + Asset Folders (PAUSE)

**First, ask the production options** (one AskUserQuestion with two questions):

> **Clips per album?**
> - **2 clips** (default) — `1_cover` (cover art footage) + `2_turntable` (LP spinning).
> - **3 clips** — `1_showing` (you showing/holding the LP) + `2_cover` + `3_turntable`.
>
> **Will you add a 3s intro clip?** (e.g. you presenting the collection — plays first,
> under a "Full BAND NAME Discography" title)
> - **Yes** — an `intro/` folder is created; the first 3 seconds of the clip open the reel.
> - **No** — the reel opens on album 1 with the title shown over its first sub-clip.

Record `clips_per_album` (2 or 3) and set `intro_sec = 3` (yes) or `0` (no). Then
**recompute the timing** (`section_sec`, `content_sec`, `total_sec`, and in 3-clip mode
the showing/cover/turntable split) and **re-run the Phase 1 timing checks** with the
mode-specific thresholds. Show the final per-album numbers to the user before creating
any folders.

Create a working directory in the current directory:
```
<Band Name> Discography/
```

For each album i (1…N), create two subfolders. Use the naming convention:
- Zero-pad the index to 2 digits: `01`, `02`, … `NN`
- Replace spaces with underscores in the album name
- Strip special characters (colons, slashes, apostrophes, quotes, asterisks) from the album name

Also create the optional top-level folders: `intro/` (only when the user said yes to the
intro clip) and `outro/` (always).

```
<Band Name> Discography/
├── intro/              ← optional: one intro clip (first 3s open the reel)
├── outro/              ← optional: one custom ending clip for the end card
├── 01_<AlbumName>_(<Year>)/
│   ├── video/          ← 2-clip: 1_cover.<ext> + 2_turntable.<ext>
│   └── audio/             3-clip: 1_showing.<ext> + 2_cover.<ext> + 3_turntable.<ext>
├── 02_<AlbumName>_(<Year>)/
│   ├── video/
│   └── audio/
└── ...
```

Show the complete folder tree to the user.

### PAUSE — Step 1: Populate asset folders

Tell the user (use the file list matching `clips_per_album`):

"Asset folders are ready. Please drop **exactly two video clips** [3-clip mode: **exactly
three video clips**] and **exactly one audio sample** into each album's subfolders:

2-clip mode:
- `video/1_cover.<ext>` — cover art footage for that album (zoom-pan, static cover shot, etc.)
- `video/2_turntable.<ext>` — LP spinning on the turntable
- `audio/<anything>.<ext>` — audio sample (one file)

3-clip mode:
- `video/1_showing.<ext>` — you showing/holding the LP to the camera
- `video/2_cover.<ext>` — cover art footage for that album (zoom-pan, static cover shot, etc.)
- `video/3_turntable.<ext>` — LP spinning on the turntable
- `audio/<anything>.<ext>` — audio sample (one file)

Video formats accepted: `.mp4 .mov .avi .mkv .m4v`
Audio formats accepted: `.m4a .mp3 .wav .aac .flac .ogg`

The files are sorted alphabetically, so the numeric prefixes (`1_`, `2_`, `3_`) determine
each clip's role.

For the audio sample, I suggested a track for each album above (♪) — pick a file that starts
at or near the catchy hook so the best seconds land within your section window.

**Intro (if chosen):** drop a single video clip into `intro/`. Only the **first 3 seconds**
are used, so pre-trim it if the moment you want isn't at the start. The 'Full <BAND NAME>
Discography' title appears over it. If the clip has its own audio (e.g. you speaking on
camera), that audio is used and crossfades into album 1's music; if it's silent, album 1's
music starts under the intro.

**Optional:** drop a single video clip into `outro/` to use as the ending card background
(where the reel asks 'What is your favorite album?'). Only the first 4 seconds are used, so
pre-trim it if the moment you want isn't at the start. If it has its own audio (e.g. you
asking on camera), that audio is used; if it's silent, the last album's music continues over
it. If you leave `outro/` empty, I'll freeze the last frame of the final album instead.

Confirm here when all folders are populated."

**Wait for the user's confirmation before continuing.**

### PAUSE — Step 2: Cover clip start offsets

After the user confirms assets are in place, show this table and ask for offsets. The
offsets apply to the **cover clip only** (`1_cover.*` in 2-clip mode, `2_cover.*` in
3-clip mode); showing and turntable clips always start from 0:

"Thanks! One more thing before I start — I need to know **at what timestamp (in seconds)
to begin the `cover_sec`-second excerpt** from each cover clip. Reply with a comma-separated
list of offsets in album order (e.g. `0, 2, 5, 0`). Leave blank or use `0` for any album
where the clip should start from the beginning.

| # | Album | Cover video |
|---|-------|-------------|
| 1 | <Album 1 name> (<Year>) | `1_cover.*` or `2_cover.*` |
| 2 | <Album 2 name> (<Year>) | `1_cover.*` or `2_cover.*` |
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

Then run the scan script with the chosen clip mode:
```bash
python3 <skill-path>/scripts/scan_assets.py "<Band Name> Discography" --clips <2|3>
```

The script outputs JSON with `errors[]` and per-album asset paths (in 3-clip mode each
album gains `showing_video` + `showing_video_duration`).

**If errors exist:** list every error clearly (missing video, missing audio, multiple files
found, unreadable file). Stop. Tell the user to fix the listed folders and confirm again.
Re-run the scan after confirmation. Do NOT proceed with an invalid asset structure.

**If all valid:** echo the scan summary (N albums, total duration), then run these extra
checks (the scan script does not cover `intro/` or `outro/`):

1. **Intro clip:** glob `<WORK_DIR>/intro/` for video files (same extensions as album
   clips). Exactly one → probe it for an audio stream:
   ```bash
   ffprobe -v quiet -select_streams a -show_entries stream=index -of csv=p=0 "<intro_file>"
   ```
   ```
   intro_audio = clip    if the probe printed anything
               = music   otherwise (album 1's music starts under the intro)
   ```
   More than one file → ask the user which to use. **Reconcile with the Phase 2 answer:**
   if the user said "no intro" but a clip is present (or said "yes" but the folder is
   empty), recompute `intro_sec`, `section_sec`, and the split checks, show the new
   numbers, and confirm with the user before continuing.
2. **Outro clip (optional):** glob `<WORK_DIR>/outro/` for video files (same extensions as
   album clips). Exactly one → note it will be used for the end card. More than one → ask
   the user which to use. Empty or missing folder → freeze-frame fallback.
3. **Last-album audio length (non-blocking, music-mode outro only):** if the **last**
   album's `audio_duration` (from the scan JSON) is less than `section_sec + outro_sec`
   (plus `intro_sec` when `N == 1` and `intro_audio == music`), warn the user that its
   music will run out during the outro end card (the tail will be silent — `apad` covers
   it) and offer to proceed anyway or swap in a longer sample. Skip this check when a
   custom outro clip with its own audio is used.
4. **Album-1 audio length (non-blocking, silent intro only):** when `intro_audio == music`,
   album 1's sample also plays under the intro, so warn if album 1's `audio_duration` is
   less than `intro_sec + section_sec` (the tail of its section will be silent — `apad`
   covers it).

Then continue to Phase 4.

---

## Phase 4: Assemble & Export

Variables established in earlier phases:
- `BAND` — band name (ALL CAPS for metadata, original case for paths)
- `N` — number of albums
- `include_eps` — whether EPs are included (Phase 1); `N_albums` / `N_eps` counts
- `clips_per_album` — `2` or `3` (Phase 2)
- `section_sec` — integer seconds per album
- `intro_sec` — `3` if an intro clip is used, else `0`
- `outro_sec` — `4` — duration of the outro end card
- `content_sec` — `section_sec * N`; `total_sec = intro_sec + content_sec + outro_sec`
- `showing_sec` — 3-clip mode only — `2` (fixed)
- `cover_sec` — 2-clip: `min(4, section_sec)`; 3-clip: `min(4, max(2, section_sec - 4))`
- `turntable_sec` — `section_sec - cover_sec` (2-clip) or
  `section_sec - showing_sec - cover_sec` (3-clip)
- `cover_offsets[1..N]` — per-album start offset in seconds for cover clip (default 0)
- `TITLE` — `Full <BAND NAME> Discography` (band name ALL CAPS)
- `INTRO_CLIP` — the video file in `<WORK_DIR>/intro/`, if any (from Phase 3)
- `intro_audio` — `clip` or `music` (from Phase 3; only set when `INTRO_CLIP` exists)
- `album1_audio_base` — `intro_sec` if `intro_audio == music`, else `0` — shift applied
  to every audio `-ss` of album 1's sub-clips (its sample's first `intro_sec` seconds
  play under the intro)
- `YEAR_FIRST` — year of album 1
- `YEAR_LAST` — year of album N
- `WORK_DIR` — `<Band Name> Discography`
- `WORK` — `<WORK_DIR>/.work` (create if needed)
- `OUTRO_CLIP` — the video file in `<WORK_DIR>/outro/`, if any (from Phase 3)
- `SUBSCRIBE` — path to subscribe animation (see 4f)

**Text size rule (album labels, intro/opening title):** count the characters of the exact
rendered string (album labels include the ` (<Year>)` suffix):
```
<= 24 chars  →  fontsize 64
25–34 chars  →  fontsize 48
>= 35 chars  →  fontsize 40
```
Referred to below as `<label_fs>` (per-album) and `<title_fs>` (for `TITLE`). All other
drawtext parameters stay the same at every size.

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

`<bold_font>` fallback order (album labels + intro title + outro question line):
1. `/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf`
2. `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`
3. Any bold `.ttf` reported by `fc-list`

`<regular_font>` fallback order (outro CTA line only):
1. `/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf`
2. `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`
3. Reuse `<bold_font>`

### 4b. Build Per-Album Segments

Each album i produces **`clips_per_album` sub-clips**. The audio file is trimmed to match
each sub-clip's duration and plays continuously across an album's sub-clips.

**Label animation (carry-over rule):** the label animates in (fade + 30px ease-out rise
over 0.35s) on an album's **first** sub-clip only, fully settled at `y=60`/`alpha=1` long
before that sub-clip ends, so the 0.3s within-album crossfades over the identical static
label on the continuation sub-clips are invisible. Continuation sub-clips carry the
**static** label (`y=60`, no `alpha`). The exit is handled for free by the 0.5s
album-boundary (or outro) xfade dissolving the whole frame.

**Album 1 audio shift:** every audio `-ss` value for album 1's sub-clips is increased by
`album1_audio_base` (0 unless the intro is silent — see 4b2). Albums 2…N are unaffected.

The animated `y` and `alpha` expressions contain commas, so they **must stay
single-quoted** or the filtergraph parser splits on them.

#### 2-clip mode (`a` = cover, `b` = turntable)

Compute per-album:
```
cover_sec      = min(4, section_sec)
turntable_sec  = section_sec - cover_sec
cover_offset_i = cover_offsets[i]   # from Phase 2 Step 2
```

**Sub-clip A — cover (`segment_<NN>a.mp4`), animated label:**

```bash
ffmpeg -y \
  -ss <cover_offset_i> -t <cover_sec> -i "<cover_video_file>" \
  -ss <album1_audio_base if i==1 else 0> -t <cover_sec> -i "<audio_file>" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,
       pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,
       drawtext=fontfile=<bold_font>:\
         text='<Album Name> (<Year>)':\
         fontcolor=white:fontsize=<label_fs>:\
         x=(w-text_w)/2:y='60+30*pow(1-clip(t/0.35,0,1),2)':\
         alpha='clip(t/0.35,0,1)':\
         box=1:boxcolor=black@0.5:boxborderw=12:\
         shadowcolor=black@0.6:shadowx=2:shadowy=2" \
  -af "apad,atrim=0:<cover_sec>,asetpts=PTS-STARTPTS" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  "<WORK>/segment_<NN>a.mp4"
```

**Sub-clip B — turntable (`segment_<NN>b.mp4`), static label:**
```bash
ffmpeg -y \
  -ss 0 -t <turntable_sec> -i "<turntable_video_file>" \
  -ss <cover_sec + (album1_audio_base if i==1 else 0)> -t <turntable_sec> -i "<audio_file>" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,
       pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,
       drawtext=fontfile=<bold_font>:\
         text='<Album Name> (<Year>)':\
         fontcolor=white:fontsize=<label_fs>:\
         x=(w-text_w)/2:y=60:\
         box=1:boxcolor=black@0.5:boxborderw=12:\
         shadowcolor=black@0.6:shadowx=2:shadowy=2" \
  -af "apad,atrim=0:<turntable_sec>,asetpts=PTS-STARTPTS" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  "<WORK>/segment_<NN>b.mp4"
```

If `turntable_sec == 0` (i.e. `section_sec <= 4`), skip sub-clip B; only sub-clip A exists
for that album. Adjust the segment list and transition chain accordingly.

#### 3-clip mode (`a` = showing, `b` = cover, `c` = turntable)

Compute per-album:
```
showing_sec    = 2
cover_sec      = min(4, max(2, section_sec - 4))
turntable_sec  = section_sec - showing_sec - cover_sec
cover_offset_i = cover_offsets[i]   # from Phase 2 Step 2 — applies to the cover clip only
```

Audio `-ss` ladder (continuous playback across the album's three sub-clips; album 1 adds
`album1_audio_base` to each value): showing `0`, cover `showing_sec`, turntable
`showing_sec + cover_sec`.

**Sub-clip A — showing (`segment_<NN>a.mp4`), animated label** — same `-vf` as the 2-clip
animated cover command (label with entrance animation):
```bash
ffmpeg -y \
  -ss 0 -t <showing_sec> -i "<showing_video_file>" \
  -ss <album1_audio_base if i==1 else 0> -t <showing_sec> -i "<audio_file>" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,
       pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,
       drawtext=fontfile=<bold_font>:\
         text='<Album Name> (<Year>)':\
         fontcolor=white:fontsize=<label_fs>:\
         x=(w-text_w)/2:y='60+30*pow(1-clip(t/0.35,0,1),2)':\
         alpha='clip(t/0.35,0,1)':\
         box=1:boxcolor=black@0.5:boxborderw=12:\
         shadowcolor=black@0.6:shadowx=2:shadowy=2" \
  -af "apad,atrim=0:<showing_sec>,asetpts=PTS-STARTPTS" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  "<WORK>/segment_<NN>a.mp4"
```

**Sub-clip B — cover (`segment_<NN>b.mp4`), static label:** video
`-ss <cover_offset_i> -t <cover_sec>`, audio
`-ss <showing_sec + (album1_audio_base if i==1 else 0)> -t <cover_sec>`, and the static
label `-vf` from the 2-clip sub-clip B command (`y=60`, no `alpha`).

**Sub-clip C — turntable (`segment_<NN>c.mp4`), static label:** video
`-ss 0 -t <turntable_sec>`, audio
`-ss <showing_sec + cover_sec + (album1_audio_base if i==1 else 0)> -t <turntable_sec>`,
same static label `-vf`.

Sub-clips are never skipped in 3-clip mode (the minimum section of 6s guarantees every
sub-clip is ≥ 2s).

Notes (both modes):
- The drawtext `alpha` expression also fades the `box=1` background and shadow, so box and
  text rise and fade in together — this is the intended look.
- This produces `clips_per_album * N` segments total (minus any skipped 2-clip B segments).
- `-ss <cover_offset_i>` on the cover input seeks to the user-specified start offset (fast
  demuxer seek). For sources shorter than their slot after the offset, add
  `tpad=stop_mode=clone` to `-vf` and `apad` to `-af` (already present).
- Escape special characters in album names: apostrophes → `'\''`, colons → `\:`.

### 4b2. Build Intro Segment (optional) / Opening Title

The reel opens with the title `Full <BAND NAME> Discography` (band name ALL CAPS,
`<title_fs>` from the text size rule). How it is rendered depends on whether an intro
clip exists.

#### With intro clip (`INTRO_CLIP` set)

Build `segment_intro.mp4` from the first 3 seconds of the clip, with the title treated
exactly like an album label (top position, box, animated entrance). It holds for the full
3s and exits via the 0.5s xfade into album 1.

In **clip audio mode** (`intro_audio == clip`) there is one input:
```bash
ffmpeg -y \
  -ss 0 -t 3 -i "$INTRO_CLIP" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,
       pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,
       drawtext=fontfile=<bold_font>:\
         text='Full <BAND NAME> Discography':\
         fontcolor=white:fontsize=<title_fs>:\
         x=(w-text_w)/2:y='60+30*pow(1-clip(t/0.35,0,1),2)':\
         alpha='clip(t/0.35,0,1)':\
         box=1:boxcolor=black@0.5:boxborderw=12:\
         shadowcolor=black@0.6:shadowx=2:shadowy=2" \
  -af "apad,atrim=0:3,asetpts=PTS-STARTPTS" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  "<WORK>/segment_intro.mp4"
```

In **music mode** (`intro_audio == music` — the clip has no audio stream), add album 1's
audio as a second input right after the clip input — the rest of the command is identical
(ffmpeg picks the second input's audio since the clip has none):
```bash
  -ss 0 -t 3 -i "$INTRO_CLIP" \
  -ss 0 -t 3 -i "<album1_audio_file>" \
```
Album 1's sub-clips then continue its sample from `t=3` via `album1_audio_base = 3`
(see 4b), so the music plays continuously from the intro into album 1's section.

If the intro clip is shorter than 3s, append `tpad=stop_mode=clone` to the `-vf` chain
(before `drawtext`) so the last frame holds; `apad` covers the audio.

#### Without intro clip — opening title on album 1

No extra segment. Instead, append a **second** drawtext to album 1's **first** sub-clip
command in 4b, after the album label filter: the title sits mid-frame, no box, animates in
like the labels, holds, then fades out over 0.3s ending at `F1` — gone before the first
crossfade. The album label at `y=60` runs simultaneously.

```
F1 = min(2.0, D_first - 0.3)     # fade-out end
F0 = F1 - 0.3                    # fade-out start
D_first = cover_sec (2-clip) or showing_sec = 2 (3-clip → F1=1.7, F0=1.4)
```

```
drawtext=fontfile=<bold_font>:\
  text='Full <BAND NAME> Discography':\
  fontcolor=white:fontsize=<title_fs>:\
  x=(w-text_w)/2:y='h*0.40+30*pow(1-clip(t/0.35,0,1),2)':\
  alpha='if(lt(t,<F0>),clip(t/0.35,0,1),clip((<F1>-t)/0.3,0,1))':\
  shadowcolor=black@0.7:shadowx=4:shadowy=4
```

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

**Music-mode audio seek:** `<last_ss> = section_sec`, except when `N == 1` and
`intro_audio == music` — then album 1 is also the last album and its sample is shifted by
the intro, so `<last_ss> = intro_sec + section_sec`.

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
         fontcolor=white:fontsize=64:\
         x=(w-text_w)/2:y='h*0.42+30*pow(1-clip((t-0.6)/0.35,0,1),2)':\
         alpha='clip((t-0.6)/0.35,0,1)':\
         shadowcolor=black@0.7:shadowx=4:shadowy=4,
       drawtext=fontfile=<regular_font>:\
         text='Let me know in the comments.':\
         fontcolor=white@0.9:fontsize=48:\
         x=(w-text_w)/2:y='h*0.42+120+30*pow(1-clip((t-0.72)/0.35,0,1),2)':\
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
  -ss <last_ss> -t 4 -i "<last_audio>" \
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
<last_video> = the last album's turntable file
               (3-clip: 3_turntable; 2-clip: 2_turntable,
                or its 1_cover file when turntable_sec == 0)
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
  -ss <last_ss> -t 4 -i "<last_audio>" \
  -vf "drawbox=x=0:y=0:w=iw:h=ih:color=black@0.45:t=fill,
       drawtext=fontfile=<bold_font>:\
         text='What is your favorite album?':\
         fontcolor=white:fontsize=64:\
         x=(w-text_w)/2:y='h*0.42+30*pow(1-clip((t-0.6)/0.35,0,1),2)':\
         alpha='clip((t-0.6)/0.35,0,1)':\
         shadowcolor=black@0.7:shadowx=4:shadowy=4,
       drawtext=fontfile=<regular_font>:\
         text='Let me know in the comments.':\
         fontcolor=white@0.9:fontsize=48:\
         x=(w-text_w)/2:y='h*0.42+120+30*pow(1-clip((t-0.72)/0.35,0,1),2)':\
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
- `-ss <last_ss>` on a music-mode audio input continues the last album's music exactly
  where its final sub-clip stopped; `apad` fills with silence if the sample runs short.
- The text delays (0.6s / 0.72s) let the incoming 0.5s crossfade settle before the lines
  animate in (fade + slide-up, staggered like the album labels).
- **No fade-out on the text** — the card holds to the last frame: it is the comment prompt
  and the loop point of the Short.

### 4d. Concatenate Segments with Crossfades

Use chained `xfade` + `acrossfade` filter_complex for smooth transitions across the whole
chain:

**Segment sequence:** `[intro?, 01-first…01-last, 02-first…02-last, …, NN-last, outro]`
— `(1 if intro) + clips_per_album * N + 1` inputs (minus any skipped 2-clip B segments).

**Crossfade durations — set by the segment being transitioned INTO:**
- Into any album's **first** sub-clip, or into the **outro**: `x = 0.5` (boundary)
- Into a **continuation** sub-clip (turntable, and cover in 3-clip mode): `x = 0.3`
- The intro→album-1 transition is therefore `0.5s`. There is no incoming transition into
  the chain head (intro when present, otherwise album 1's first sub-clip).

**Segment durations:** `d = 3` (intro, if present); per album, `cover_sec`/`turntable_sec`
(2-clip) or `showing_sec`/`cover_sec`/`turntable_sec` (3-clip); `d[last] = outro_sec = 4`.

**Offset formula** (the offsets must be strictly increasing and in output-timeline seconds):
```
O[0] = d[0] - x[0]
O[i] = O[i-1] + (d[i] - x[i-1]) - x[i]    for i >= 1
     = sum(d[0..i]) - sum(x[0..i])
```

Compute all offsets before writing the filter_complex. Round to 2 decimal places.

Build the filter_complex dynamically. Worked example — intro + 3-clip mode, N=2,
illustrative `section_sec=10` (split 2/4/4); 8 segments, 7 transitions:
```
# segments:    intro(3), 01a(2), 01b(4), 01c(4), 02a(2), 02b(4), 02c(4), outro(4)
# transitions: 0.5,      0.3,    0.3,    0.5,    0.3,    0.3,    0.5
# offsets:     O = 2.5, 4.2, 7.9, 11.4, 13.1, 16.8, 20.3
# assembled duration = sum(d) - sum(x) = 27 - 2.7 = 24.3
-filter_complex "
  [0:v][1:v]xfade=transition=fade:duration=0.5:offset=2.5[v01];
  [v01][2:v]xfade=transition=fade:duration=0.3:offset=4.2[v02];
  [v02][3:v]xfade=transition=fade:duration=0.3:offset=7.9[v03];
  [v03][4:v]xfade=transition=fade:duration=0.5:offset=11.4[v04];
  [v04][5:v]xfade=transition=fade:duration=0.3:offset=13.1[v05];
  [v05][6:v]xfade=transition=fade:duration=0.3:offset=16.8[v06];
  [v06][7:v]xfade=transition=fade:duration=0.5:offset=20.3[vout];
  [0:a][1:a]acrossfade=d=0.5:c1=tri:c2=tri[a01];
  [a01][2:a]acrossfade=d=0.3:c1=tri:c2=tri[a02];
  [a02][3:a]acrossfade=d=0.3:c1=tri:c2=tri[a03];
  [a03][4:a]acrossfade=d=0.5:c1=tri:c2=tri[a04];
  [a04][5:a]acrossfade=d=0.3:c1=tri:c2=tri[a05];
  [a05][6:a]acrossfade=d=0.3:c1=tri:c2=tri[a06];
  [a06][7:a]acrossfade=d=0.5:c1=tri:c2=tri[aout]
" -map "[vout]" -map "[aout]"
```

(A 2-clip reel with no intro reduces to the previous alternating `0.3 / 0.5 / 0.3 / …`
chain — the destination rule produces it automatically.)

**Special cases:**
- If `turntable_sec == 0` for some albums (2-clip mode only), those albums have only one
  segment (sub-clip A). Adjust the segment list — the destination rule still applies
  (the transition into the next album's first sub-clip stays 0.5s).
- N=1: the chain is `[intro?, 01a, 01b, outro]` (2-clip; `[intro?, 01a, outro]` when
  `turntable_sec == 0`) or `[intro?, 01a, 01b, 01c, outro]` (3-clip). The outro means
  there are always at least 2 chain elements — the single-segment copy case never occurs.

Full assemble command:
```bash
ffmpeg -y \
  -i "<WORK>/segment_intro.mp4" \      # only when an intro clip is used
  -i "<WORK>/segment_01a.mp4" \
  -i "<WORK>/segment_01b.mp4" \
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

If `total_sec <= 20` (note `total_sec` includes `intro_sec`), skip the subscribe overlay
(the animation would not appear within the video duration). Mention this to the user.

### 4g. Generate Metadata

Write `<WORK_DIR>/<BAND_SLUG>_Discography_metadata.md` with English and Ukrainian sections.

**BAND NAME in ALL CAPS** everywhere in titles and descriptions.
**No em dashes (—) anywhere.** Use plain hyphens `-` as separators.

When `include_eps`: EN title becomes
`BAND NAME - Full Discography: Albums + EPs (<YEAR_FIRST>-<YEAR_LAST>) #vinyl`, the
description line becomes "This reel covers their complete studio discography - N_albums
albums and N_eps EPs from <YEAR_FIRST> to <YEAR_LAST>.", each EP in the list is annotated
`Album Name (YEAR) [EP]`, and the UA title becomes
`BAND NAME - Повна дискографія: альбоми та EP (<YEAR_FIRST>-<YEAR_LAST>) #vinyl` with the
description line "Цей ролик охоплює повну студійну дискографію - N_albums альбомів та
N_eps EP від <YEAR_FIRST> до <YEAR_LAST>." Albums-only wording (below) is unchanged.

```markdown
# BAND NAME - Full Discography (<YEAR_FIRST>-<YEAR_LAST>)

---

## English

**Title:** BAND NAME - Full Discography (<YEAR_FIRST>-<YEAR_LAST>) #vinyl

**Description:**
BAND NAME is a <genre> band from <country>, active since <year>.
This reel covers their complete studio discography - N albums from <YEAR_FIRST> to <YEAR_LAST>.

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
BAND NAME - <genre> гурт з <country>, заснований у <year>.
Цей ролик охоплює повну студійну дискографію - N альбомів від <YEAR_FIRST> до <YEAR_LAST>.

Альбоми:
1. Album Name (YEAR)
2. Album Name (YEAR)
...

Підписуйтесь - щотижня метал-вінілова колекція.

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

When an intro clip was used, add: "The reel opens with your 3 s intro clip under the
'Full <BAND NAME> Discography' title."

---

## Error Handling

- **Source clip shorter than its slot:** Add `tpad=stop_mode=clone` to freeze the last
  frame for the remaining duration. Add `apad` for audio (already in the segment command).
  This also covers an intro clip shorter than 3s.
- **Font not found:** Try `fc-list` to find any available bold TTF. If none, omit
  `fontfile=` — ffmpeg will use its default font (text will still render, just less styled).
- **Crossfade offset calculation:** If the filter_complex fails with offset errors,
  double-check that the O_i values are strictly increasing and rounded to 2 decimal places.
- **assembled.mp4 duration check:** After assembly, verify duration with ffprobe. When no
  sub-clips are skipped, it should be approximately
  `intro_sec + content_sec + 4 - (0.5 * (N + I) + 0.3 * N * (clips_per_album - 1))`
  where `I = 1` if an intro clip is used, else `0` — the shortfall vs `total_sec` is the
  crossfade overlap. This is expected.
- **outro_frame.png empty or missing:** Retry the extraction with `-sseof -0.5` on the raw
  source (replacing the `-ss <last_t>` seek).
- **Multiple files in `intro/` or `outro/`:** ask the user which one to use (Phase 3
  should have caught this).
- **`intro/` contents contradict the Phase 2 answer:** (clip present after "no", or empty
  after "yes") — Phase 3 reconciles: recompute `intro_sec`/`section_sec`, re-run the split
  checks, show the new numbers, and confirm before continuing.
- **Custom outro clip shorter than 4s:** `tpad=stop_mode=clone` in `-vf` holds the last
  frame; `apad` covers the audio.
- **Last album audio shorter than `section_sec + 4`:** `apad` fills the outro tail with
  silence — acceptable for an end card. The Phase 3 check should already have warned the user.
- **Album 1 audio shorter than `intro_sec + section_sec` (silent-intro mode):** `apad`
  fills the tail of its section with silence. The Phase 3 check should already have warned
  the user.
- **N=1 (band with only 1 studio album):** The chain is `[intro?, 01a, 01b, outro]` — or
  `[intro?, 01a, outro]` when turntable_sec == 0, or `[intro?, 01a, 01b, 01c, outro]` in
  3-clip mode. Remember the outro music seek becomes `intro_sec + section_sec` when the
  intro is silent (4c). Subscribe overlay still applied if total_sec > 20.
- **Subscribe asset not found:** If `<skill-path>/assets/subscribe_btn_animation_small.mp4`
  is missing, skip the `_yt.mp4` export and tell the user — the asset should be bundled
  with the plugin.
