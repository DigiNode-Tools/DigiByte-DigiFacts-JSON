#!/usr/bin/env python3
#
# Name:    tidy.py
# Purpose: Remove DigiFacts from the translation files (facts/<lang>.json) and tags.json that are no longer in facts/en.json, so
#          deleting a fact only means deleting it from facts/en.json. Run by the "Build and publish DigiFacts"
#          GitHub Action before each build (it commits any changes). Nothing else in the files is changed.
#
# Usage:   build/tidy.py          Remove them
#          build/tidy.py --check  Only list them (exit code 1 if there are any)

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_DIR = os.path.join(ROOT, "facts")


def save_tags(path, data):
    """Save tags.json, with each DigiFact's tags on one line (e.g. "digifact-7ttm": ["digifacts"])."""
    text = json.dumps(data, indent=2, ensure_ascii=False)
    text = re.sub(r'\[\s*((?:"[^"]*",?\s*)+)\]', lambda m: "[" + ", ".join(re.findall(r'"[^"]*"', m.group(1))) + "]", text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")


def main():
    check = "--check" in sys.argv[1:]
    with open(os.path.join(FACTS_DIR, "en.json"), encoding="utf-8") as f:
        en = json.load(f)

    found = 0
    for name in sorted(os.listdir(FACTS_DIR)):
        if not name.endswith(".json") or name == "en.json":
            continue
        path = os.path.join(FACTS_DIR, name)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        gone = [key for key in data if not key.startswith("_") and key not in en]
        if not gone:
            continue
        found += len(gone)
        print(f"facts/{name}: {'would remove' if check else 'removed'} {', '.join(gone)} (no longer in facts/en.json)")
        if not check:
            for key in gone:
                del data[key]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")

    # The tags file too
    tags_path = os.path.join(ROOT, "tags.json")
    if os.path.exists(tags_path):
        with open(tags_path, encoding="utf-8") as f:
            tags = json.load(f)
        gone = [key for key in tags.get("facts", {}) if key not in en]
        if gone:
            found += len(gone)
            print(f"tags.json: {'would remove' if check else 'removed'} {', '.join(gone)} (no longer in facts/en.json)")
            if not check:
                for key in gone:
                    del tags["facts"][key]
                save_tags(tags_path, tags)

    if not found:
        print("Nothing to tidy: every translated DigiFact is in facts/en.json")
    sys.exit(1 if check and found else 0)


if __name__ == "__main__":
    main()
