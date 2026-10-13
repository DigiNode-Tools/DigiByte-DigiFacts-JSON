#!/usr/bin/env python3
#
# Name:    build.py
# Purpose: Build the DigiFacts website (https://digifacts.diginode.tools) from the facts in facts/<lang>.json.
#          Run hourly by the "Build and publish DigiFacts" GitHub Action, and whenever the facts change.
#
#          1. Checks every facts file (a broken file stops the build, so the live site is never broken).
#          2. Gets the current DigiByte block count from several block explorers. It uses the middle value of the
#             ones that look right, never goes backwards, and falls back to an estimate (one block every 15
#             seconds) if no explorer answers.
#          3. Numbers the facts in the order they appear in facts/en.json (so deleting one never leaves a gap), makes
#             each title from the language's "_title" (e.g. "DigiFact #{number}"), fills in the
#             live values (e.g. $blocks_tot_mil) and writes each language in each format (social, html, markdown),
#             plus languages.json, info.json, and the help and proofreading pages. A fact that isn't translated yet
#             is shown in English.
#          4. Picks the DigiFact of the day (the same fact in every language, every fact once before any repeats)
#             and writes <lang>/today.json and an RSS feed of the last 30 days, <lang>/feed.xml.
#
#          Everything here is public, so anyone can see exactly how DigiFacts are made.
#
# Usage:   build/build.py OUT_DIR
#          Environment (optional):
#            DIGIFACTS_SITE_URL   Where the site is published, to read the previous info.json (block count never
#                                 goes backwards, and the build can tell whether anything changed)
#            GITHUB_OUTPUT        Set by GitHub Actions: 'changed=true|false' is written to it
#            FORCE_PUBLISH=1      Report changed=true even if nothing changed

import email.utils
import hashlib
import html
import json
import os
import random
import re
import statistics
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_DIR = os.path.join(ROOT, "facts")
REPO_URL = "https://github.com/DigiNode-Tools/digibyte-digifacts"
SITE_URL = "https://digifacts.diginode.tools"
# Short links for facts with a link: SHORT_BASE + the fact's key number, e.g. HTTPS://DIGIFACTS.DIGINODE.TOOLS/L/55.
# In capitals on purpose: a QR code can then use its compact alphanumeric mode, so the code is small enough for
# a 64x32 display (25x25). The site publishes a redirect page for each one (L/55.html).
SHORT_BASE = SITE_URL.upper() + "/L/"
SPONSOR_URL = "https://github.com/sponsors/DigiNode-Tools"
USER_AGENT = f"DigiFacts builder ({REPO_URL})"

LANGUAGE_NAMES = {
    "en": "English", "de": "German", "es": "Spanish", "fr": "French", "hi": "Hindi", "it": "Italian",
    "ja": "Japanese", "ko": "Korean", "nl": "Dutch", "pt": "Portuguese", "ru": "Russian",
    "zh": "Chinese (Simplified)",
}
FIELDS = ("content", "url", "link_social", "link_html", "link_md")
TITLE_KEY = "_title"   # Each language's title, e.g. "DigiFact #{number}"
FORMATS = {"social": "link_social", "html": "link_html", "markdown": "link_md"}
OUTPUT_FORMATS = dict(FORMATS, plain=None)   # plain = the fact without its link (e.g. for small displays)

# The only HTML allowed in a fact: one link, in link_html. (Sites may show the html format as HTML.)
LINK_HTML_RE = re.compile(r'[^<>]*<a target="_blank" href="https://[^"<>\s]+">[^<>]+</a>[^<>]*')

# Block count. A reading is only used if it's within 3% of the estimate below (one block every 15 seconds since
# a known block), and never lower than the last published count.
BLOCK_TIME = 15
ANCHOR_HEIGHT, ANCHOR_TIME = 24372532, 1791825343   # 2026-10-12 17:15 UTC
SANE_RANGE = 0.03


