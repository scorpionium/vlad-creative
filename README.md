# vlad-creative

A Claude Code plugin marketplace with creative and media production skills.

## Install

```
/plugin marketplace add scorpionium/vlad-creative-plugin
```

Then install individual plugins:

```
/plugin install vinyl-reel@vlad-creative
```

## Plugins

| Plugin | Trigger | Description |
|--------|---------|-------------|
| [`vinyl-reel`](plugins/vinyl-reel) | `/vinyl-reel` or describe a vinyl unboxing task | Produces 9:16 YouTube Shorts and Instagram Reels from raw footage, with bilingual voiceover and background music |

## Adding a Plugin

1. Create `plugins/<name>/` with a `.claude-plugin/plugin.json` and your `skills/` or `commands/`
2. Add an entry to `.claude-plugin/marketplace.json`
3. Bump the marketplace version if applicable

## License

MIT
