"""The Theory tab: short reference sections a beginner can dip into.

Each section is a list of blocks. A block is a tuple whose first item says how
to draw it: "p" paragraph, "h" small heading, "list" bullet list, "terms" a
two-column glossary, "open_strings" the staff diagram of the four open strings.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Section:
    id: str
    title: str
    summary: str
    blocks: tuple[tuple, ...]


THEORY_INTRO = "The reading and vocabulary used in the lessons. Tap a heading to open it."

SECTIONS: tuple[Section, ...] = (
    Section(
        "staff", "Reading the staff", "Lines, spaces, ledger lines, sharps and flats",
        (
            ("p", "Cello music is written on a staff of five lines with a bass clef at the "
                  "start. The bass clef's two dots sit either side of the F line, which is how "
                  "it got its other name, the F clef. Notes sit on the lines and in the spaces "
                  "between them. The higher a note is on the staff, the higher it sounds."),
            ("p", "From the bottom line up, the lines are G, B, D, F and A. The spaces are A, C, "
                  "E and G. Put together they run straight through the musical alphabet: "
                  "G, A, B, C, D, E, F, G, A."),
            ("open_strings",),
            ("p", "These are your four open strings. C is below the staff, under two short "
                  "extra lines. G sits on the bottom line, D on the middle line and A on the "
                  "top line."),
            ("h", "Ledger lines"),
            ("p", "When a note is too low or too high for the staff, it gets short lines of its "
                  "own, called ledger lines. Your open C needs two. The C♯ on the A string, "
                  "which you play with finger 3, sits on one ledger line above the staff, and "
                  "the D above it, finger 4, sits just over that line."),
            ("p", "Much later, cello music climbs high enough to switch to the tenor or treble "
                  "clef. Everything in this course stays in the bass clef."),
            ("h", "Sharps, flats and naturals"),
            ("list", (
                "A sharp (♯) raises a note by a half step.",
                "A flat (♭) lowers it by a half step.",
                "A natural (♮) cancels a sharp or flat.",
            )),
            ("p", "A sharp or flat written next to a note lasts until the end of that bar. The "
                  "sheet music in this app writes the sharp beside every note that needs one, so "
                  "you never have to remember it."),
            ("h", "Ties and slurs"),
            ("p", "Both are curved lines. A tie joins two notes of the same pitch into one "
                  "longer note. A slur covers notes of different pitches and tells you to play "
                  "them in a single bow."),
        ),
    ),
    Section(
        "keys", "Key signatures", "Why some music starts with sharps",
        (
            ("p", "Many pieces use the same sharps from start to finish. Rather than mark each "
                  "one, the composer writes them once at the beginning of every line, just after "
                  "the clef. That group of sharps or flats is the key signature, and it applies "
                  "to every note with that letter name, in any octave."),
            ("terms", (
                ("C major", "No sharps or flats."),
                ("G major", "One sharp: F♯."),
                ("D major", "Two sharps: F♯ and C♯."),
            )),
            ("p", "Your finger pattern of open, 1, 3 and 4 already plays in these keys. On the C "
                  "and G strings it gives you C major. On the G and D strings it gives you G "
                  "major, and on the D and A strings, D major."),
            ("p", "A natural sign in front of a note cancels the key signature for the rest of "
                  "that bar."),
        ),
    ),
    Section(
        "rhythm", "Rhythm and time signatures", "Note lengths, rests, dots and counting",
        (
            ("h", "Note lengths"),
            ("terms", (
                ("Whole note", "Four beats. An open oval with no stem."),
                ("Half note", "Two beats. An open oval with a stem."),
                ("Quarter note", "One beat. A filled note with a stem."),
                ("Eighth note", "Half a beat. A filled note with a flag, or joined to its neighbor by a beam."),
            )),
            ("p", "Those counts assume the quarter note gets the beat, which is true of every "
                  "piece in this app."),
            ("h", "Rests"),
            ("p", "A rest is a silence with a length. There is one to match each note value. "
                  "Keep counting through a rest exactly as you would through a note. Coming back "
                  "in early is the usual mistake."),
            ("h", "Dotted notes"),
            ("p", "A dot after a note makes it half as long again. A dotted half note lasts "
                  "three beats. A dotted quarter lasts one and a half, and is usually followed "
                  "by an eighth note to make up two full beats."),
            ("h", "Time signatures"),
            ("p", "The two numbers at the start of a piece are the time signature. The top "
                  "number is how many beats are in each bar. The bottom number is the kind of "
                  "note that gets one beat, and 4 means a quarter note. So 4/4 is four "
                  "quarter-note beats to a bar, and 3/4 is three, which is the feel of a waltz. "
                  "Every piece in this app is in 4/4."),
            ("h", "Counting"),
            ("p", "For quarter notes in 4/4, count \"1, 2, 3, 4\" at an even pace. For eighth "
                  "notes, fit an \"and\" between the numbers: \"1 and 2 and 3 and 4 and\". Clap "
                  "a new rhythm while counting aloud before you play it. Sorting out the rhythm "
                  "first leaves you free to think about the notes."),
            ("h", "Using a metronome"),
            ("p", "A metronome clicks a steady beat. Its number is beats a minute, so 60 is one "
                  "click a second and 120 is two. The app's metronome has its own tab, Metro, "
                  "and each lesson has a timing study that uses it."),
            ("p", "Start slower than you think you need. When your note lands exactly on a "
                  "click, the click seems to disappear. If you can still hear it clearly, you "
                  "are early or late."),
        ),
    ),
    Section(
        "bowing", "Bowing words", "Parts of the bow, directions and strokes",
        (
            ("h", "Parts of the bow"),
            ("p", "You hold the bow at the frog, the block at the heavy end. The far end is the "
                  "tip. A cello bow is shorter, heavier and thicker than a violin bow. The hair is what touches the string. The screw at the end of the frog "
                  "tightens the hair before you play and loosens it afterwards. Always loosen "
                  "it before the bow goes back in the case."),
            ("h", "Direction"),
            ("terms", (
                ("Down-bow", "Starts at the frog and moves toward the tip. Marked with a square bracket above the note."),
                ("Up-bow", "Starts toward the tip and moves back to the frog. Marked with a V."),
            )),
            ("h", "Strokes and styles"),
            ("terms", (
                ("Arco", "Play with the bow. This is the default."),
                ("Pizzicato (pizz.)", "Pluck the string with your right index finger."),
                ("Détaché", "One smooth bow per note, changing direction without a gap."),
                ("Legato", "Smooth and connected, often several notes in one bow."),
                ("Staccato", "Short notes with a clear stop between them. Marked with a dot above or below the note."),
                ("Tenuto", "Hold the note for its full length. Marked with a short line."),
            )),
        ),
    ),
    Section(
        "dynamics", "Dynamics and tempo", "How loud and how fast",
        (
            ("h", "Dynamics"),
            ("terms", (
                ("pp (pianissimo)", "Very soft."),
                ("p (piano)", "Soft."),
                ("mp (mezzo piano)", "Fairly soft."),
                ("mf (mezzo forte)", "Fairly loud."),
                ("f (forte)", "Loud."),
                ("ff (fortissimo)", "Very loud."),
                ("Crescendo (cresc.)", "Get louder little by little. Drawn as a long wedge that opens to the right."),
                ("Diminuendo (dim.)", "Get softer little by little. The wedge closes to the right. Also called decrescendo."),
            )),
            ("h", "Tempo"),
            ("p", "Tempo words are Italian and describe the speed and character of a piece."),
            ("terms", (
                ("Largo", "Very slow and broad."),
                ("Adagio", "Slow."),
                ("Andante", "Walking pace."),
                ("Moderato", "Medium."),
                ("Allegro", "Fast and lively."),
                ("Presto", "Very fast."),
                ("Ritardando (rit.)", "Slow down gradually."),
                ("Accelerando (accel.)", "Speed up gradually."),
            )),
            ("p", "A metronome marking such as ♩ = 60 gives the exact speed: 60 quarter-note "
                  "beats a minute, one each second."),
        ),
    ),
    Section(
        "fingers", "Finger numbers", "How cellists count fingers, and what comes later",
        (
            ("p", "Cellists number the fingers of the left hand from the index finger. The "
                  "thumb has no number until much later, when it is marked with a special sign "
                  "for thumb position. Pianists count the thumb as 1, so if you have played "
                  "piano, expect to be confused for a week."),
            ("list", (
                "1 is the index finger.",
                "2 is the middle finger.",
                "3 is the ring finger.",
                "4 is the little finger.",
                "0 means an open string, with no finger down.",
            )),
            ("p", "A small number printed above a note tells you which finger to use. In first "
                  "position on the cello each finger covers one half step, so the hand spans "
                  "four half steps from finger 1 to finger 4. In the keys this course uses, "
                  "finger 2 has no note of its own. It rests on the string between 1 and 3, "
                  "ready for notes like F on the D string or C on the A string."),
            ("p", "Unlike the violin, finger 4 can't reach the next open string's note in first "
                  "position. Finger 4 on one string is a whole step short of the next open "
                  "string, and the open string fills the gap."),
            ("h", "What comes later"),
            ("p", "The next step for most cellists is extensions: finger 1 stretches back a half "
                  "step, or the hand opens forward so there is a whole step between fingers 1 "
                  "and 2. That reaches notes such as B♭ on the A string and C♯ on the G string. "
                  "After that comes shifting, where the whole hand moves up the neck to reach "
                  "higher notes. The first stop is usually fourth position, and thumb position "
                  "comes much later."),
        ),
    ),
    Section(
        "tuning", "How the cello is tuned", "Fifths, fine tuners and pegs",
        (
            ("p", "From lowest to highest the strings are C, G, D and A. They are an octave "
                  "below a viola's strings, and the top three share their names with the "
                  "violin's bottom three. Each string is a "
                  "perfect fifth above the one before it. A fifth is the distance from the first "
                  "note of a scale to the fifth, like the jump at the start of Twinkle, Twinkle, "
                  "Little Star."),
            ("h", "Concert pitch"),
            ("p", "The A string is tuned to 440 vibrations per second, written 440 Hz. This is "
                  "the standard almost everywhere, and it is what the Tuner tab uses. Some "
                  "orchestras tune a shade higher, to 442 or 443."),
            ("h", "Fine tuners and pegs"),
            ("p", "The small screws on the tailpiece are fine tuners. Many student cellos have "
                  "one for every string; others have one only on the A string. Turning one "
                  "clockwise raises the pitch slightly. Use them for everyday tuning. The wooden pegs in "
                  "the scroll make big changes with a small turn. Use a peg only when a string "
                  "is far out, or when a fine tuner has been screwed all the way down."),
            ("p", "If you have to use a peg, loosen it slightly first, then turn it up toward "
                  "the note while pressing it gently into the pegbox so it holds. Go a little at "
                  "a time. Strings break when they are tightened too far, and the A string "
                  "breaks most easily. Cello pegs are large and can slip, so keep a hand on the "
                  "scroll. If you are unsure, ask a teacher or a string shop to show you once."),
            ("h", "Tuning by ear"),
            ("p", "Play two neighboring strings together. If they are close but not quite a "
                  "fifth, you will hear a slow wobble in the sound. As you adjust one string the "
                  "wobble slows down, and when the fifth is in tune it stops and the two notes "
                  "ring as one."),
        ),
    ),
    Section(
        "ear", "Training your ear", "Habits that improve tuning and timing",
        (
            ("p", "Your fingers go where your ear tells them. The clearer the note is in your "
                  "head, the more often you will land on it."),
            ("list", (
                "Sing or hum a note before you play it. If you can sing it, you know what you are aiming for.",
                "Tap a note on the Fingers tab, listen, then try to match it on your cello.",
                "Use Hear the tune in Play-Along before you learn a new piece.",
                "Record yourself once or twice a week. Problems you miss while playing are obvious on a recording.",
                "When a note sounds wrong, work out whether it is too high or too low before you move your finger.",
            )),
        ),
    ),
)
