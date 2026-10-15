#!/usr/bin/env python3
"""Fill missing Korean translations with machine translations, preserving existing work."""
# One-time localization backfill; retains all approved pre-existing translations.
import json
import re
import sys
import time
from pathlib import Path
from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "languages/en.json"
KO = ROOT / "languages/ko.json"
TOKEN = re.compile(r"(\\{[^{}]+\\}|<[^<>]+>|%[0-9]*[sdif]|\\\\[nr]|\\[[^\\]]+\\])")

def translated_with_tokens(engine, text):
    tokens = []
    def stash(match):
        tokens.append(match.group(0))
        return f"EORSAFEPLACEHOLDER{len(tokens) - 1}END"
    masked = TOKEN.sub(stash, text)
    for attempt in range(6):
        try:
            result = engine.translate(masked)
            if not isinstance(result, str) or not result.strip():
                raise ValueError("Empty translation")
            for index, token in enumerate(tokens):
                marker = f"EORSAFEPLACEHOLDER{index}END"
                if marker not in result:
                    raise ValueError(f"Placeholder {index} altered")
                result = result.replace(marker, token)
            if sorted(TOKEN.findall(result)) != sorted(TOKEN.findall(text)):
                raise ValueError("Formatting token mismatch")
            return result
        except Exception as exc:
            if attempt == 5:
                raise RuntimeError(f"Unable to translate {text[:80]!r}: {exc}") from exc
            time.sleep(min(30, 2 ** attempt))
    raise AssertionError("unreachable")

def main():
    english = json.loads(EN.read_text(encoding="utf-8"))
    korean = json.loads(KO.read_text(encoding="utf-8"))
    if not isinstance(english, dict) or not isinstance(korean, dict):
        raise ValueError("Expected language dictionaries")
    engine = GoogleTranslator(source="en", target="ko")
    cache = {}
    missing = [(key, value) for key, value in english.items() if key not in korean]
    print(f"Translating {len(missing)} missing keys", flush=True)
    for index, (key, value) in enumerate(missing, 1):
        if not isinstance(value, str):
            raise ValueError(f"Nonstring English source for {key}")
        if not value.strip():
            korean[key] = value
        elif value in cache:
            korean[key] = cache[value]
        else:
            result = translated_with_tokens(engine, value)
            cache[value] = result
            korean[key] = result
        if index % 100 == 0:
            print(f"{index}/{len(missing)} complete", flush=True)
    if set(korean) != set(english):
        raise ValueError("Korean key set differs from English")
    for key, value in english.items():
        if not isinstance(korean[key], str):
            raise ValueError(f"Nonstring translation: {key}")
        if sorted(TOKEN.findall(value)) != sorted(TOKEN.findall(korean[key])):
            raise ValueError(f"Formatting tokens differ: {key}")
    KO.write_text(json.dumps({key: korean[key] for key in english}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Finished: {len(korean)}/{len(english)} keys", flush=True)

if __name__ == "__main__":
    main()
