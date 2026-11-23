"""Builds the Play Store image set from the captures in raw/phone, raw/tab7 and raw/tab10.

    APP_DIR=/path/to/app python3 compose.py

Writes PlayStoreAssets/ next to this script: phone and tablet screenshots as captured,
1920x1080 landscape images (Chromebook and Android XR) with a caption, and the feature graphic.
"""
import glob
import os
import shutil

import kivy
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import common

HERE = common.HERE
OUT = os.path.join(HERE, "PlayStoreAssets")
HEAD = common.HEAD_FONT
BODY = os.path.join(os.path.dirname(kivy.__file__), "data", "fonts", "Roboto-Regular.ttf")
WOOD, DEEP, CREAM, SOFT, VARNISH = (43, 24, 16), (31, 19, 12), (232, 220, 192), (201, 184, 154), (168, 84, 46)

# (capture name, headline, sub-line, capture shown dimmed behind it).
SHOTS = [
    ("01-tuner", "A tuner that listens", "Play a string and watch the needle. Green means in tune.", "08-finger-check"),
    ("02-lessons", "Twelve weeks, one hour a day", "A full beginner course, with sheet music for every week.", "03-play-along"),
    ("03-play-along", "Sheet music that follows you", "The dot is the note you are playing. Land on the right one and the music moves on.", "02-lessons"),
    ("04-timing-lesson", "Learn to play in time", "A timing lesson every week, with rhythms to clap and play.", "05-metronome"),
    ("05-metronome", "A metronome on every screen", "Start it once and it keeps going while you practice.", "04-timing-lesson"),
    ("06-record-and-check", "Record a take, see what to fix", "Every note marked for pitch, tuning and timing.", "03-play-along"),
    ("07-fingers", "See where each finger goes", "Cello first position, spaced as on a real fingerboard.", "08-finger-check"),
    ("08-finger-check", "Check any finger, live", "Pick a string and a finger. The app tells you if it is in the right place.", "07-fingers"),
]


def raw(device, name):
    return Image.open(glob.glob(os.path.join(HERE, "raw", device, name + "*.png"))[0]).convert("RGB")


def background(w, h):
    """Dark varnished wood with a soft pool of light."""
    img = Image.new("RGB", (w, h), DEEP)
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse((-w * 0.25, -h * 0.5, w * 0.8, h * 1.1), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(w * 0.16))
    img.paste(Image.new("RGB", (w, h), (58, 34, 22)), (0, 0), glow)
    return img


def staff_lines(draw, x0, x1, y, gap, color=(86, 56, 38)):
    for i in range(5):
        draw.line((x0, y + i * gap, x1, y + i * gap), fill=color, width=2)


def wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            lines.append(line); line = word
    return lines + [line]


def fitted(draw, text, path, size, width):
    """The largest font up to ``size`` at which ``text`` fits in ``width``."""
    while size > 20:
        font = ImageFont.truetype(path, size)
        if draw.textlength(text, font=font) <= width:
            return font
        size -= 2
    return ImageFont.truetype(path, size)


def phone(shot, width, radius=30, dim=1.0):
    """A screenshot with rounded corners, a thin rim and a drop shadow, on transparency."""
    height = round(shot.height * width / shot.width)
    screen = shot.resize((width, height), Image.LANCZOS)
    if dim < 1.0:
        screen = Image.blend(Image.new("RGB", screen.size, DEEP), screen, dim)
    pad = 60
    canvas = Image.new("RGBA", (width + pad * 2, height + pad * 2), (0, 0, 0, 0))
    shadow = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(shadow).rounded_rectangle((pad, pad + 14, pad + width, pad + height + 14), radius, fill=150)
    canvas.paste(Image.new("RGBA", canvas.size, (0, 0, 0, 255)), (0, 0), shadow.filter(ImageFilter.GaussianBlur(22)))
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius, fill=255)
    canvas.paste(screen, (pad, pad), mask)
    ImageDraw.Draw(canvas).rounded_rectangle((pad, pad, pad + width - 1, pad + height - 1), radius,
                                             outline=(92, 62, 42, 255), width=3)
    return canvas, pad


