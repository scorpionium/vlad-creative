---
description: Create a vinyl unboxing reel from a folder of clips
allowed-tools: Read, Write, Edit, Bash, WebSearch, WebFetch, TodoWrite
argument-hint: [path-to-album-folder]
---

Invoke the vinyl-reel skill to create a vertical short-form unboxing reel.

The working folder is: $ARGUMENTS

If no folder path was provided, ask the user to select a folder using the request_cowork_directory tool, then proceed.

Follow the full 6-phase workflow defined in the vinyl-reel skill:
1. Scan & Catalog clips
2. Research the album
3. Write voiceover script (pause for approval)
4. Generate voiceover audio
5. Arrange, mix, and edit video
6. Export YouTube Shorts version + Instagram clean version, and generate YouTube metadata

Use the skill's bundled scripts and references. The VOICEOVER_API_KEY must be set — if it isn't, ask the user to provide it before continuing.
