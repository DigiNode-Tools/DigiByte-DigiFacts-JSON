#!/usr/bin/env python3
#
# Name:    assign_ids.py
# Purpose: Give new DigiFacts their IDs. Contributors never choose an ID: a new DigiFact can be added with any key
#          (e.g. "new"), an empty key (""), or no key at all - just { "content": ... } in the list. Any key in
#          facts/en.json that wasn't there before is replaced by a new ID (from build/new_id.py, never used before),
#          in every facts file and in tags.json, and facts/en.json is saved as valid JSON again.
#          - When a change is merged, the "Build and publish DigiFacts" GitHub Action runs this (comparing with
#            facts/en.json before the change) and commits the new IDs.
#          - On a pull request, the "Check DigiFacts" GitHub Action runs it (on its own copy, without committing)
#            before checking the DigiFacts.
#
# Usage:   build/assign_ids.py OLD_EN_JSON

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from new_id import new_ids   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_DIR = os.path.join(ROOT, "facts")
TAGS_FILE = os.path.join(ROOT, "tags.json")


def no_duplicate_keys(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            sys.exit(f'ERROR: the key "{key}" is used twice in a file - a new DigiFact needs a key of its own '
                     f'(e.g. "new", "new-2", ...)')
        data[key] = value
    return data


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=no_duplicate_keys)


def load_en(path):
    """facts/en.json, allowing new DigiFacts with no key ({ "content": ... } on its own) or an empty key: each gets
    a temporary key ("(new 1)", ...), which is then replaced by its ID like any other new key."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    decoder, data, missing = json.JSONDecoder(object_pairs_hook=no_duplicate_keys), {}, 0
    ws = " \t\r\n"

    def skip(i):
        while i < len(text) and text[i] in ws:
            i += 1
        return i

    def problem(i, what):
        line = text.count("\n", 0, i) + 1
        sys.exit(f"ERROR: facts/en.json line {line}: {what}")

    i = skip(0)
    if text[i:i + 1] != "{":
        problem(i, "it should start with {")
    i = skip(i + 1)
    while text[i:i + 1] != "}":
        if text[i:i + 1] == '"':
            key, i = decoder.raw_decode(text, i)
            i = skip(i)
            if text[i:i + 1] != ":":
                problem(i, f'a ":" is missing after "{key}"')
            value, i = decoder.raw_decode(text, skip(i + 1))
        elif text[i:i + 1] == "{":
            key, (value, i) = "", decoder.raw_decode(text, i)   # A DigiFact with no key
        else:
            problem(i, "expected a DigiFact (a key in quotes, or { ... })")
        if key == "":
            missing += 1
            key = f"(new {missing})"
        if key in data:
            sys.exit(f'ERROR: the key "{key}" is used twice in facts/en.json - a new DigiFact needs a key of its own '
                     f'(e.g. "new", "new-2", ...), or none')
        data[key] = value
        i = skip(i)
        if text[i:i + 1] == ",":
            i = skip(i + 1)
        elif text[i:i + 1] != "}":
            problem(i, 'a "," is missing between two DigiFacts')
    return data


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: build/assign_ids.py OLD_EN_JSON")
    old = load(sys.argv[1])
    en_path = os.path.join(FACTS_DIR, "en.json")
    en = load_en(en_path)
    new_keys = [key for key in en if not key.startswith("_") and key not in old]
    if not new_keys:
        print("No new DigiFacts to give IDs to")
        return
    ids = dict(zip(new_keys, new_ids(len(new_keys), en)))

    for name in sorted(os.listdir(FACTS_DIR)):
        if name.endswith(".json"):
            path = os.path.join(FACTS_DIR, name)
            data = en if path == en_path else load(path)
            if any(key in ids for key in data):
                save(path, {ids.get(key, key): value for key, value in data.items()})
    if os.path.exists(TAGS_FILE):
        tags = load(TAGS_FILE)
        if any(key in ids for key in tags.get("facts", {})):
            tags["facts"] = {ids.get(key, key): value for key, value in tags["facts"].items()}
            save(TAGS_FILE, tags)
    for key, new in ids.items():
        print(f"New DigiFact {key} -> {new}")


if __name__ == "__main__":
    main()
