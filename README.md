# StringWise Cello

A cello tutor for beginners, written in Python with [Kivy](https://kivy.org) and
packaged for Android with Buildozer.

- **Tuner** that listens through the microphone
- **Lessons**: a 12-week course planned for an hour of practice a day, with two pieces of sheet music and a timing lesson each week
- **Metronome** on its own tab, with tap tempo, eighth-note clicks and drop-out bars. It keeps running across tabs
- **Record and Check**: records a take with the click, then marks each note for pitch, tuning and timing
- **Play-Along**: follows the sheet music as you play and shows the note it hears on the staff
- **Fingers**: a cello first-position map with real string spacing, and a live check for any finger
- **Settings** behind the gear icon: tuning pitch (A = 440 to 443), feedback email, rate on Play, reset progress
- **Theory**, and a **Practice** tab with a rhythm of the day, a tempo ladder and a daily checklist

Sheet music is in the bass clef. The app works offline. Its only permission is the microphone, and audio is analysed on the device.

## Project layout

```
main.py                     entry point
buildozer.spec              Android build settings
stringwise/
  app.py                    title bar, navigation, screen switching
  theme.py                  colours and fonts
  storage.py                saved progress (JSON)
  audio/                    pitch detection (YIN), microphone, reference tones, metronome
  music/                    notes, fingering, the 22 practice pieces, rhythm studies
  logic/                    tuner, finger check, play-along and take-checking rules (no UI code)
  content/                  all lesson, theory and practice text
  ui/                       widgets: dial, sheet music, fingerboard
  ui/screens/               one file per screen
  assets/                   fonts, icon, optional photos
tests/                      pytest suite for audio, music, content and logic
```

To change wording, edit the files in `stringwise/content/`. To add a piece, add it to
`stringwise/music/pieces.py`; the tests check that every bar adds up and every note is reachable.

## Run it on a computer

```
pip install -r requirements.txt
python main.py
python -m pytest tests
```

No cello to hand? `STRINGWISE_FAKE_MIC="147,165,185" python main.py` feeds the app D, E and F♯
on the D string, one a second.

## Build for Android with GitHub Actions

1. Push this folder to a GitHub repository.
2. Open the **Actions** tab, choose **Build Android**, and press **Run workflow**.
3. When it finishes, download the **stringwise-cello-android** artifact. It contains a debug
   `.apk` you can install on your phone, and the signed `.aab` for Google Play if the
   signing secrets below are set.

The first build takes 30 to 40 minutes. Later builds reuse the cached toolchain.

### Signing secrets

StringWise Cello is a separate app on Google Play, so it gets its own upload key. Do not
reuse the violin app's key. Make one once with Java's `keytool` and keep it somewhere safe,
because every later update must be signed with it:

```
keytool -genkeypair -v -keystore stringwise-cello-upload.jks -alias upload \
  -keyalg RSA -keysize 2048 -validity 10000
```

Add four repository secrets under **Settings > Secrets and variables > Actions**:

| Secret | Value |
| --- | --- |
| `ANDROID_KEYSTORE_BASE64` | the keystore file, base64 encoded (`base64 -w0 stringwise-cello-upload.jks`) |
| `ANDROID_KEYSTORE_PASSWORD` | the keystore password |
| `ANDROID_KEY_ALIAS` | the key alias |
| `ANDROID_KEY_PASSWORD` | the key password |

Never commit the keystore itself. `.gitignore` already excludes `*.keystore` and `*.jks`.

### Before each upload

In `buildozer.spec`, raise `android.numeric_version` by at least 1 and update `version`.
The package id, `golemapps.stringwisecello`, must stay as it is: it is the id registered for the app in Play Console.

## Photos of hand positions

The Fingers screen shows photos above each checklist when these files exist in
`stringwise/assets/photos/`:

- Left hand: `hand-frame-front.jpg`, `hand-frame-side.jpg`, `thumb.jpg`, `place-1234.jpg`
- Bow hold: `bow-hold-side.jpg`, `bow-hold-top.jpg`, `bow-hold-end.jpg`

Landscape, about 1200 px wide.

## Testing feedback

`docs/TESTING_FEEDBACK.md` is a running, plain-language log of feedback since version 1.0.0
and the change made for each item.

## Credits

Headings are set in Crimson Text (SIL Open Font License, see `stringwise/assets/fonts/`).
Traditional tunes are simplified arrangements; the other studies were written for this course.

## Store assets

`tools/store-assets/` makes the whole Google Play graphics set by running the real app
headless and feeding it simulated playing: feature graphic, 512 px icon, eight screenshots
each for phone, 7-inch and 10-inch tablet, Chromebook and Android XR, and a ~51 s
walkthrough video with music from the app's own pieces. It needs Linux with xvfb, ffmpeg,
Kivy, numpy and Pillow.

```
cd tools/store-assets
xvfb-run -a -s "-screen 0 1700x2900x24" python3 stills.py 1080 1920 3 raw/phone
xvfb-run -a -s "-screen 0 1700x2900x24" python3 stills.py 1200 2132 2 raw/tab7
xvfb-run -a -s "-screen 0 1700x2900x24" python3 stills.py 1600 2844 2 raw/tab10
python3 compose.py
xvfb-run -a -s "-screen 0 1300x1400x24" python3 film.py
python3 build_video.py build
```

The listing text is in `docs/STORE_LISTING.md`.
