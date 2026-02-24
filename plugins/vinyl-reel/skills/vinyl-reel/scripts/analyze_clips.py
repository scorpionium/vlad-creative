#!/usr/bin/env python3
"""
Scan a working folder's video/ subfolder and catalog all clips.
Outputs JSON with duration, dimensions, and extracts thumbnails.

Usage: python3 analyze_clips.py <working-folder>
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def probe_clip(filepath):
    """Get clip metadata using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration:stream=width,height,codec_name,codec_type",
        "-of", "json",
        str(filepath)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)


def extract_thumbnail(filepath, output_path, timestamp=1.0):
    """Extract a single frame as thumbnail."""
    cmd = [
        "ffmpeg", "-y", "-ss", str(timestamp),
        "-i", str(filepath),
        "-frames:v", "1", "-q:v", "3",
        str(output_path)
    ]
    subprocess.run(cmd, capture_output=True)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_clips.py <working-folder>", file=sys.stderr)
        sys.exit(1)

    working_folder = Path(sys.argv[1])
    video_folder = working_folder / "video"

    if not video_folder.exists():
        print(f"Error: {video_folder} does not exist", file=sys.stderr)
        sys.exit(1)

    # Create thumbnails directory
    thumb_dir = working_folder / ".thumbnails"
    thumb_dir.mkdir(exist_ok=True)

    # Find all video files
    video_extensions = {".mp4", ".mov", ".avi", ".mkv", ".m4v", ".MP4", ".MOV"}
    clips = sorted([
        f for f in video_folder.iterdir()
        if f.suffix in video_extensions
    ], key=lambda f: f.name)

    catalog = []

    for clip in clips:
        info = probe_clip(clip)
        if info is None:
            continue

        duration = float(info.get("format", {}).get("duration", 0))

        # Get video stream dimensions
        width = height = 0
        for stream in info.get("streams", []):
            if stream.get("codec_type") == "video":
                width = stream.get("width", 0)
                height = stream.get("height", 0)
                break

        # Extract thumbnail at 1s or midpoint for short clips
        thumb_time = min(1.0, duration / 2)
        thumb_path = thumb_dir / f"{clip.stem}.jpg"
        extract_thumbnail(clip, thumb_path, thumb_time)

        catalog.append({
            "filename": clip.name,
            "path": str(clip),
            "duration": round(duration, 2),
            "width": width,
            "height": height,
            "thumbnail": str(thumb_path),
            "orientation": "portrait" if height > width else "landscape"
        })

    # Also catalog audio files
    audio_folder = working_folder / "audio"
    audio_files = []
    if audio_folder.exists():
        audio_extensions = {".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg"}
        for f in sorted(audio_folder.iterdir()):
            if f.suffix.lower() in audio_extensions:
                info = probe_clip(f)
                if info:
                    duration = float(info.get("format", {}).get("duration", 0))
                    audio_files.append({
                        "filename": f.name,
                        "path": str(f),
                        "duration": round(duration, 2)
                    })

    output = {
        "working_folder": str(working_folder),
        "video_clips": catalog,
        "audio_samples": audio_files,
        "total_video_clips": len(catalog),
        "total_video_duration": round(sum(c["duration"] for c in catalog), 2),
        "total_audio_samples": len(audio_files),
        "total_audio_duration": round(sum(a["duration"] for a in audio_files), 2)
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
