"""
Applet: DigiFacts
Summary: Facts about DigiByte
Description: Shows a DigiFact - a bite-size fact about DigiByte - in your language. Choose the DigiFact of the day, or a random DigiFact each time.
Author: saltedlolly
"""

load("encoding/json.star", "json")
load("http.star", "http")
load("images/dgb_icon.png", DGB_ICON = "file")
load("random.star", "random")
load("render.star", "canvas", "render")
load("schema.star", "schema")

SITE = "https://digifacts.diginode.tools"

# Languages the display fonts can show (no fonts for Chinese, Hindi, Japanese or Korean yet)
LANGUAGES = [
    ("English", "en"),
    ("Deutsch", "de"),
    ("Español", "es"),
    ("Français", "fr"),
    ("Italiano", "it"),
    ("Nederlands", "nl"),
    ("Português", "pt"),
    ("Русский", "ru"),
]

# Fonts for each text size: (64 pixel wide displays: 64x32 and 64x64, 128x64 displays)
FONTS = {
    "small": ("tom-thumb", "terminus-12"),
    "medium": ("tb-8", "terminus-16"),
    "large": ("6x10", "terminus-20"),
}
NO_CYRILLIC = ["tom-thumb"]  # Fonts without Cyrillic letters (for Russian, the medium font is used instead)

DIGIBYTE_BLUE = "#0066cc"
TEXT_COLOR = "#ffffff"
CACHE_SECONDS = 3600
INTRO_SECONDS = 2  # How long the DigiByte logo and the DigiFact number are shown before the DigiFact scrolls

def main(config):
    lang = config.get("language", "en")
    if lang not in [code for _, code in LANGUAGES]:
        lang = "en"

    fact = random_fact(lang) if config.get("mode", "today") == "random" else fact_of_the_day(lang)
    if fact == None:
        return []  # Skip this time if the DigiFacts can't be loaded

    size = config.get("size", "medium")
    if size not in FONTS:
        size = "medium"
    return render_fact(fact["header"], fact["text"], size, lang)

def get_json(url):
    res = http.get(url = url, ttl_seconds = CACHE_SECONDS)
    if res.status_code != 200:
        return None
    return json.decode(res.body())

def header_of(title):
    # "DigiFact # 22 - Did you know..." -> "DigiFact #22" (short enough for a 64 pixel wide display)
    return title.split(" - ")[0].strip().replace("# ", "#")

def intro_card(header, width, height, big, header_font):
    # The DigiByte logo next to the DigiFact's name and number ("DigiFact" above "#22")
    parts = header.rsplit("#", 1)
    name = parts[0].strip()
    number = "#" + parts[1] if len(parts) == 2 else ""
    text = [
        render.Text(name, font = header_font, color = TEXT_COLOR),
        render.Text(number, font = header_font, color = TEXT_COLOR),
    ]
    if width == height:
        # Square (64x64): a bigger logo, with the name and number underneath
        return render.Box(
            width = width,
            height = height,
            child = render.Column(
                expanded = True,
                main_align = "space_evenly",
                cross_align = "center",
                children = [
                    render.Image(src = DGB_ICON.readall(), width = 36, height = 36),
                    render.Column(cross_align = "center", children = text),
                ],
            ),
        )
    size = 36 if big else 18
    return render.Box(
        width = width,
        height = height,
        child = render.Row(
            expanded = True,
            main_align = "space_evenly",
            cross_align = "center",
            children = [
                render.Image(src = DGB_ICON.readall(), width = size, height = size),
                render.Column(cross_align = "center", children = text),
            ],
        ),
    )

def fact_of_the_day(lang):
    data = get_json("%s/%s/today.json" % (SITE, lang))
    if data == None or not data.get("plain"):
        return None
    return {"header": header_of(data.get("title", "DigiFact")), "text": data["plain"]}

def random_fact(lang):
    data = get_json("%s/%s/plain.json" % (SITE, lang))
    if data == None or len(data) == 0:
        return None
    keys = list(data.keys())
    fact = data[keys[random.number(0, len(keys) - 1)]]
    return {"header": header_of(fact.get("title", "DigiFact")), "text": fact.get("content", "")}

def render_fact(header, text, size, lang):
    # Works on every display: 64x32, 64x64 (square) and 128x64 (2x). The DigiByte logo and the DigiFact's number are
    # shown first, then the DigiFact scrolls up under a header. show_full_animation lets Tronbyt play the whole
    # DigiFact, however long it is.
    width, height = canvas.size()
    big = canvas.is2x()
    body_font = FONTS[size][1] if big else FONTS[size][0]
    if lang == "ru" and body_font in NO_CYRILLIC:
        body_font = FONTS["medium"][0]
    header_font = "terminus-12" if big else "tb-8"
    header_height = 13 if big else 8
    line = 2 if big else 1

    delay = 37 if big else 75  # The same speed on every display (128x64 has twice as many pixels)
    intro = intro_card(header, width, height, big, "terminus-16" if big else "tb-8")
    return render.Root(
        delay = delay,
        show_full_animation = True,
        child = render.Sequence(children = [
            render.Animation(children = [intro] * (INTRO_SECONDS * 1000 // delay)),
            render.Column(
                children = [
                    render.Box(
                        width = width,
                        height = header_height,
                        color = DIGIBYTE_BLUE,
                        child = render.Text(header, font = header_font, color = TEXT_COLOR),
                    ),
                    render.Box(width = width, height = line, color = "#000"),
                    render.Marquee(
                        height = height - header_height - line,
                        scroll_direction = "vertical",
                        offset_start = height - header_height - line,
                        child = render.WrappedText(text, font = body_font, color = TEXT_COLOR, width = width),
                    ),
                ],
            ),
        ]),
    )

def get_schema():
    return schema.Schema(
        version = "1",
        fields = [
            schema.Dropdown(
                id = "language",
                name = "Language",
                desc = "The language of the DigiFacts.",
                icon = "language",
                default = "en",
                options = [schema.Option(display = name, value = code) for name, code in LANGUAGES],
            ),
            schema.Dropdown(
                id = "size",
                name = "Text size",
                desc = "The size of the DigiFact text.",
                icon = "textHeight",
                default = "medium",
                options = [
                    schema.Option(display = "Small", value = "small"),
                    schema.Option(display = "Medium", value = "medium"),
                    schema.Option(display = "Large", value = "large"),
                ],
            ),
            schema.Dropdown(
                id = "mode",
                name = "Show",
                desc = "The DigiFact of the day, or a random DigiFact each time.",
                icon = "lightbulb",
                default = "today",
                options = [
                    schema.Option(display = "DigiFact of the day", value = "today"),
                    schema.Option(display = "A random DigiFact", value = "random"),
                ],
            ),
        ],
    )
