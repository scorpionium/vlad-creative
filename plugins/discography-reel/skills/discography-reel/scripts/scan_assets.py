#!/usr/bin/env python3
"""
Validate a discography working directory before assembly.

Expects subdirectories matching NN_* pattern, each with:
  video/ — exactly 2 or 3 video files, sorted alphabetically:
           2-clip mode: 1_cover.*, 2_turntable.*
           3-clip mode: 1_showing.*, 2_cover.*, 3_turntable.*
  audio/ — exactly 1 audio file

Usage: python3 scan_assets.py <working-folder> [--clips 2|3]

Exit code 0 = all valid, 1 = errors found.
Outputs JSON to stdout.
"""

import argparse
import json
import re
import subprocess
from pathlib import Path


VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".m4v"}
AUDIO_EXTENSIONS = {".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg"}

ALBUM_DIR_PATTERN = re.compile(r"^\d{2}_")

# Sorted-alphabetical role assignment per clip mode
ROLES = {
    2: ["cover", "turntable"],
    3: ["showing", "cover", "turntable"],
}
EXPECTED_HINT = {
    2: "1_cover.* and 2_turntable.*",
    3: "1_showing.*, 2_cover.* and 3_turntable.*",
}


def probe_clip(filepath):
    """Get file metadata using ffprobe. Returns parsed JSON or None on error."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration:stream=width,height,codec_name,codec_type",
        "-of", "json",
        str(filepath)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def get_duration(filepath):
    """Return float duration in seconds, or None if unreadable."""
    info = probe_clip(filepath)
    if info is None:
        return None
    try:
        return float(info["format"]["duration"])
    except (KeyError, ValueError, TypeError):
        return None


def find_files_by_extension(folder, extensions):
    """Return list of files in folder matching the given extensions (case-insensitive)."""
    if not folder.exists():
        return []
    return [
        f for f in sorted(folder.iterdir())
        if f.is_file() and f.suffix.lower() in extensions
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Validate a discography working directory before assembly.")
    parser.add_argument("working_folder", type=Path)
    parser.add_argument("--clips", type=int, choices=[2, 3], default=2,
                        help="expected video clips per album (default: 2)")
    args = parser.parse_args()

    working_folder = args.working_folder
    clips = args.clips
    roles = ROLES[clips]

    if not working_folder.exists():
        parser.error(f"{working_folder} does not exist")

    # Discover album subdirectories matching NN_* pattern, sorted alphabetically
    album_dirs = sorted(
        [d for d in working_folder.iterdir()
         if d.is_dir() and ALBUM_DIR_PATTERN.match(d.name)],
        key=lambda d: d.name
    )

    errors = []
    albums = []

    for album_dir in album_dirs:
        album_name = album_dir.name
        video_folder = album_dir / "video"
        audio_folder = album_dir / "audio"

        album_entry = {"album_dir": album_name, "path": str(album_dir)}
        for role in roles:
            album_entry[f"{role}_video"] = None
        album_entry["audio_file"] = None
        for role in roles:
            album_entry[f"{role}_video_duration"] = None
        album_entry["audio_duration"] = None
        album_entry["valid"] = True

        # Check video/ folder — expects exactly `clips` files (sorted alphabetically → roles)
        if not video_folder.exists():
            errors.append(f"{album_name}: missing video/ subfolder")
            album_entry["valid"] = False
        else:
            video_files = find_files_by_extension(video_folder, VIDEO_EXTENSIONS)
            if len(video_files) != clips:
                names = ", ".join(f.name for f in video_files) or "none"
                errors.append(
                    f"{album_name}/video/: expected {clips} video files "
                    f"({EXPECTED_HINT[clips]}), found {len(video_files)}: {names}")
                album_entry["valid"] = False
            else:
                for role, vf in zip(roles, video_files):
                    duration = get_duration(vf)
                    if duration is None:
                        errors.append(f"{album_name}/video/{vf.name}: ffprobe could not read file")
                        album_entry["valid"] = False
                    else:
                        album_entry[f"{role}_video"] = str(vf)
                        album_entry[f"{role}_video_duration"] = round(duration, 2)

        # Check audio/ folder
        if not audio_folder.exists():
            errors.append(f"{album_name}: missing audio/ subfolder")
            album_entry["valid"] = False
        else:
            audio_files = find_files_by_extension(audio_folder, AUDIO_EXTENSIONS)
            if len(audio_files) == 0:
                errors.append(f"{album_name}/audio/: no audio file found (accepted: {', '.join(sorted(AUDIO_EXTENSIONS))})")
                album_entry["valid"] = False
            elif len(audio_files) > 1:
                names = ", ".join(f.name for f in audio_files)
                errors.append(f"{album_name}/audio/: expected 1 audio file, found {len(audio_files)}: {names}")
                album_entry["valid"] = False
            else:
                af = audio_files[0]
                duration = get_duration(af)
                if duration is None:
                    errors.append(f"{album_name}/audio/{af.name}: ffprobe could not read file")
                    album_entry["valid"] = False
                else:
                    album_entry["audio_file"] = str(af)
                    album_entry["audio_duration"] = round(duration, 2)

        albums.append(album_entry)

    valid_albums = [a for a in albums if a["valid"]]

    output = {
        "working_folder": str(working_folder),
        "clips_per_album": clips,
        "total_albums": len(album_dirs),
        "valid_albums": len(valid_albums),
        "errors": errors,
        "albums": albums
    }

    print(json.dumps(output, indent=2))

    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
