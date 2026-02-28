---
description: Create a discography reel for a band's complete studio albums
allowed-tools: Read, Write, Edit, Bash, WebSearch, WebFetch, TodoWrite
argument-hint: [band name]
---

Invoke the discography-reel skill to create a vertical short-form discography reel.

Band name: $ARGUMENTS

If no band name was provided, ask the user which band they want to make a discography reel for, then proceed.

Follow the full 4-phase workflow defined in the discography-reel skill:
1. Research the band's studio discography (exclude EPs, singles, compilations, live albums, demos, box sets)
2. Create per-album asset folders and pause — wait for user to populate them
3. Scan and validate all asset folders
4. Assemble segments, concatenate, and export both MP4 outputs plus metadata

Use the skill's bundled scripts and references.