def landscape(name, headline, sub, companion):
    w, h = 1920, 1080
    img = background(w, h)
    draw = ImageDraw.Draw(img)
    staff_lines(draw, 0, 900, 700, 30)
    draw.text((110, 96), common.APP_NAME, font=ImageFont.truetype(HEAD, 46), fill=SOFT)
    head_font, sub_font = ImageFont.truetype(HEAD, 96), ImageFont.truetype(BODY, 36)
    y = 300
    for line in wrap(draw, headline, head_font, 800):
        draw.text((108, y), line, font=head_font, fill=CREAM); y += 108
    draw.rectangle((112, y + 22, 212, y + 28), fill=VARNISH)
    y += 62
    for line in wrap(draw, sub, sub_font, 720):
        draw.text((112, y), line, font=sub_font, fill=SOFT); y += 52
    back, pad = phone(raw("phone", companion), 400, dim=0.62)
    img.paste(back, (1440 - pad, 250 - pad), back)
    front, pad = phone(raw("phone", name), 500)
    img.paste(front, (985 - pad, 96 - pad), front)
    return img


def feature_graphic():
    w, h = 1024, 500
    img = background(w, h)
    draw = ImageDraw.Draw(img)
    staff_lines(draw, 0, 560, 330, 17)
    # "StringWise Cello" is longer than "StringWise": shrink it to stay clear of the phones.
    title = fitted(draw, common.APP_NAME, HEAD, 104, 500)
    top = 120 + (104 - title.size) * 0.6
    draw.text((70, top), common.APP_NAME, font=title, fill=CREAM)
    draw.rectangle((74, 250, 150, 255), fill=VARNISH)
    draw.text((74, 276), common.TAGLINE, font=ImageFont.truetype(BODY, 29), fill=CREAM)
    draw.text((74, 426), common.FEATURE_LINE, font=ImageFont.truetype(BODY, 21), fill=SOFT)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for name, width, x, y, angle, dim in (("03-play-along", 250, 790, 80, -6, 0.7), ("01-tuner", 290, 590, 40, 5, 1.0)):
        card, pad = phone(raw("phone", name), width, radius=22, dim=dim)
        card = card.rotate(angle, resample=Image.BICUBIC, expand=True)
        layer.paste(card, (x - pad, y - pad), card)
    img.paste(layer, (0, 0), layer)
    return img


def app_icon(inset=34):
    """512 x 512 store icon. Play rounds the corners itself, so the artwork fills the square:
    the launcher icon's own rounded corners are cropped off and the rest scaled back up."""
    icon = Image.open(os.path.join(common.APP_DIR, "stringwise", "assets", "images", "icon.png")).convert("RGBA")
    icon = icon.resize((512, 512), Image.LANCZOS)
    return icon.crop((inset, inset, 512 - inset, 512 - inset)).resize((512, 512), Image.LANCZOS)


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    for folder, device in (("phone-screenshots", "phone"), ("tablet-7in-screenshots", "tab7"),
                           ("tablet-10in-screenshots", "tab10")):
        os.makedirs(os.path.join(OUT, folder))
        for name, *_ in SHOTS:
            raw(device, name).save(os.path.join(OUT, folder, name + ".png"), optimize=True)
    for folder in ("desktop-screenshots", "android-xr-screenshots"):
        os.makedirs(os.path.join(OUT, folder))
    for name, headline, sub, companion in SHOTS:
        picture = landscape(name, headline, sub, companion)
        for folder in ("desktop-screenshots", "android-xr-screenshots"):
            picture.save(os.path.join(OUT, folder, name + ".png"), optimize=True)
    os.makedirs(os.path.join(OUT, "feature-graphic"))
    feature_graphic().save(os.path.join(OUT, "feature-graphic", "feature-graphic-1024x500.png"), optimize=True)
    app_icon().save(os.path.join(OUT, "app-icon-512.png"), optimize=True)
    print("done")


if __name__ == "__main__":
    main()
