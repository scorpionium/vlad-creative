# FFmpeg Patterns for Discography Reel Production

Proven filter chains for assembling multi-album discography reels. All outputs are 1080x1920
9:16 portrait, H.264 CRF-18, 30fps, AAC 192kbps.

## Table of Contents
1. [Scale & Pad to Portrait](#scale--pad-to-portrait)
2. [Text Overlay — Top of Frame (Animated)](#text-overlay--top-of-frame-animated)
3. [Segment Build — Two Sub-Clips per Album](#segment-build--two-sub-clips-per-album)
4. [Short Clip Padding](#short-clip-padding)
5. [Outro End Card (Freeze-Frame + CTA)](#outro-end-card-freeze-frame--cta)
6. [Crossfade — Chained xfade + acrossfade](#crossfade--chained-xfade--acrossfade)
7. [Subscribe Overlay (Chromakey at t=20s)](#subscribe-overlay-chromakey-at-t20s)
8. [Standard Encoding Settings](#standard-encoding-settings)

---

## Scale & Pad to Portrait

Phone clips and footage can be any orientation. This filter outputs a clean 1080x1920 frame
regardless of source aspect ratio, with black bars (letterbox/pillarbox) as needed:

```bash
-vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black"
```

- `force_original_aspect_ratio=decrease` — scales down to fit within 1080x1920
- `pad` — centers the scaled frame, fills remainder with black

---

## Text Overlay — Top of Frame (Animated)

Album name and year displayed at the top of each section. Semi-transparent black background
box provides legibility over any footage. The label animates in with a fade + slide-up.

Font detection (run before building segments):
```bash
fc-list | grep -i "LiberationSans-Bold"      # Preferred (labels, outro question)
fc-list | grep -i "DejaVuSans-Bold"          # Fallback
fc-list | grep -i "LiberationSans-Regular"   # Preferred (outro CTA line)
fc-list | grep -i "DejaVuSans"               # Fallback (else reuse bold)
```

**Animated entrance (cover sub-clip A)** — fades in over 0.35s while rising ~30px into
place with an ease-out quad. The `y`/`alpha` expressions contain commas and **must stay
single-quoted** or the filtergraph parser splits on them:
```
drawtext=fontfile=<bold_font>:\
  text='Album Name (Year)':\
  fontcolor=white:fontsize=40:\
  x=(w-text_w)/2:y='60+30*pow(1-clip(t/0.35,0,1),2)':\
  alpha='clip(t/0.35,0,1)':\
  box=1:boxcolor=black@0.5:boxborderw=12:\
  shadowcolor=black@0.6:shadowx=2:shadowy=2
```

**Static continuation (turntable sub-clip B)** — same block with `y=60` and no `alpha`.

Carry-over rule (overlays are burned per segment and `t` restarts at 0 in each):
- Sub-clip A = entrance: fade-in + rise, settled long before the segment ends, so the
  0.3s A→B crossfade over B's identical static label is invisible.
- Sub-clip B = continuation: fully static.
- Exit: no explicit fade-out — the 0.5s album-boundary (or outro) xfade dissolves the
  whole frame, taking the old label out as the next one animates in.
- The `alpha` expression also fades the box and shadow with the text (intended).

Key parameters:
- `y=60` — resting position near the top with breathing room from the edge
- `box=1:boxcolor=black@0.5:boxborderw=12` — semi-transparent background strip (12px padding)
- `fontsize=40` — readable at phone screen size
- `shadowcolor=black@0.6` — additional depth for legibility

Escaping special characters in album names:
```
text='It'\''s a Long Way'     # Escape apostrophes with '\''
text='Title\: Subtitle'       # Escape colons with \:
text='Кров у наших криницях'  # Unicode (Cyrillic etc.) works directly
```

---

## Segment Build — Two Sub-Clips per Album

Each album produces **two segments**: sub-clip A (cover, `cover_sec = min(4, section_sec)`,
starts at the user-supplied `cover_offset`) and sub-clip B (turntable,
`turntable_sec = section_sec - cover_sec`, skipped when 0). The album's audio file spans
both: A takes `[0, cover_sec)`, B continues from `-ss <cover_sec>`.

**Sub-clip A — cover (animated label):**
```bash
ffmpeg -y \
  -ss <cover_offset> -t <cover_sec> -i "<cover_video_file>" \
  -ss 0              -t <cover_sec> -i "<audio_file>" \
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
  ".work/segment_<NN>a.mp4"
```

**Sub-clip B — turntable (static label):** same structure with
`-ss 0 -t <turntable_sec>` on the video, `-ss <cover_sec> -t <turntable_sec>` on the audio,
the static drawtext (`y=60`, no `alpha`), and output `.work/segment_<NN>b.mp4`.

Notes:
- `-ss ... -t ...` before each `-i` = fast demuxer-level seek (no full decode)
- `-af "apad,atrim=0:<dur>,asetpts=PTS-STARTPTS"` — pads short audio to fill the sub-clip,
  then trims to exact length and resets timestamps
- If the video source is shorter than the sub-clip duration, add `tpad` to the `-vf` chain
  (see [Short Clip Padding](#short-clip-padding))

---

## Short Clip Padding

If a source clip is shorter than `section_sec`, freeze the last frame to fill the gap.

Add `tpad` at the end of the `-vf` filter chain:
```
tpad=stop_mode=clone:stop_duration=<extra_sec>
```

Where `extra_sec = section_sec - source_duration` (use scan output to compute this).

Full `-vf` with padding:
```bash
-vf "scale=1080:1920:force_original_aspect_ratio=decrease,
     pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,
     tpad=stop_mode=clone:stop_duration=<extra_sec>,
     drawtext=..."
```

Audio padding is already handled by `apad` in the `-af` chain.

---

## Outro End Card (Freeze-Frame + CTA)

A 4-second closing card, darkened 45%, with two animated text lines inviting comments. The
background is either a user-provided **custom outro clip** (from `<WORK_DIR>/outro/`) or a
**freeze-frame** of the final album's footage; the darken + text treatment is identical.

**Custom clip variant** — one command, first 4s of the clip, scale/pad + the same
darken/text filters as Step 2 below in place of the `-loop 1` image input:
```bash
ffmpeg -y \
  -ss 0 -t 4 -i "<outro_clip>" \
  <if the clip has NO audio stream, add:  -ss <section_sec> -t 4 -i "<last_album_audio>"> \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,
       pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,
       <darkbox + two drawtext lines from Step 2>" \
  -af "apad,atrim=0:4,asetpts=PTS-STARTPTS" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k \
  ".work/segment_outro.mp4"
```
Audio auto-detect: probe the clip with
`ffprobe -v quiet -select_streams a -show_entries stream=index -of csv=p=0` — any output
means the clip's own audio is used (clip mode; final export fade drops to 1s so a spoken
ask isn't faded down); no output means the last album's music continues (music mode, 3s
fade). Clip shorter than 4s: add `tpad=stop_mode=clone` before the darkbox.

**Freeze-frame variant** — built in two steps.

**Step 1 — extract the freeze-frame** from the **raw source video** (`2_turntable` file, or
`1_cover` when the turntable sub-clip was skipped) — not from the encoded segment, which has
the album label burned in. `<last_t>` = the last displayed source timestamp
(`turntable_sec - 0.1`, or `cover_offset + cover_sec - 0.1` when the turntable was skipped):
```bash
ffmpeg -y -ss <last_t> -i "<last_video>" -frames:v 1 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,
       pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -update 1 ".work/outro_frame.png"
# if no frame is produced (source shorter than <last_t>), retry with:
#   ffmpeg -y -sseof -0.5 -i "<last_video>" ... (same -vf)
```

**Step 2 — build the outro segment** (frame is already scale/padded to 1080x1920):
```bash
ffmpeg -y \
  -loop 1 -framerate 30 -t 4 -i ".work/outro_frame.png" \
  -ss <section_sec> -t 4 -i "<last_album_audio>" \
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
  ".work/segment_outro.mp4"
```

Design rationale:
- `drawbox=...black@0.45:t=fill` — darkens the frozen frame so the text pops
- `-ss <section_sec>` on the audio — the last album's music continues seamlessly into the
  card; `apad` fills with silence if the sample runs short
- Text delays 0.6s / 0.72s — the incoming 0.5s crossfade settles before the lines animate
  in (fade + slide-up, staggered like the album labels)
- **No fade-out on the text** — the card holds to the last frame; it is the comment prompt
  and the loop point of the Short

---

## Crossfade — Chained xfade + acrossfade

Fade transitions between all chain segments, applied in a single `filter_complex` pass.

**Chain (0-indexed):** `[01a, 01b, 02a, 02b, …, NNa, NNb, outro]` — `2N + 1` inputs when
every album has both sub-clips.

**Transition durations:**
- Within-album (A→B): `x = 0.3`
- Album-boundary (B→A of next album): `x = 0.5`
- Into the outro (final transition): `x = 0.5`

**Segment durations:** `d = cover_sec` for A segments, `turntable_sec` for B segments,
`4` for the outro.

### Offset Formula

With mixed durations, use the general running-sum formula (offsets are in output-timeline
seconds and must be strictly increasing; round to 2 decimals):
```
O[i] = sum(d[0..i]) - sum(x[0..i])
```

### Worked Example — 2 Albums, section_sec=11 (cover_sec=4, turntable_sec=7)

```
segments:    01a(4), 01b(7), 02a(4), 02b(7), outro(4)
transitions: 0.3,    0.5,    0.3,    0.5
O_0 = 4 - 0.3                          = 3.7
O_1 = (4+7) - (0.3+0.5)                = 10.2
O_2 = (4+7+4) - (0.3+0.5+0.3)          = 13.9
O_3 = (4+7+4+7) - (0.3+0.5+0.3+0.5)    = 20.4
```

```bash
ffmpeg -y \
  -i ".work/segment_01a.mp4" \
  -i ".work/segment_01b.mp4" \
  -i ".work/segment_02a.mp4" \
  -i ".work/segment_02b.mp4" \
  -i ".work/segment_outro.mp4" \
  -filter_complex "
    [0:v][1:v]xfade=transition=fade:duration=0.3:offset=3.7[v01];
    [v01][2:v]xfade=transition=fade:duration=0.5:offset=10.2[v02];
    [v02][3:v]xfade=transition=fade:duration=0.3:offset=13.9[v03];
    [v03][4:v]xfade=transition=fade:duration=0.5:offset=20.4[vout];
    [0:a][1:a]acrossfade=d=0.3:c1=tri:c2=tri[a01];
    [a01][2:a]acrossfade=d=0.5:c1=tri:c2=tri[a02];
    [a02][3:a]acrossfade=d=0.3:c1=tri:c2=tri[a03];
    [a03][4:a]acrossfade=d=0.5:c1=tri:c2=tri[aout]
  " \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k \
  ".work/assembled.mp4"
```

**Special case N=1:** the chain is `[01a, 01b, outro]` (transitions `0.3, 0.5`), or
`[01a, outro]` (single `0.5`) when turntable_sec == 0. The outro guarantees at least two
chain elements, so a no-crossfade copy case never occurs.

**Note on assembled duration:** each crossfade overlaps adjacent segments, so the output is
`sum(d) - sum(x)` seconds — with all sub-clips present, approximately
`content_sec + 4 - (0.3 * N + 0.5 * N)`. This is expected and correct. Derive any
downstream timings (e.g. the audio fade-out start) from the **ffprobe'd duration of
assembled.mp4**, never from `total_sec`.

---

## Subscribe Overlay (Chromakey at t=20s)

Overlay the green-screen subscribe animation starting at exactly the 20-second mark.
The animation plays once through and stops naturally (no looping).

```bash
# Asset is bundled with the plugin
SUBSCRIBE="<skill-path>/assets/subscribe_btn_animation_small.mp4"

# Input is the CLEAN EXPORT (already carries the audio fade-out), not assembled.mp4
ffmpeg -y \
  -i "<BAND_SLUG>_Discography_<YEAR_FIRST>-<YEAR_LAST>.mp4" \
  -itsoffset 20 -i "$SUBSCRIBE" \
  -filter_complex " \
    [1:v]chromakey=0x00FF00:0.3:0.1,scale=1080:-1[sub]; \
    [0:v][sub]overlay=(W-w)/2:(H-h)/2:eof_action=pass[out]" \
  -map "[out]" -map "0:a" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30 \
  -c:a copy \
  "<BAND_SLUG>_Discography_<YEAR_FIRST>-<YEAR_LAST>_yt.mp4"
```

Key settings:
- `-itsoffset 20` — delays the subscribe animation input by 20 seconds relative to the main video
- `chromakey=0x00FF00:0.3:0.1` — removes green background (similarity=0.3, blend=0.1)
- `scale=1080:-1` — full frame width, preserves aspect ratio
- `overlay=(W-w)/2:(H-h)/2:eof_action=pass` — centered; `eof_action=pass` keeps the main
  video playing normally after the animation ends (prevents last-frame freeze)
- `-c:a copy` — audio stream (with fade) passed through without re-encode

If `total_sec <= 20`, skip this export — the animation would appear after the video ends.

---

## Standard Encoding Settings

All video outputs:
```
-c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r 30
```

Audio:
```
-c:a aac -b:a 192k
```

Resolution: `1080x1920` (9:16 portrait)
