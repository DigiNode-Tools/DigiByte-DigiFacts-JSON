"""
Applet: DigiFacts
Summary: Facts about DigiByte
Description: Shows a DigiFact - a bite-size fact about DigiByte - in your language. Choose the DigiFact of the day, or a random DigiFact each time.
Author: saltedlolly
"""

load("encoding/json.star", "json")
load("http.star", "http")
load("images/dgb_icon.png", DGB_ICON = "file")
load("images/dgb_icon@2x.png", DGB_ICON_2X = "file")
load("qrcode.star", "qrcode")
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
QR_SECONDS = 5  # How long the QR code for the DigiFact's link is shown at the end

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
    return render_fact(fact, size, lang)

def get_json(url):
    res = http.get(url = url, ttl_seconds = CACHE_SECONDS)
    if res.status_code != 200:
        return None
    return json.decode(res.body())

def header_of(title):
    # "DigiFact # 22 - Did you know..." -> "DigiFact #22" (short enough for a 64 pixel wide display)
    return title.split(" - ")[0].strip().replace("# ", "#")

def fact_of_the_day(lang):
    data = get_json("%s/%s/today.json" % (SITE, lang))
    if data == None or not data.get("plain"):
        return None
    return {"header": header_of(data.get("title", "DigiFact")), "text": data["plain"], "link": data.get("short_url", "")}

def random_fact(lang):
    data = get_json("%s/%s/plain.json" % (SITE, lang))
    if data == None or len(data) == 0:
        return None
    keys = list(data.keys())
    fact = data[keys[random.number(0, len(keys) - 1)]]
    return {"header": header_of(fact.get("title", "DigiFact")), "text": fact.get("content", ""), "link": fact.get("short_url", "")}

def logo(big):
    # The hand-drawn 18x18 DigiByte logo, or the smoothed 36x36 version for bigger displays
    if big:
        return render.Image(src = DGB_ICON_2X.readall(), width = 36, height = 36)
    return render.Image(src = DGB_ICON.readall(), width = 18, height = 18)

def intro_card(header, width, height, font):
    # The DigiByte logo with the DigiFact's name and number ("DigiFact" above "#22")
    parts = header.rsplit("#", 1)
    name = [
        render.Text(parts[0].strip(), font = font, color = TEXT_COLOR),
        render.Text("#" + parts[1] if len(parts) == 2 else "", font = font, color = TEXT_COLOR),
    ]
    if width == height:
        # Square (64x64): the bigger logo, with the name and number underneath
        layout = render.Column(
            expanded = True,
            main_align = "space_evenly",
            cross_align = "center",
            children = [logo(True), render.Column(cross_align = "center", children = name)],
        )
    else:
        layout = render.Row(
            expanded = True,
            main_align = "space_evenly",
            cross_align = "center",
            children = [logo(canvas.is2x()), render.Column(cross_align = "center", children = name)],
        )
    return render.Box(width = width, height = height, child = layout)

def qr_card(link, width, height):
    # The DigiFact's short link as a QR code (black on white, with a white border so phones can read it)
    big = canvas.is2x()
    code = qrcode.generate(url = link, size = "medium", color = "#000", background = "#fff")
    border = 4 if big else 2
    qr = render.Box(
        width = (50 if big else 25) + 2 * border,
        height = (50 if big else 25) + 2 * border,
        color = "#fff",
        child = render.Image(src = code),
    )
    children = [qr] if width == height else [logo(big), qr]
    return render.Box(
        width = width,
        height = height,
        child = render.Row(expanded = True, main_align = "space_evenly", cross_align = "center", children = children),
    )

def hold(widget, seconds, delay):
    return render.Animation(children = [widget] * (seconds * 1000 // delay))

def render_fact(fact, size, lang):
    # Works on every display: 64x32, 128x64 (2x) and 64x64 (square). The DigiByte logo and the DigiFact's number are
    # shown first. On 64x32 and 128x64 they then scroll up off the display, with the DigiFact following; on 64x64 the
    # DigiFact scrolls up under a header. If the DigiFact has a link, its QR code is shown at the end.
    # show_full_animation lets Tronbyt play the whole DigiFact, however long it is.
    width, height = canvas.size()
    big = canvas.is2x()
    square = width == height
    delay = 37 if big else 75  # The same speed on every display (128x64 has twice as many pixels)

    body_font = FONTS[size][1] if big else FONTS[size][0]
    if lang == "ru" and body_font in NO_CYRILLIC:
        body_font = FONTS["medium"][0]
    title_font = "terminus-16" if big else "tb-8"

    intro = intro_card(fact["header"], width, height, title_font)
    text = render.WrappedText(fact["text"], font = body_font, color = TEXT_COLOR, width = width)

    if square:
        header_height = 8
        body = render.Column(
            children = [
                render.Box(
                    width = width,
                    height = header_height,
                    color = DIGIBYTE_BLUE,
                    child = render.Text(fact["header"], font = "tb-8", color = TEXT_COLOR),
                ),
                render.Box(width = width, height = 1),
                render.Marquee(
                    height = height - header_height - 1,
                    scroll_direction = "vertical",
                    offset_start = height - header_height - 1,
                    child = text,
                ),
            ],
        )
    else:
        # The logo card scrolls up off the display, and the DigiFact follows straight behind it
        body = render.Marquee(
            height = height,
            scroll_direction = "vertical",
            offset_start = 0,
            child = render.Column(children = [intro, text]),
        )

    parts = [hold(intro, INTRO_SECONDS, delay), body]
    if fact.get("link"):
        parts.append(hold(qr_card(fact["link"], width, height), QR_SECONDS, delay))

    return render.Root(delay = delay, show_full_animation = True, child = render.Sequence(children = parts))

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