def explorer_chainz():
    return int(fetch("https://chainz.cryptoid.info/dgb/api.dws?q=getblockcount").strip())


def explorer_digibyte_io():
    return int(json.loads(fetch("https://digibyte.io/api/getblockchaininfo"))["blocks"])


def explorer_atomic_blockbook():
    d = json.loads(fetch("https://digibyte.atomicwallet.io/api/"))["blockbook"]
    if not d.get("inSync"):
        raise ValueError("not in sync")
    return int(d["bestHeight"])


EXPLORERS = {
    "chainz.cryptoid.info": explorer_chainz,
    "digibyte.io": explorer_digibyte_io,
    "digibyte.atomicwallet.io": explorer_atomic_blockbook,
}

# Live values that can be used in a fact. Longer names first, so $blocks_tot_mil isn't read as $blocks_tot.
VARIABLES = {
    "$blocks_tot_mil": lambda n: f"{n // 1000000}.{(n % 1000000) // 100000}",   # 24.3 (rounded down)
    "$blocks_tot_cs": lambda n: f"{n:,}",                                       # 24,372,532
    "$blocks_tot": lambda n: str(n),                                            # 24372532
}
VARIABLE_RE = re.compile(r"\$[a-z_]+")


def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")


def warn(msg):
    print(f"::warning::{msg}" if os.environ.get("GITHUB_ACTIONS") else f"WARNING: {msg}")


def fail(msg):
    sys.exit(f"::error::{msg}" if os.environ.get("GITHUB_ACTIONS") else f"ERROR: {msg}")


# ---------------------------------------------------------------------------------------------------------------
# 1. Read and check the facts

def load_facts():
    """Return ({lang: {key: fact}}, {lang: title}) in language order (English first), checking everything.
    Exits on a problem."""
    # Language files are named with their language code: de.json, or e.g. pt_BR.json / pt-br.json for a regional
    # variant (Weblate names new files pt_BR.json). On the website the code is lower case with a hyphen: pt-br.
    files = {}
    for name in os.listdir(FACTS_DIR):
        if name.endswith(".json"):
            code = name[:-5]
            if not re.fullmatch(r"[a-z]{2,3}([_-][A-Za-z0-9]{2,4})?", code):
                fail(f"facts/{name}: name the file with a language code, e.g. de.json or pt_BR.json")
            files[code.lower().replace("_", "-")] = name
    langs = sorted(files, key=lambda l: (l != "en", l))
    if "en" not in langs:
        fail("facts/en.json is missing")
    facts, titles = {}, {}
    for lang in langs:
        path = f"facts/{files[lang]}"
        if lang not in LANGUAGE_NAMES:
            warn(f"{path}: add the language's name to LANGUAGE_NAMES in build/build.py")
            LANGUAGE_NAMES[lang] = lang
        try:
            with open(os.path.join(FACTS_DIR, files[lang]), encoding="utf-8") as f:
                data = json.load(f)
        except ValueError as e:
            fail(f"{path} is not valid JSON: {e}")
        if not isinstance(data, dict):
            fail(f"{path} should contain one object with a key for each DigiFact")
        title = data.pop(TITLE_KEY, "")
        if title:
            if not isinstance(title, str) or title.count("{number}") != 1 or re.search(r"[<>$]", title):
                fail(f'{path} {TITLE_KEY} should be text containing {{number}} once, e.g. "DigiFact #{{number}}"')
            titles[lang] = title
        for key, fact in data.items():
            where = f"{path} {key}"
            if not re.fullmatch(r"digifact[1-9][0-9]*", key):
                fail(f"{where}: keys must be digifact1, digifact2, ...")
            if not isinstance(fact, dict):
                fail(f"{where} should be an object")
            for field, value in fact.items():
                if field not in FIELDS:
                    hint = f" - titles are now set once per language, with {TITLE_KEY}" if field == "title" else ""
                    fail(f"{where}: unknown field '{field}' (allowed: {', '.join(FIELDS)}){hint}")
                if not isinstance(value, str):
                    fail(f"{where} {field} should be text")
                if field != "link_html" and re.search(r"[<>]", value):
                    fail(f"{where} {field}: '<' and '>' aren't allowed (only link_html may contain a link)")
                for var in VARIABLE_RE.findall(value):
                    if var not in VARIABLES:
                        fail(f"{where} {field}: unknown live value '{var}' (available: {', '.join(VARIABLES)})")
            if fact.get("link_html") and not LINK_HTML_RE.fullmatch(fact["link_html"]):
                fail(f'{where} link_html should contain exactly one link: <a target="_blank" href="https://...">text</a>')
            if fact.get("url") and not re.fullmatch(r"https://\S+", fact["url"]):
                fail(f"{where} url should start with https://")
        facts[lang] = data

    en = facts["en"]
    if "en" not in titles:
        fail(f"facts/en.json needs a {TITLE_KEY}")
    for key, fact in en.items():
        if not fact.get("content"):
            fail(f"facts/en.json {key} needs content")
        if fact.get("url"):
            for field in ("link_social", "link_html", "link_md"):
                if fact["url"] not in fact.get(field, ""):
                    fail(f"facts/en.json {key} {field} should contain the url")
    for lang in langs[1:]:
        for key, fact in facts[lang].items():
            if key not in en:
                warn(f"facts/{files[lang]} {key} isn't in facts/en.json - it will be ignored (build/tidy.py removes it)")
                continue
            if fact.get("content"):
                if set(VARIABLE_RE.findall(en[key]["content"])) != set(VARIABLE_RE.findall(fact["content"])):
                    warn(f"facts/{files[lang]} {key} content should use the same live values as English: "
                         f"{', '.join(sorted(set(VARIABLE_RE.findall(en[key]['content'])))) or 'none'}")
        if lang not in titles:
            warn(f"facts/{files[lang]} has no {TITLE_KEY} - the English title is used")
    return facts, titles


