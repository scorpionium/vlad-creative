---
description: Create a discography reel for a band's studio albums (optionally including EPs)
allowed-tools: Read, Write, Edit, Bash, WebSearch, WebFetch, TodoWrite
argument-hint: [band name]
---

Invoke the discography-reel skill to create a vertical short-form discography reel.

Band name: $ARGUMENTS

If no band name was provided, ask the user which band they want to make a discography reel for, then proceed.

Follow the full 4-phase workflow defined in the discography-reel skill:
1. Research the band's discography - asks whether to cover studio albums only or studio albums + EPs (always excluding singles, compilations, live albums, demos, box sets)
2. Create asset folders and pause - asks clips-per-album (2 or 3) and whether a 3s intro clip will be added, creates per-album folders plus `intro/` and `outro/`, then waits for the user to populate them
3. Scan and validate all asset folders
4. Assemble segments (opening title, intro if provided, animated album labels, outro end card), concatenate, and export both MP4 outputs plus metadata

Use the skill's bundled scripts and references.
