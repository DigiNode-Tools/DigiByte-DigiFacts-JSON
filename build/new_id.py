#!/usr/bin/env python3
#
# Name:    new_id.py
# Purpose: Make a new DigiFact ID: "digifact-" and four random letters and numbers, e.g. digifact-7ttm - with no vowels
#          (so it can't spell a word), no 0, 1 or l, and never two numbers in a row (so it can't look like a number).
#          It's never one used before - not by a DigiFact in facts/en.json, nor by one that has been deleted (from
#          the git history), because websites may still be hiding a deleted DigiFact by its ID.
#
# Usage:   build/new_id.py [HOW_MANY]
#          (New DigiFacts don't need this: add them with any key, e.g. "new", and build/assign_ids.py gives them
#          an ID when they're merged.)

import json
import os
import re
import secrets
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARACTERS = "bcdfghjkmnpqrstvwxz23456789"


def used_ids(current=None):
    """Every ID in facts/en.json (or the keys given in current) and in its git history."""
    if current is None:
        with open(os.path.join(ROOT, "facts", "en.json"), encoding="utf-8") as f:
            current = json.load(f)
    used = set(current)
    try:
        history = subprocess.run(["git", "-C", ROOT, "log", "-p", "--all", "--", "facts/en.json"],
                                 capture_output=True, text=True, check=True).stdout
        used |= set(re.findall(r'^[-+ ]\s*"(digifact-[a-z0-9]{4})":', history, re.M))
    except (OSError, subprocess.CalledProcessError):
        print("(No git history found - only checked facts/en.json)", file=sys.stderr)
    return used


def new_ids(how_many, current=None):
    """A list of new, never-used IDs. current: the keys now in facts/en.json, if already read."""
    used, ids = used_ids(current), []
    for _ in range(how_many):
        while True:
            new = "digifact-" + "".join(secrets.choice(CHARACTERS) for _ in range(4))
            if new not in used and not re.search(r"[0-9]{2}", new):
                break
        used.add(new)
        ids.append(new)
    return ids


def main():
    for new in new_ids(int(sys.argv[1]) if len(sys.argv) > 1 else 1):
        print(new)


if __name__ == "__main__":
    main()
