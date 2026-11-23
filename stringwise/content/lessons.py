"""The twelve-week course. One lesson a week, planned for an hour of practice a day."""

from __future__ import annotations

from dataclasses import dataclass, replace

from .timing import TIMING, TimingStudy


@dataclass(frozen=True)
class PlanItem:
    minutes: int
    title: str
    text: str


@dataclass(frozen=True)
class Lesson:
    week: int
    title: str
    goals: tuple[str, ...]
    body: tuple[str, ...]
    plan: tuple[PlanItem, ...]
    pieces: tuple[str, ...] = ()
    timing: TimingStudy | None = None

    @property
    def total_minutes(self) -> int:
        return sum(item.minutes for item in self.plan)


def _plan(*items: tuple[int, str, str]) -> tuple[PlanItem, ...]:
    return tuple(PlanItem(*item) for item in items)


LESSONS: tuple[Lesson, ...] = (
    Lesson(
        week=1,
        title="Meeting the instrument",
        goals=(
            "Sit with the cello resting against you, balanced without the left hand",
            "Hold the bow with a loose, rounded hand",
            "Get a clear sound from each of the four open strings",
        ),
        body=(
            "Nothing this week involves reading music or pressing a string down. The job is to "
            "get comfortable sitting with the cello and holding the bow, because tension you "
            "learn now is hard to unlearn later.",
            "Sit near the front edge of a chair with no arms, feet flat on the floor and knees "
            "a little lower than your hips. Pull out the endpin so that, with the cello resting "
            "against your chest, the C string peg sits near your left ear and the neck is just "
            "clear of your shoulder. Your knees touch the sides of the cello lightly to keep it "
            "from turning. Put a rock stop or strap under the endpin so it can't slide.",
            "For the bow, bend your thumb and rest its tip on the stick where it meets the "
            "frog, across from your middle finger. Let all four fingers drape over the stick, "
            "with your little finger resting on top of it rather than perched on its tip. Your "
            "hand should hang from the bow, heavy and loose. If your knuckles turn white, shake "
            "your hand out and start again.",
            "Pluck the open strings first, from low to high: C, G, D, A. Plucking is called "
            "pizzicato. Once the strings are familiar, try short, slow bow strokes on the G and "
            "D strings, which are the easiest to reach.",
        ),
        plan=_plan(
            (10, "Posture check", "Sit, set the endpin, settle the cello against your chest, drop your shoulders. Use a mirror if you have one."),
            (10, "Plucked open strings", "Pluck each string four times, slowly. Say its name as you go."),
            (15, "Bow hold and first strokes", "Set the bow hold with the bow in the air, then play short, slow strokes on G and D."),
            (10, "Tuner", "Open the Tuner tab and check all four strings. Get used to the sound of a string that is in tune."),
            (5, "Rest", "Stand up, stretch, and shake out your hands and shoulders."),
        ),
    ),
    Lesson(
        week=2,
        title="Full bows and steady tone",
        pieces=("openwarmup", "crossings"),
        goals=(
            "Draw a whole bow, frog to tip, on every string",
            "Keep the sound even from one end of the bow to the other",
            "Know a down-bow from an up-bow",
        ),
        body=(
            "No new notes this week. All of the work is in the right arm.",
            "A down-bow starts at the frog and travels to the tip, pulling away from you to the "
            "right. An up-bow pushes back. For a clean sound the bow has to stay parallel to the "
            "bridge the whole way, about halfway between the bridge and the end of the "
            "fingerboard. Near the tip the bow tends to slide toward the fingerboard, so watch "
            "yourself in a mirror or film a few strokes on your phone.",
            "Let the weight of your arm sink into the string through the bow. If the sound "
            "crunches, you are pressing too hard for how slowly the bow is moving. If it sounds "
            "thin or airy, let more weight in. In both cases the fix comes from the arm. "
            "Squeezing with the fingers only makes it worse.",
        ),
        plan=_plan(
            (10, "Warm-up", "Pluck the open strings, then play a few slow bows to loosen up."),
            (15, "Whole bows", "Four slow down-bows and up-bows on each string. Count to four on each stroke."),
            (15, "String crossings", "Play Open String Crossings below. Your right elbow rises for the higher strings and drops for the lower ones."),
            (5, "Tuner", "Check all four strings again. New strings drift a lot in the first weeks."),
            (5, "Listen", "One slow bow on each string. Is the sound the same at the frog, the middle and the tip?"),
        ),
    ),
    Lesson(
        week=3,
        title="The first finger pattern",
        pieces=("firstpattern", "hotcrossbuns"),
        goals=(
            "Place fingers 1 and 3 on the D string",
            "Play each note in tune, checking with the app",
            "Keep the left hand rounded and loose",
        ),
        body=(
            "The left hand starts work this week. On the D string, finger 1 (index) plays E and "
            "finger 3 (ring) plays F♯. The Fingers tab shows where each one lands.",
            "On the cello the fingers are spaced a half step apart, one finger for each half "
            "step. From the open string to finger 1 is a whole step. From finger 1 to finger 3 "
            "is another whole step, with finger 2 in the middle. When you play finger 3, put "
            "fingers 1 and 2 down behind it as well. They hold the hand open at the right width.",
            "Shape your hand as if it were wrapped around a soft drink can, with the fingers "
            "curved and coming down on their tips, square across the string. Your thumb rests "
            "behind the neck, roughly opposite finger 2, without squeezing. Your left elbow "
            "stays up and out to the side, so the arm makes a gentle curve rather than hanging.",
        ),
        plan=_plan(
            (10, "Warm-up bows", "Whole bows on all four open strings."),
            (15, "Finger drill, plucked", "D string. Put finger 1 down, pluck, and check the note with the live checker on the Fingers tab. Then put fingers 1, 2 and 3 down together and check finger 3."),
            (10, "Same drill with the bow", "One slow bow for each note: open, 1, 3 and back down."),
            (10, "This week's pieces", "Play First Pattern Warm-Up, then Hot Cross Buns."),
            (5, "Rest", "Shake out your left hand. Sore fingertips are normal this week."),
        ),
    ),
    Lesson(
        week=4,
        title="Adding the fourth finger",
        pieces=("skips", "ode"),
        goals=(
            "Add finger 4 on the D string",
            "Match finger 4 to the open G string, an octave apart",
            "Play a whole tune from start to finish",
        ),
        body=(
            "Your little finger is finger 4. On the D string it plays G, one octave above the "
            "open G string next door. That gives you a built-in test: when finger 4 is exactly "
            "in tune, the open G string starts to ring along with it on its own, and the note "
            "sounds fuller. Play finger 4 and listen for that ring.",
            "Finger 4 sits a half step past finger 3. It is the weakest finger, so keep it "
            "curved and let the weight of the arm press it down rather than squeezing. Keep "
            "fingers 1, 2 and 3 down behind it.",
            "There are two tunes this week. Steps and Skips stays on the D string. Ode to Joy "
            "uses all your fingers and the open A string for its top note.",
        ),
        plan=_plan(
            (10, "Warm-up", "Open strings, then last week's pattern: open, 1, 3 on the D string."),
            (10, "Finger 4", "Play finger 3, then finger 4. Adjust finger 4 until the open G string rings along with it."),
            (15, "Steps and Skips", "Learn it one bar at a time from the music below, then join the bars together."),
            (10, "Ode to Joy", "Start it once Steps and Skips is steady. The first two bars are enough for today."),
            (5, "Play through", "Play one tune from beginning to end without stopping, wrong notes and all."),
        ),
    ),
    Lesson(
        week=5,
        title="The G string",
        pieces=("mary", "twinkle"),
        goals=(
            "Use the same finger pattern on the G string",
            "Play tunes that cross between the G and D strings",
            "Cross strings without a bump in the sound",
        ),
        body=(
            "The finger pattern you learned on the D string works on every string. On the G "
            "string the open note is G, finger 1 plays A, finger 3 plays B and finger 4 plays "
            "C. Every finger is still a half step from the next.",
            "To get there, keep the shape of your hand and raise your left elbow a little, "
            "which carries the fingers over to the lower string. Your bow arm moves too: the "
            "right elbow sits a little lower for the G string than for the D.",
            "Mary Had a Little Lamb stays on the G string except for two open D notes. Twinkle "
            "crosses back and forth more often and uses finger 1 on the D string.",
        ),
        plan=_plan(
            (10, "Warm-up", "Open strings, then the D string pattern from memory."),
            (10, "G string pattern", "Open, 1, 3, 4 on the G string, checking each note with the live checker. When finger 4 is in tune, the open C string rings along."),
            (15, "Mary Had a Little Lamb", "One bar at a time, then the whole tune."),
            (10, "Twinkle", "Watch the jump from open G to open D at the start. Move the bow to the new string before you play it."),
            (5, "Play through", "One slow run of whichever tune is going better."),
        ),
    ),
    Lesson(
        week=6,
        title="The C and A strings",
        pieces=("auclair", "lightlyrow"),
        goals=(
            "Play the finger pattern on the C and A strings",
            "Reach the C string without the bow touching the G string",
            "Know the name of every note you can now play",
        ),
        body=(
            "Two strings to go. On the C string the notes are C, D, E and F. On the A string "
            "they are A, B, C♯ and D. The spacing under your fingers is the same as before.",
            "The C string is the thickest and the slowest to speak. Give it a slower bow with "
            "plenty of arm weight, and drop your right elbow so the bow clears the G string. "
            "The A string is the opposite. It needs less weight, and your right elbow comes up "
            "so the bow clears the D string.",
            "Au Clair de la Lune sits entirely on the C string. Lightly Row is on the D string "
            "and reaches up to the open A for its top note.",
        ),
        plan=_plan(
            (10, "Warm-up", "Open strings, then the D and G string patterns."),
            (10, "C and A patterns", "Open, 1, 3, 4 on the C string, then on the A string. Check each note with the live checker."),
            (10, "Au Clair de la Lune", "Slow, heavy bows. Listen for the G string sounding by accident."),
            (15, "Lightly Row", "Move the bow over to the A string a moment before the top note, so it speaks on time."),
            (5, "Play through", "One tune, start to finish."),
        ),
    ),
    Lesson(
        week=7,
        title="Reading it on paper",
        pieces=("oldmac", "reading"),
        goals=(
            "Find the four open strings on the bass staff",
            "Name the notes of the G and D strings from the page",
            "Play a tune you know while reading it",
        ),
        body=(
            "You have been reading a little already, every time you followed the music under a "
            "lesson. This week you slow down and learn what the page is telling you.",
            "Open the Theory tab and read the first section, Reading the staff. Cello music is "
            "written in the bass clef. Each line and each space is one letter, and the letters "
            "run in order as you climb. The open G sits on the bottom line, the open D on the "
            "middle line, and the open A on the top line.",
            "Old MacDonald is here because you already know how it sounds, so your eyes can "
            "follow the notes while your ear checks them. The Reading Study is new. Say the "
            "note names aloud before you play it.",
        ),
        plan=_plan(
            (10, "Warm-up", "Open strings and the finger pattern on all four strings."),
            (10, "Staff study", "Read Reading the staff on the Theory tab. Then point to notes in this week's music and name them."),
            (15, "Old MacDonald", "Play it from the page. Keep your eyes on the music and off your fingers."),
            (10, "Reading Study", "Name the notes, clap the rhythm, then play."),
            (5, "Notes to self", "Which notes did you have to stop and work out? Write them down."),
        ),
    ),
    Lesson(
        week=8,
        title="Bow control: strokes and volume",
        pieces=("dynamics", "london"),
        goals=(
            "Play one smooth, separate bow stroke per note",
            "Play loud and soft on purpose",
            "Change bow direction without a bump",
        ),
        body=(
            "Back to the bow. The basic stroke is called détaché: one note per bow, "
            "changing direction smoothly with no gap and no accent. You have been doing a rough "
            "version of it since week 2.",
            "Loud and soft are called forte and piano. Three things control volume on a cello: "
            "how fast the bow moves, how much arm weight goes into the string, and how close "
            "the bow is to the bridge. For forte, use more bow and more weight and move a "
            "little toward the bridge. For piano, use less bow and less weight, and drift "
            "toward the fingerboard.",
            "Grip is not on that list. Your bow hold should feel the same at every volume.",
        ),
        plan=_plan(
            (10, "Warm-up", "Open strings. Listen to the moment the bow changes direction and try to make it disappear."),
            (10, "Détaché", "Play the G string pattern up and down, one bow per note, all the notes the same length."),
            (15, "Loud and Soft Study", "Play it forte, then piano. Notice what your arm does differently."),
            (10, "London Bridge", "Play each two-bar phrase forte, then repeat it piano like an echo."),
            (5, "Wind down", "One slow, quiet bow on each open string."),
        ),
    ),
    Lesson(
        week=9,
        title="New rhythms",
        pieces=("rhythmecho", "longlongago"),
        goals=(
            "Play eighth notes evenly, two to a beat",
            "Play a dotted quarter note followed by an eighth",
            "Hold a steady beat through a whole tune",
        ),
        body=(
            "Until now every note has lasted one beat or longer. An eighth note lasts half a "
            "beat, so two of them fit in the time of one quarter note. Count them \"1 and 2 and\".",
            "A dotted quarter note lasts a beat and a half. It is nearly always followed by a "
            "single eighth note, and together they fill two beats. Count \"1, 2 and\": hold the "
            "long note through the 2 and play the eighth on the \"and\".",
            "Clap each rhythm while you count aloud before you pick up the bow. Use short "
            "bows for eighth notes, about half the length you use for a quarter. Most people "
            "speed up when the notes get shorter, so set the metronome to 60 and stay with it.",
        ),
        plan=_plan(
            (10, "Warm-up", "Open strings and finger patterns."),
            (20, "Rhythm Echo", "Play it at a slow, even beat. Short bows on the eighth notes."),
            (15, "Long, Long Ago", "The rhythm is long, short, short, over and over. The B is finger 1 on the A string."),
            (5, "Play through", "Play one piece along with a metronome at 60."),
        ),
    ),
    Lesson(
        week=10,
        title="A first scale",
        pieces=("scale", "thirds"),
        goals=(
            "Play a one-octave G major scale from memory",
            "Hear when a scale note is out of tune",
            "Slur two notes in one bow",
        ),
        body=(
            "A scale is a ladder of notes, and G major is one of the easiest on the cello: G, "
            "A, B, C on the G string, then D, E, F♯, G on the D string. It is the finger "
            "pattern you already know, played on two strings in a row.",
            "Play it slowly and listen to each step. The two half steps, B to C and F♯ to G, "
            "are between fingers 3 and 4. If finger 4 sounds dull, it is probably flat. Check "
            "it against the open string next door, which is the same note an octave lower: "
            "when finger 4 is in tune, that string rings along.",
            "A slur is a curved line over two or more different notes, and it means you play "
            "them in one bow. Start with two notes to a bow: G and A on a down-bow, B and C on "
            "an up-bow. Change finger exactly halfway through the stroke.",
        ),
        plan=_plan(
            (10, "Warm-up", "Open strings, then the G and D string patterns."),
            (15, "G major scale", "One bow per note, up and down. Check B and F♯ with the live checker."),
            (10, "Slurs", "The same scale, two notes to a bow."),
            (10, "Scale in thirds", "Play G Major Scale in Thirds below. Every pair skips one note of the scale."),
            (5, "From memory", "Put the phone down and play the scale up and down once."),
        ),
    ),
    Lesson(
        week=11,
        title="Polishing a piece",
        pieces=("etude", "andante"),
        goals=(
            "Choose one piece and get it ready to play for someone",
            "Find its two or three hardest spots and fix them",
            "Play it through at one steady speed",
        ),
        body=(
            "Nothing new this week. Pick one piece to polish: Etude in G or Andante in G below, "
            "or a favorite from an earlier week.",
            "Play it through once and mark the places where you stumble. There are usually two "
            "or three. Practice those spots alone, a few notes at a time and at half speed, "
            "until you can play each one correctly three times in a row. Then add the bar "
            "before and the bar after.",
            "Starting from the top every time you make a mistake feels productive, but it "
            "mostly rehearses the parts you can already play.",
        ),
        plan=_plan(
            (10, "Warm-up", "Open strings and the G major scale."),
            (10, "Find the hard spots", "Play your piece once and note where it falls apart."),
            (15, "Spot practice", "Loop each hard spot slowly. Three correct tries in a row, then move on."),
            (10, "Run-throughs", "Play the whole piece twice at a speed you can keep up all the way through."),
            (5, "Record", "Record one run-through and listen back. Pick one thing to fix tomorrow."),
        ),
    ),
    Lesson(
        week=12,
        title="Putting it together",
        pieces=("recital", "arpeggio"),
        goals=(
            "Play a piece from memory for another person",
            "Tune by ear, then confirm with the tuner",
            "Decide what to learn next",
        ),
        body=(
            "In twelve weeks you have learned to sit with the cello and hold the bow, play in "
            "tune on all four strings in first position, read simple music in the bass clef, "
            "count basic rhythms and play a scale. That is a solid start.",
            "Try tuning by ear this week. Tune the A string with the tuner, then play A and D "
            "together and adjust the D string until the two notes ring smoothly, with no wobble "
            "in the sound. Do the same for D with G, then G with C. Check your work with the "
            "tuner afterwards.",
            "Then play for someone. A friend, a family member or your phone's camera all count. "
            "Playing for a listener is a skill of its own and it only improves with practice.",
            "After this course, the usual next steps are extensions, where finger 1 stretches "
            "back or the hand opens forward by an extra half step (which opens up keys such as "
            "D major across all the strings and F major), longer slurs, and later fourth "
            "position and vibrato. A teacher will get you through those faster than an app can, "
            "because a teacher can see your posture and hear your tone.",
        ),
        plan=_plan(
            (10, "Tune by ear", "A from the tuner, the other three by ear, then check them."),
            (10, "Review", "G major scale, then the finger pattern on all four strings."),
            (15, "Performance", "Play your polished piece from memory, twice. Record the second one."),
            (10, "This week's pieces", "Recital Piece and G Major Arpeggio. The arpeggio goes up to D on the A string."),
            (5, "Look back", "Play something from week 4. Notice how much easier it has become."),
        ),
    ),
)



def _with_timing(lesson: Lesson) -> Lesson:
    """Attach the week's timing study and slot it into the plan after the warm-up."""
    study = TIMING[lesson.week]
    item = PlanItem(10, f"Timing: {study.title}", study.plan_text)
    return replace(lesson, timing=study, plan=(lesson.plan[0], item, *lesson.plan[1:]))


LESSONS = tuple(_with_timing(lesson) for lesson in LESSONS)
LESSON_BY_WEEK = {lesson.week: lesson for lesson in LESSONS}



def piece_menu() -> dict[str, str]:
    """'Week 3: Hot Cross Buns' -> piece id, in course order."""
    from ..music.pieces import PIECES
    return {f"Week {lesson.week}: {PIECES[piece_id].title}": piece_id
            for lesson in LESSONS for piece_id in lesson.pieces}


LESSONS_INTRO = ("One lesson a week, planned for an hour of practice a day. "
                 "Take them in order, because each one builds on the last.")
