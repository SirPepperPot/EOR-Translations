#!/usr/bin/env python3
"""Validate language dictionaries and publish a content-addressed EOR manifest."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ROOT / "languages"
EXPECTED = {"en", "ko", "pl", "ru", "zh-Hans"}
MAX_BYTES = 2_000_000

def strict_object(pairs):
    result = {}
    seen = set()
    for key, value in pairs:
        normalized = key.strip().casefold()
        if not normalized or key != key.strip() or normalized in seen:
            raise ValueError(f"Blank, padded or duplicate localization key: {key!r}")
        seen.add(normalized)
        result[key] = value
    return result

def load(path):
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"{path.name}: file too large")
    document = json.loads(data.decode("utf-8-sig"), object_pairs_hook=strict_object)
    if not isinstance(document, dict) or not document:
        raise ValueError(f"{path.name}: expected a nonempty JSON object")
    if any(not isinstance(k, str) or not isinstance(v, str) for k, v in document.items()):
        raise ValueError(f"{path.name}: keys and values must be strings")
    return document, data

def placeholders(value):
    numbered = re.findall(r"(?<!\{)\{\s*([0-9]+)(?:\s*,\s*-?[0-9]+)?(?:\s*:[^{}]*)?\s*\}(?!\})", value)
    named = re.findall(r"\{\{[A-Z][A-Z0-9_]+\}\}", value)
    return sorted(numbered + named)

def main():
    english, _ = load(LANGUAGES / "en.json")
    manifest = {"schemaVersion": 1, "languages": {}}
    for path in sorted(LANGUAGES.glob("*.json")):
        code = path.stem
        if code not in EXPECTED:
            raise ValueError(f"Unexpected language code: {code}")
        values, data = load(path)
        invalid = []
        for key, value in values.items():
            if key not in english or (value.strip() and placeholders(value) != placeholders(english[key])):
                invalid.append(key)
        if invalid:
            if code not in {"pl", "ru"}:
                raise ValueError(f"{code}: invalid keys/placeholders: {invalid[:8]}")
            print(f"WARNING: {code} has {len(invalid)} legacy entries requiring review")
        digest = hashlib.sha256(data).hexdigest()
        valid = values.keys() - set(invalid)
        translated = sum(bool(values[key].strip()) and (code == "en" or values[key] != english[key]) for key in valid)
        manifest["languages"][code] = {
            "file": f"languages/{path.name}",
            "version": digest[:16],
            "sha256": digest,
            "translated": translated,
            "total": len(english)
        }
    if not EXPECTED.issubset(manifest["languages"]):
        raise ValueError("Required language files missing")
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Validated and generated manifest for", ", ".join(manifest["languages"]))

if __name__ == "__main__":
    main()