def localise(facts, titles, lang):
    """The facts for one language, in English order, numbered from 1: the translation where there is one, else the
    English fact. Each fact gets its title, from the language's title (or the English one) and its number."""
    en, tr = facts["en"], facts[lang]
    title = titles.get(lang, titles["en"])
    out, translated = {}, 0
    for number, key in enumerate(en, start=1):
        fact = tr.get(key) or {}
        if lang != "en" and not fact.get("content"):
            out[key] = dict(en[key], title=title.replace("{number}", str(number)), translated=False)
            continue
        fact = dict(fact)
        fact["url"] = fact.get("url") or en[key].get("url", "")
        if en[key].get("url") and not all(fact.get(f) for f in FORMATS.values()):
            for f in FORMATS.values():   # Translated text, but no translated link yet: use the English link
                fact[f] = en[key].get(f, "")
        out[key] = dict(fact, title=title.replace("{number}", str(number)), translated=True)
        translated += 1
    return out, translated


# ---------------------------------------------------------------------------------------------------------------
# 2. Block count

def previous_info():
    site = os.environ.get("DIGIFACTS_SITE_URL", "").rstrip("/")
    if not site:
        return {}
    try:
        info = json.loads(fetch(f"{site}/info.json"))
        return info if isinstance(info, dict) else {}
    except Exception as e:
        print(f"No previous info.json ({e})")
        return {}


