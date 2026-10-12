#!/usr/bin/env python3
#
# Name:    tidy.py
# Purpose: Remove DigiFacts from the translation files (facts/<lang>.json) that are no longer in facts/en.json, so
#          deleting a fact only means deleting it from facts/en.json. Run by the "Build and publish DigiFacts"
#          GitHub Action before each build (it commits any changes). Nothing else in the files is changed.
#
# Usage:   build/tidy.py          Remove them
#          build/tidy.py --check  Only list them (exit code 1 if there are any)

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_DIR = os.path.join(ROOT, "facts")


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

    if not found:
        print("Nothing to tidy: every translated DigiFact is in facts/en.json")
    sys.exit(1 if check and found else 0)


if __name__ == "__main__":
    main()
