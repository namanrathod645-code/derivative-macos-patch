#!/usr/bin/env python3
"""Build the macOS shader pack from an authentic Derivative 25.0.1 archive."""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import sys
from zipfile import ZIP_DEFLATED, ZipFile
import zlib


SOURCE_SHA256 = "85602bd0acab36575733cdb122d446c99c231251bb995f4bddfa0a8d16cbbfd2"
SOURCE_PREFIX = "Derivative [25.0.1]/"
OUTPUT_NAME = "Derivative-Mac-DC-FORK-25.0.1.zip"
ENDINGS = (b"", b"\n", b"\r\n", b"\r")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def split_lines(data):
    parts = re.split(rb"(\r\n|\r|\n)", data)
    lines = [(parts[i], parts[i + 1]) for i in range(0, len(parts) - 1, 2)]
    if parts[-1]:
        lines.append((parts[-1], b""))
    return lines


def apply_delta(source, patch):
    if sha256(source) != patch["source_sha256"]:
        raise ValueError("Source file hash differs from the expected release")

    original = [content for content, _ in split_lines(source)]
    result = []
    cursor = 0
    for start, stop, inserted in patch["edits"]:
        if not (cursor <= start <= stop <= len(original)):
            raise ValueError("Invalid patch range")
        result.extend(original[cursor:start])
        result.extend(base64.b64decode(value, validate=True) for value in inserted)
        cursor = stop
    result.extend(original[cursor:])

    ending_codes = zlib.decompress(base64.b64decode(patch["endings"], validate=True))
    if len(result) != len(ending_codes) or any(code >= len(ENDINGS) for code in ending_codes):
        raise ValueError("Invalid patch line endings")
    output = b"".join(content + ENDINGS[code] for content, code in zip(result, ending_codes))
    if sha256(output) != patch["output_sha256"]:
        raise ValueError("Patched file hash differs from the expected result")
    return output


def build(source_path, output_path):
    if source_path.resolve() == output_path.resolve():
        raise ValueError("Output cannot overwrite the original archive")
    if output_path.exists():
        raise FileExistsError(f"Output already exists: {output_path}")
    if sha256(source_path.read_bytes()) != SOURCE_SHA256:
        raise ValueError("Use the official Derivative [25.0.1].zip release; SHA-256 does not match")

    patches = json.loads((Path(__file__).parent / "patches.json").read_text())
    remaining = set(patches)
    completed = 0
    try:
        with ZipFile(source_path) as original, ZipFile(output_path, "x", compression=ZIP_DEFLATED) as result:
            for info in original.infolist():
                if info.is_dir():
                    continue
                if not info.filename.startswith(SOURCE_PREFIX):
                    raise ValueError(f"Unexpected source path: {info.filename}")
                name = info.filename[len(SOURCE_PREFIX):]
                if not name or name.startswith("/") or ".." in Path(name).parts or "\\" in name:
                    raise ValueError(f"Unsafe source path: {info.filename}")
                content = original.read(info)
                if name in patches:
                    content = apply_delta(content, patches[name])
                    remaining.remove(name)
                    completed += 1
                result.writestr(name, content)
            if remaining:
                raise ValueError(f"Patch targets missing from source: {sorted(remaining)[:3]}")
    except Exception:
        output_path.unlink(missing_ok=True)
        raise
    return completed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original_zip", type=Path, help="official Derivative [25.0.1].zip")
    parser.add_argument("--output", type=Path, default=Path(OUTPUT_NAME))
    args = parser.parse_args()
    try:
        count = build(args.original_zip, args.output)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Created {args.output} ({count} patched files). Put this ZIP in Minecraft's shaderpacks folder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
