#!/usr/bin/env python3
"""Validate language dictionaries and publish a content-addressed EOR manifest."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ROOT / "languages"
EXPECTED = {"en", "ko", "pl", "ru", "zh-Hans"}
MAX_BYTES = 2_000_000

def load(path):
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"{path.name}: file too large")
    document = json.loads(data.decode("utf-8-sig"))
    if not isinstance(document, dict):
        raise ValueError(f"{path.name}: expected JSON object")
    if any(not isinstance(k, str) or not isinstance(v, str) for k, v in document.items()):
        raise ValueError(f"{path.name}: keys and values must be strings")
    return document, data

def placeholders(value):
    import re
    return sorted(re.findall(r"(?<!\{)\{\d+(?::[^{}]+)?\}(?!\})", value))

def main():
    english, _ = load(LANGUAGES / "en.json")
    manifest = {"schemaVersion": 1, "languages": {}}
    for path in sorted(LANGUAGES.glob("*.json")):
        code = path.stem
        if code not in EXPECTED:
            raise ValueError(f"Unexpected language code: {code}")
        values, data = load(path)
        unexpected = set(values) - set(english)
        if unexpected:
            raise ValueError(f"{code}: unknown keys: {sorted(unexpected)[:8]}")
        for key, value in values.items():
            if placeholders(value) != placeholders(english[key]):
                raise ValueError(f"{code}: format placeholders changed for {key}")
        manifest["languages"][code] = {
            "file": f"languages/{path.name}",
            "version": hashlib.sha256(data).hexdigest()[:16],
            "sha256": hashlib.sha256(data).hexdigest(),
            "translated": len(values),
            "total": len(english)
        }
    if not EXPECTED.issubset(manifest["languages"]):
        raise ValueError("Required language files missing")
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Validated and generated manifest for", ", ".join(manifest["languages"]))

if __name__ == "__main__":
    main()
