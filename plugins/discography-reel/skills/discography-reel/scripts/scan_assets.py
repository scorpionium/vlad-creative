#!/usr/bin/env python3
"""
Validate a discography working directory before assembly.

Expects subdirectories matching NN_* pattern, each with:
  video/ — exactly 1 video file
  audio/ — exactly 1 audio file

Usage: python3 scan_assets.py <working-folder>

Exit code 0 = all valid, 1 = errors found.
Outputs JSON to stdout.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".m4v"}
AUDIO_EXTENSIONS = {".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg"}

ALBUM_DIR_PATTERN = re.compile(r"^\d{2}_")


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
    if len(sys.argv) < 2:
        print("Usage: python3 scan_assets.py <working-folder>", file=sys.stderr)
        sys.exit(1)

    working_folder = Path(sys.argv[1])

    if not working_folder.exists():
        print(f"Error: {working_folder} does not exist", file=sys.stderr)
        sys.exit(1)

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

        album_entry = {
            "album_dir": album_name,
            "path": str(album_dir),
            "video_file": None,
            "audio_file": None,
            "video_duration": None,
            "audio_duration": None,
            "valid": True
        }

        # Check video/ folder
        if not video_folder.exists():
            errors.append(f"{album_name}: missing video/ subfolder")
            album_entry["valid"] = False
        else:
            video_files = find_files_by_extension(video_folder, VIDEO_EXTENSIONS)
            if len(video_files) == 0:
                errors.append(f"{album_name}/video/: no video file found (accepted: {', '.join(sorted(VIDEO_EXTENSIONS))})")
                album_entry["valid"] = False
            elif len(video_files) > 1:
                names = ", ".join(f.name for f in video_files)
                errors.append(f"{album_name}/video/: expected 1 video file, found {len(video_files)}: {names}")
                album_entry["valid"] = False
            else:
                vf = video_files[0]
                duration = get_duration(vf)
                if duration is None:
                    errors.append(f"{album_name}/video/{vf.name}: ffprobe could not read file")
                    album_entry["valid"] = False
                else:
                    album_entry["video_file"] = str(vf)
                    album_entry["video_duration"] = round(duration, 2)

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
        "total_albums": len(album_dirs),
        "valid_albums": len(valid_albums),
        "errors": errors,
        "albums": albums
    }

    print(json.dumps(output, indent=2))

    if errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