def block_count(prev):
    now = int(time.time())
    prev_count = prev.get("block_count") if isinstance(prev.get("block_count"), int) else 0
    prev_time = prev.get("block_count_time") if isinstance(prev.get("block_count_time"), int) else 0
    if prev_count and prev_time:
        estimate = prev_count + (now - prev_time) // BLOCK_TIME
    else:
        estimate = ANCHOR_HEIGHT + (now - ANCHOR_TIME) // BLOCK_TIME

    readings = {}
    for name, get in EXPLORERS.items():
        try:
            n = get()
        except Exception as e:
            warn(f"Block explorer {name} didn't answer: {e}")
            continue
        if abs(n - estimate) > estimate * SANE_RANGE:
            warn(f"Block explorer {name} says {n:,}, too far from the expected {estimate:,} - ignored")
            continue
        readings[name] = n
        print(f"Block explorer {name}: {n:,}")

    if readings:
        count = statistics.median_low(readings.values())
        source = ", ".join(sorted(readings))
    else:
        warn(f"No block explorer answered - using an estimate ({estimate:,})")
        count, source = estimate, "estimate"
    if count < prev_count:
        count = prev_count   # Never go backwards
    return count, source, now, readings


# ---------------------------------------------------------------------------------------------------------------
# 3. Output

FEED_DAYS = 30


def fact_of_the_day(keys, day):
    """The DigiFact for a day (days since 1970-01-01, UTC). The facts are shuffled into a new order each cycle, so
    every fact is shown once before any is repeated, and the same fact is chosen in every language."""
    def order(cycle):
        o = list(keys)
        random.Random(f"digifacts-{cycle}").shuffle(o)
        return o
    cycle, pos = divmod(day, len(keys))
    o = order(cycle)
    if len(o) > 1 and o[0] == order(cycle - 1)[-1]:
        o[0], o[1] = o[1], o[0]   # Don't show the same fact two days running, between cycles
    return o[pos]


def today_and_feed(lang, loc, count, day):
    """<lang>/today.json and <lang>/feed.xml (RSS) for one language."""
    keys = list(loc)
    numbers = {key: n for n, key in enumerate(keys, start=1)}

    def entry(d):
        key = fact_of_the_day(keys, d)
        f = loc[key]
        return {
            "date": time.strftime("%Y-%m-%d", time.gmtime(d * 86400)),
            "number": numbers[key],
            "key": key,
            "title": fill(f["title"], count),
            "url": f.get("url", ""),
            "text": fill(f["content"] + f.get("link_social", ""), count),
            "html": fill(f["content"] + f.get("link_html", ""), count),
            "markdown": fill(f["content"] + f.get("link_md", ""), count),
            "plain": fill(f["content"], count),
            "short_url": short_url(key, f),
        }

    today = entry(day)
    items = []
    for d in range(day, day - FEED_DAYS, -1):
        e = entry(d)
        items.append(
            "<item>"
            f"<title>{html.escape(e['title'])}</title>"
            f"<description>{html.escape(e['text'])}</description>"
            f"<link>{html.escape(e['url'] or SITE_URL + '/help/')}</link>"
            f"<guid isPermaLink=\"false\">digifacts-{lang}-{e['date']}</guid>"
            f"<pubDate>{email.utils.formatdate(d * 86400, usegmt=True)}</pubDate>"
            "</item>")
    feed = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            f"<title>DigiByte DigiFacts ({html.escape(LANGUAGE_NAMES[lang])})</title>"
            f"<link>{SITE_URL}/help/</link>"
            "<description>A DigiFact - a bite-size fact about DigiByte - every day.</description>"
            f"<language>{lang}</language>"
            + "".join(items) + "</channel></rss>\n")
    return to_json(today), feed


def short_url(key, fact):
    return SHORT_BASE + key[len("digifact"):] if fact.get("url") else ""


def redirect_page(url):
    u = html.escape(url, quote=True)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>DigiFacts link</title>'
            f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={u}">'
            f'<link rel="canonical" href="{u}"><script>location.replace({json.dumps(url)})</script></head>'
            f'<body><p>Going to <a href="{u}">{u}</a></p></body></html>\n')


def fill(text, count):
    for var, value in VARIABLES.items():
        text = text.replace(var, value(count))
    return text


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def to_json(data):
    return json.dumps(data, indent=4, ensure_ascii=False) + "\n"


