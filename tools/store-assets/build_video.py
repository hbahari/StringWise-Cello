"""Assembles the walkthrough video from the clips in video/.

    APP_DIR=/path/to/app python3 build_video.py build      # writes StringWise-Cello-walkthrough.mp4
    APP_DIR=/path/to/app python3 build_video.py preview 5  # one still of scene 5 in build/preview.png

Title card, eight captioned scenes (phone footage beside the caption), end card, and music
made from the app's own "Hear the tune" sound playing pieces from the course.
"""
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import common
import compose as c
from stringwise.audio.tone import SAMPLE_RATE, synthesize_melody
from stringwise.music.pieces import PIECES

HERE = common.HERE
V = os.path.join(HERE, "video"); B = os.path.join(HERE, "build"); os.makedirs(B, exist_ok=True)
W, H, FPS = 1920, 1080, 30
PX, PY, PW, PH, R = 1190, 100, 495, 880, 32
FADE, SCENE, TITLE, END = 0.35, 5.6, 3.0, 3.6
ENC = ["-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS)]
BG = "0x1f130c"
SCENES = [("1-tuner", 0), ("2-lessons", 1), ("3-play-along", 2), ("4-timing", 3), ("5-metronome", 4),
          ("6-take", 5), ("7-fingers", 6), ("8-check", 7)]
MUSIC = ("ode", "andante", "twinkle", "etude", "recital", "ode")


def caption_frame(headline, sub, number):
    """Background, caption and phone surround, with a transparent window for the footage."""
    img = c.background(W, H).convert("RGBA")
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((PX, PY + 16, PX + PW, PY + PH + 16), R, fill=170)
    img.paste(Image.new("RGBA", (W, H), (0, 0, 0, 255)), (0, 0), shadow.filter(ImageFilter.GaussianBlur(26)))
    draw = ImageDraw.Draw(img)
    c.staff_lines(draw, 0, 960, 720, 30)
    draw.text((120, 100), common.APP_NAME, font=ImageFont.truetype(c.HEAD, 46), fill=c.SOFT)
    head, body = ImageFont.truetype(c.HEAD, 100), ImageFont.truetype(c.BODY, 38)
    y = 300
    for line in c.wrap(draw, headline, head, 900):
        draw.text((118, y), line, font=head, fill=c.CREAM); y += 112
    draw.rectangle((122, y + 22, 222, y + 28), fill=c.VARNISH); y += 64
    for line in c.wrap(draw, sub, body, 800):
        draw.text((122, y), line, font=body, fill=c.SOFT); y += 54
    for i in range(8):
        x = 122 + i * 34
        draw.rounded_rectangle((x, 960, x + 22, 966), 3, fill=c.CREAM if i == number else (96, 66, 46))
    hole = Image.new("L", (W, H), 255)
    ImageDraw.Draw(hole).rounded_rectangle((PX, PY, PX + PW - 1, PY + PH - 1), R, fill=0)
    img.putalpha(hole)
    ImageDraw.Draw(img).rounded_rectangle((PX - 2, PY - 2, PX + PW + 1, PY + PH + 1), R + 2,
                                          outline=(104, 72, 50, 255), width=4)
    return img


def card(big, small):
    img = c.background(W, H); draw = ImageDraw.Draw(img)
    c.staff_lines(draw, 0, W, 640, 30)
    font = c.fitted(draw, big, c.HEAD, 190, W - 240)
    draw.text(((W - draw.textlength(big, font=font)) / 2, 300 + (190 - font.size) * 0.6), big, font=font, fill=c.CREAM)
    draw.rectangle((W / 2 - 70, 578, W / 2 + 70, 585), fill=c.VARNISH)
    font = ImageFont.truetype(c.BODY, 46)
    draw.text(((W - draw.textlength(small, font=font)) / 2, 820), small, font=font, fill=c.SOFT)
    return img


def run(args, out):
    part = out.replace(".mp4", ".part.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + args + [part], check=True)
    os.replace(part, out)


def still(png, seconds, out):
    run(["-framerate", str(FPS), "-i", png, "-vf",
         f"format=yuv420p,loop=-1:1,trim=duration={seconds},fade=t=in:st=0:d={FADE}:color={BG},"
         f"fade=t=out:st={seconds - FADE}:d={FADE}:color={BG}"] + ENC, out)


def preview():
    name, i = SCENES[int(sys.argv[2])]
    _, headline, sub, _ = c.SHOTS[i]
    frame = caption_frame(headline, sub, i)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "4.5", "-i", os.path.join(V, name + ".mp4"),
                    "-frames:v", "1", os.path.join(B, "f.png")], check=True)
    base = Image.new("RGBA", (W, H), (31, 19, 12, 255))
    base.paste(Image.open(os.path.join(B, "f.png")).resize((PW, PH), Image.LANCZOS), (PX, PY))
    base.alpha_composite(frame); base.convert("RGB").save(os.path.join(B, "preview.png"))


def build():
    parts = []
    card(common.APP_NAME, common.TAGLINE).save(os.path.join(B, "title.png"))
    still(os.path.join(B, "title.png"), TITLE, os.path.join(B, "s0.mp4")); parts.append("s0.mp4")
    for name, i in SCENES:
        _, headline, sub, _ = c.SHOTS[i]
        overlay = os.path.join(B, f"overlay{i}.png"); caption_frame(headline, sub, i).save(overlay)
        graph = (f"color=c={BG}:s={W}x{H}:r={FPS}:d={SCENE}[base];[0:v]fps={FPS},scale={PW}:{PH}:flags=lanczos[v];"
                 f"[base][v]overlay={PX}:{PY}[a];[a][1:v]overlay=0:0,"
                 f"fade=t=in:st=0:d={FADE}:color={BG},fade=t=out:st={SCENE - FADE}:d={FADE}:color={BG},format=yuv420p")
        run(["-i", os.path.join(V, name + ".mp4"), "-i", overlay, "-filter_complex", graph, "-t", str(SCENE)] + ENC,
            os.path.join(B, f"s{i + 1}.mp4"))
        parts.append(f"s{i + 1}.mp4")
    card(common.APP_NAME, common.FEATURE_LINE.replace("  ", "   ")).save(os.path.join(B, "end.png"))
    still(os.path.join(B, "end.png"), END, os.path.join(B, "s9.mp4")); parts.append("s9.mp4")
    with open(os.path.join(B, "list.txt"), "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    run(["-f", "concat", "-safe", "0", "-i", os.path.join(B, "list.txt"), "-c", "copy"], os.path.join(B, "silent.mp4"))

    total = TITLE + SCENE * len(SCENES) + END
    notes = [n for pid in MUSIC for n in PIECES[pid].notes]
    audio = synthesize_melody(notes, 0.5)[:int(total * SAMPLE_RATE)]
    t = np.arange(len(audio)) / SAMPLE_RATE
    audio = audio * np.minimum(1, t / 1.0) * np.minimum(1, (total - t) / 2.5) * 0.7
    with wave.open(os.path.join(B, "music.wav"), "wb") as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(SAMPLE_RATE)
        out.writeframes((np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes())
    run(["-i", os.path.join(B, "silent.mp4"), "-i", os.path.join(B, "music.wav"), "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-af", "volume=6dB,aecho=0.8:0.6:70|140:0.22|0.12,alimiter=limit=0.9",
         "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart"],
        os.path.join(HERE, common.APP_NAME.replace(" ", "-") + "-walkthrough.mp4"))
    print("built", total, "seconds")


if __name__ == "__main__":
    preview() if sys.argv[1] == "preview" else build()
