#!/usr/bin/env python3
#
# Name:    check_edits.py
# Purpose: Check that edits to English DigiFacts are still the same DigiFact. A DigiFact's ID (its key, e.g. digifact-np2q) never
#          changes, and websites use IDs to hide particular DigiFacts - so a DigiFact rewritten into a different
#          one must be added as a new DigiFact instead (and the old one deleted if it's out of date). Run on pull
#          requests by the "Check DigiFacts" workflow. Fails if an edited DigiFact's text has changed too much.
#
# Usage:   build/check_edits.py OLD_EN_JSON [NEW_EN_JSON]   (NEW defaults to facts/en.json)
#          If the change really is the same DigiFact, add the label "same-digifact" to the pull request.

import difflib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_SIMILARITY = 0.5   # How much of the text must stay the same (0-1)


def text(fact):
    return " ".join(fact.get(f, "") for f in ("content", "link_social")).strip()


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: build/check_edits.py OLD_EN_JSON [NEW_EN_JSON]")
    with open(sys.argv[1], encoding="utf-8") as f:
        old = json.load(f)
    with open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "facts", "en.json"), encoding="utf-8") as f:
        new = json.load(f)

    problems = 0
    for key, fact in new.items():
        if key.startswith("_") or key not in old or not isinstance(fact, dict):
            continue
        before, after = text(old[key]), text(fact)
        if before == after:
            continue
        similarity = difflib.SequenceMatcher(None, before.lower(), after.lower()).ratio()
        if similarity < MIN_SIMILARITY:
            problems += 1
            msg = (f"{key} has changed so much ({similarity:.0%} the same) that it looks like a different DigiFact. "
                   f"Please add it as a new DigiFact instead (and delete {key} if it's out of date), because "
                   f"websites use the ID to hide particular DigiFacts. If it really is the same DigiFact, the "
                   f"maintainer can add the label 'same-digifact'.")
            print(f"::error::{msg}" if os.environ.get("GITHUB_ACTIONS") else f"ERROR: {msg}")
        else:
            print(f"{key}: edited ({similarity:.0%} the same) - OK")

    if problems:
        sys.exit(1)
    print("Edited DigiFacts are still the same DigiFacts")


if __name__ == "__main__":
    main()