PAGE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{ color-scheme: light dark; --fg: #1d2330; --muted: #5b6475; --bg: #fff; --card: #f4f7fb; --line: #d9e1ec; --accent: #0066cc; }}
@media (prefers-color-scheme: dark) {{ :root {{ --fg: #e6ebf2; --muted: #9aa6b8; --bg: #0f1520; --card: #172131; --line: #26344a; --accent: #5aa9ff; }} }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width: 1100px; margin: 0 auto; padding: 24px 16px 48px; }}
h1 {{ font-size: 1.7em; margin: 0 0 .3em; }} h2 {{ margin-top: 1.8em; }}
a {{ color: var(--accent); }} code {{ background: var(--card); padding: .1em .35em; border-radius: 4px; font-size: .92em; word-break: break-all; }}
.muted {{ color: var(--muted); }}
table {{ border-collapse: collapse; width: 100%; }} th, td {{ text-align: left; padding: .45em .6em; border-bottom: 1px solid var(--line); vertical-align: top; }}
.scroll {{ overflow-x: auto; }}
.langs a {{ display: inline-block; margin: 0 .5em .4em 0; }}
.row {{ display: grid; gap: 12px; margin: 12px 0; }} .row.two {{ grid-template-columns: 1fr 1fr; }}
@media (max-width: 700px) {{ .row.two {{ grid-template-columns: 1fr; }} }}
.fact {{ background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 12px 14px; overflow-wrap: anywhere; }}
.fact h3 {{ margin: 0 0 .3em; font-size: 1em; }} .fact p {{ margin: 0; }}
.missing {{ color: #c0392b; font-weight: 600; }}
</style>
</head>
<body><main>
{body}
</main></body>
</html>
"""


def help_page(langs, info):
    rows = "\n".join(
        f'<tr><td>{html.escape(LANGUAGE_NAMES[l])}</td><td><code>{l}</code></td>'
        f'<td><a href="../{l}/social.json">social</a> · <a href="../{l}/html.json">html</a> · '
        f'<a href="../{l}/markdown.json">markdown</a> · <a href="../{l}/plain.json">plain</a></td>'
        f'<td>{info["languages"][l]["translated"]} of {info["facts"]}</td>'
        f'<td><a href="../proofread/{l}/">proofread</a></td></tr>' for l in langs)
    body = f"""<h1>DigiByte DigiFacts</h1>
<p>Bite-size facts about DigiByte, for apps, websites and social media, in {len(langs)} languages. Free to use: the facts are MIT licensed.</p>

<h2>Get the DigiFacts</h2>
<p>Each language is a JSON file in four formats. The address is <code>https://digifacts.diginode.tools/&lt;language&gt;/&lt;format&gt;.json</code>, for example <a href="../en/social.json"><code>/en/social.json</code></a>.</p>
<ul>
<li><b>social</b> - links as plain URLs, for social media: <code>Learn more: https://example.com</code></li>
<li><b>html</b> - links as HTML, for websites: <code>Learn more &lt;a href="https://example.com"&gt;here&lt;/a&gt;.</code></li>
<li><b>markdown</b> - links in Markdown: <code>Learn more [here](https://example.com).</code></li>
<li><b>plain</b> - no link, just the fact (e.g. for small displays). The link is still in <code>url</code>.</li>
</ul>
<p>A fact that isn't translated yet is included in English, so every language always has every fact.</p>
<div class="scroll"><table>
<tr><th>Language</th><th>Code</th><th>Files</th><th>Translated</th><th></th></tr>
{rows}
</table></div>

<h2>Other files</h2>
<ul>
<li><a href="../languages.json"><code>/languages.json</code></a> - the language codes, as a JSON list.</li>
<li><a href="../en/today.json"><code>/&lt;language&gt;/today.json</code></a> - the DigiFact of the day: the same fact for everyone, in every language, changing at midnight UTC. Every fact is shown once before any repeats. Includes the title, number, and the text in all three formats.</li>
<li><a href="../en/feed.xml"><code>/&lt;language&gt;/feed.xml</code></a> - an RSS feed of the DigiFact of the day (the last 30 days). Use it with any RSS app, or an RSS bot to post DigiFacts to Discord, Telegram or social media.</li>
<li><a href="../info.json"><code>/info.json</code></a> - when the facts were last published, the block count used and where it came from, and each language's progress.</li>
</ul>

<h2>Using them</h2>
<ul>
<li>Show a random fact, e.g. when the page loads or once a minute.</li>
<li>Some facts include live data such as the number of DigiByte blocks, so fetch the file again every few hours. Don't fetch it more than once an hour.</li>
<li>Browsers can fetch the files directly (CORS is allowed), so they work in any website or app.</li>
</ul>

<h2>Add DigiFacts to your website</h2>
<p>Add this where you want a DigiFact to appear. It shows a random DigiFact, which changes every minute, and uses your site's font and colours:</p>
<pre><code>&lt;div data-digifacts data-lang="en"&gt;&lt;/div&gt;
&lt;script src="https://digifacts.diginode.tools/embed/v1/digifacts.js" async&gt;&lt;/script&gt;</code></pre>
<p>Options (attributes on the div): <code>data-lang</code> (a language code, or <code>auto</code> for the visitor's language), <code>data-box="no"</code> (text only), <code>data-interval</code> (seconds between DigiFacts, or <code>0</code> for just one), <code>data-credit="no"</code> (hide the small DigiFacts link) and <code>data-accent</code> (a colour, e.g. <code>#0066cc</code>). Here it is:</p>
<div data-digifacts data-lang="en"></div>
<script src="../embed/v1/digifacts.js" async></script>
<p>On WordPress, you can use the <a href="https://github.com/DigiNode-Tools/digibyte-digifacts/tree/main/wordpress">DigiFacts plugin</a> instead.</p>

<h2>How they're made</h2>
<p>The facts live in the <a href="{REPO_URL}">digibyte-digifacts</a> repository. Every hour, and whenever the facts change, a public <a href="{REPO_URL}/actions">GitHub Action</a> checks them, fills in the live data and publishes this site. The block count comes from several block explorers (currently {html.escape(", ".join(EXPLORERS))}); the middle value is used, and if none of them answer, an estimate based on DigiByte's 15 second block time.</p>

<h2>Help improve them</h2>
<p>Spotted a mistake, or a fact that's out of date? Translations can always be improved too, and new languages are welcome. See <a href="{REPO_URL}#contributing">how to contribute</a>, or <a href="../proofread/en/">read through the facts</a>.</p>
<p>DigiFacts are maintained by <a href="https://diginode.tools">DigiNode Tools</a>. If you find them useful, please consider <a href="{SPONSOR_URL}">sponsoring DigiNode Tools</a>.</p>
<p class="muted">Last published {time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(info["built"]))}.</p>"""
    return PAGE.format(lang="en", title="DigiByte DigiFacts", body=body)


def proofread_page(lang, langs, en_facts, facts, count):
    links = " ".join(f'<a href="../{l}/">{html.escape(LANGUAGE_NAMES[l])}</a>' for l in langs)

    def card(key, fact, missing=False):
        if missing:
            return f'<div class="fact"><h3>{key}</h3><p class="missing">Not translated yet - shown in English.</p></div>'
        link = fill(fact.get("link_social", ""), count)
        return (f'<div class="fact"><h3>{html.escape(fill(fact["title"], count))}</h3>'
                f'<p>{html.escape(fill(fact["content"], count))}{html.escape(link)}</p></div>')

    rows = []
    for key, fact in facts.items():
        if lang == "en":
            rows.append(f'<div class="row">{card(key, fact)}</div>')
        else:
            rows.append(f'<div class="row two">{card(key, en_facts[key])}{card(key, fact, not fact["translated"])}</div>')
    intro = ("Read through the English DigiFacts below." if lang == "en" else
             f"The English DigiFacts on the left, and the {html.escape(LANGUAGE_NAMES[lang])} translation on the right.")
    body = f"""<h1>DigiFacts proofreading: {html.escape(LANGUAGE_NAMES[lang])}</h1>
<p>{intro} Found a mistake? See <a href="{REPO_URL}#contributing">how to fix it</a>. Thank you!</p>
<p class="langs">{links}</p>
{"".join(rows)}
<p class="muted"><a href="../../help/">About DigiFacts</a></p>"""
    return PAGE.format(lang=lang, title=f"DigiFacts proofreading: {LANGUAGE_NAMES[lang]}", body=body)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: build/build.py OUT_DIR")
    out_dir = sys.argv[1]
    facts, titles = load_facts()
    langs = list(facts)
    prev = previous_info()
    count, source, count_time, readings = block_count(prev)

    files, langs_info, localised = {}, {}, {}
    day = int(time.time() // 86400)
    for lang in langs:
        loc, translated = localise(facts, titles, lang)
        localised[lang] = loc
        langs_info[lang] = {"name": LANGUAGE_NAMES[lang], "translated": translated}
        for fmt, link_field in OUTPUT_FORMATS.items():
            data = {key: {"title": fill(f["title"], count),
                          "content": fill(f["content"] + (f.get(link_field, "") if link_field else ""), count),
                          "url": f.get("url", ""),
                          "short_url": short_url(key, f)} for key, f in loc.items()}
            files[f"{lang}/{fmt}.json"] = to_json(data)
        files[f"{lang}/today.json"], files[f"{lang}/feed.xml"] = today_and_feed(lang, loc, count, day)
    files["index.html"] = files["en/social.json"]   # DigiNode Tools v26.10.x and older use '/?lang=en&format=social'
    files["languages.json"] = json.dumps(langs) + "\n"
    with open(os.path.join(ROOT, "embed", "digifacts.js"), encoding="utf-8") as f:
        files["embed/v1/digifacts.js"] = f.read()   # The embed for any website (v1: keep it compatible)

    # Did anything change since the last publish? (Not counting info.json's times)
    digest = hashlib.sha256("".join(f"{p}\n{c}" for p, c in sorted(files.items())).encode("utf-8")).hexdigest()
    changed = digest != prev.get("content_hash") or os.environ.get("FORCE_PUBLISH") == "1"
    if not changed:   # Keep the published block count, so info.json matches the published facts
        count, source, count_time = prev["block_count"], prev.get("block_count_source", source), prev["block_count_time"]

    info = {
        "built": int(time.time()),
        "facts": len(facts["en"]),
        "block_count": count,
        "block_count_source": source,
        "block_count_time": count_time,
        "explorers": readings,
        "languages": langs_info,
        "formats": list(OUTPUT_FORMATS),
        "source": REPO_URL,
        "commit": os.environ.get("GITHUB_SHA", ""),
        "content_hash": digest,
    }
    files["info.json"] = to_json(info)
    files["help/index.html"] = help_page(langs, info)
    for lang in langs:
        files[f"proofread/{lang}/index.html"] = proofread_page(lang, langs, localised["en"], localised[lang], count)
    files["proofread/index.html"] = '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=en/"><a href="en/">Proofread the DigiFacts</a>\n'
    files[".nojekyll"] = ""
    for key, f in facts["en"].items():
        if f.get("url"):
            files[f"L/{key[len('digifact'):]}.html"] = redirect_page(f["url"])

    for path, content in files.items():
        write(os.path.join(out_dir, path), content)

    print(f"Built {len(files)} files: {len(facts['en'])} facts in {len(langs)} languages, "
          f"block count {count:,} ({source}){'' if changed else ' - nothing changed'}")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")


if __name__ == "__main__":
    main()
