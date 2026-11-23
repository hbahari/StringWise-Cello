# StringWise Cello: testing feedback and what changed

A running log of feedback on StringWise Cello since version 1.0.0, in plain language, with
the change made in response. Newest entries are at the bottom of each section, and new
sections are added as testing continues.

StringWise Cello is built from StringWise (violin) and shares its screens and features.
Everything changed in the violin app up to version 2.4.0 was already in StringWise Cello
1.0.0; that history is in the violin app's own log.

**Where the feedback came from**

- **Closed test**: reported by testers during the Google Play closed test.
- **Device testing**: found by the developer while testing builds on a phone and a computer.
- **Play Console**: raised by Google Play's own checks on an uploaded build.
- **From StringWise (violin)**: reported on the violin app and fixed in both, because the
  two apps share the same screens.

Keeping these apart matters when answering Google's questions about tester feedback.

---

## 21 November 2026 (version 1.0.0)

| Feedback | Source | What changed |
| --- | --- | --- |
| StringWise only teaches the violin, so there was nothing for beginner cellists. | Device testing | Made StringWise Cello, a separate app with the same tuner, metronome, lessons, Play-Along, Record and Check, Fingers, Theory, Practice and Settings, rewritten for the cello. |
| The tuner listened only from the violin's open G (196 Hz) upwards, so it could not hear the cello's C and G strings. | Device testing | Pitch detection now reaches down to 56 Hz, below the open C (65.4 Hz). It names the C and G strings in the right octave even when a phone microphone barely picks up the lowest part of the sound. |
| Record and Check ignored every note below 150 Hz, so most cello notes came back as missed. | Device testing | Record and Check now uses the same range as the tuner. |
| The finger map, the finger check and the lesson text used the violin's finger spacing. | Device testing | Everything follows cello first position: a whole step from the open string to finger 1, then a half step from each finger to the next. The fingerboard is labelled half, half, half, and finger 2 on the C and G strings is named E♭ and B♭, as cellists call those notes. |
| Cello music is written in the bass clef, but the sheet music used the treble clef. | Device testing | All sheet music, the open-strings diagram and the Theory section on reading the staff now use the bass clef. |
| The violin pieces would not fit the cello's strings or its first position. | Device testing | Every piece and rhythm moved down an octave and a fifth, so each violin string lands on the matching cello string and every note can be played without shifting. The scale, études and arpeggio are in G major. Weeks 3 and 4 swapped a piece each so finger 4 still arrives in week 4. |
| Posture, bow hold, left hand and bow arm advice was written for the violin. | Device testing | Rewritten for the cello: sitting, setting the endpin, the cello bow hold, the left-hand frame, and how the bow arm rises for the A string and drops for the C string. The fourth-finger check is now listening for the open string below to ring along. |
| Two apps with the same icon would be hard to tell apart on one phone. | Device testing | The icon and opening screen say CELLO under the S, and the title bar reads StringWise Cello. |

## 23 November 2026 (version 1.1.0)

Brought over from StringWise (violin) 2.5.0, which made these changes after the Testers
Community report of 22 November 2026.

| Feedback | Source | What changed |
| --- | --- | --- |
| New users get no guided introduction to the app's features. | From StringWise (violin) | Added a short tour that runs the first time the app opens. It dims the screen, highlights one part at a time (tuner, metronome, lessons, finger map, theory, practice and settings) and explains it in a bubble, with Skip and Next buttons. It can be watched again from Settings. |
| There is no easy way to share the app with friends. | From StringWise (violin) | Added Share StringWise Cello to Settings. It opens the phone's share menu with a short message and the Google Play link. |
| There is no button to rate the app. | From StringWise (violin) | Already in version 1.0.0: Rate StringWise Cello on Google Play, in Settings. |
| The store description is short and lacks search keywords. | From StringWise (violin) | A full store listing with a feature list and natural search keywords was written for the first StringWise Cello listing (see version 1.1.1). |
| Let users send feedback from inside the app. | From StringWise (violin) | Already in version 1.0.0: Send feedback, in Settings. |
| Works well offline. | From StringWise (violin) | The app needs no internet connection for anything except the feedback, rate and share links. |
| Add new lessons and pieces over time, rewards for finishing lessons, and a community area. | From StringWise (violin) | Noted for later versions. Not in this release. |

## 23 November 2026 (version 1.1.1)

| Feedback | Source | What changed |
| --- | --- | --- |
| On a standard-width phone the title "StringWise Cello" did not fit beside the metronome control and wrapped onto two lines, but stayed on one line on wider phones. | Device testing | The title bar now always shows "StringWise" with a smaller "Cello" underneath, sized to fit the bar on every phone. Found while making the store screenshots. |
| Play Console rejected the app bundle: the app was registered as golemapps.stringwisecello, but the build was named golemapps.stringwisecello.app. | Play Console | The build now uses golemapps.stringwisecello, matching Play Console. The Share button's store link uses the same id. |
| The app had no store listing or store graphics. | Device testing | Wrote the Google Play listing (docs/STORE_LISTING.md) and made the feature graphic, store icon, screenshots for phone, tablets, Chromebook and Android XR, and a walkthrough video, all from the running app. |

---

## Still to do

- Check the tuner, the finger check and Record and Check with a real cello on several
  phones, especially the C string.
- Check the tour and the share menu on a real phone.
- Photos of real cello hand positions for the Fingers tab.
