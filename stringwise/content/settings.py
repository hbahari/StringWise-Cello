"""Text and links for the Settings screen."""

SUPPORT_EMAIL = "golemapps1@gmail.com"
PACKAGE = "golemapps.stringwisecello.app"
STORE_APP_LINK = f"market://details?id={PACKAGE}"
STORE_WEB_LINK = f"https://play.google.com/store/apps/details?id={PACKAGE}"
PRIVACY_LINK = "https://github.com/hbahari/StringWise-Cello/blob/main/PRIVACY_POLICY.md"

PITCH_TITLE = "Tuning pitch"
PITCH_TEXT = ("The note A that everything is tuned to. Leave it at 440 unless your teacher or "
              "orchestra tunes higher. It changes the tuner, the finger check, Play-Along and "
              "every note the app plays.")

FEEDBACK_TITLE = "Feedback and sharing"
FEEDBACK_TEXT = ("Found a problem or have an idea? Send an email and it goes straight to the "
                 "developer. Your app version and phone model are added so problems are easier "
                 "to track down.")
FEEDBACK_SUBJECT = "StringWise Cello feedback"
FEEDBACK_BODY = "\n\n\n---\nStringWise Cello {version}\n{device}\n"
NO_EMAIL_APP = "No email app was found. You can write to " + SUPPORT_EMAIL + " from any device."
NO_BROWSER = "That link could not be opened on this device."

SHARE_BUTTON = "Share StringWise Cello"
SHARE_SUBJECT = "StringWise Cello"
SHARE_MESSAGE = ("I'm learning cello with StringWise Cello, a free twelve-week course with a "
                 "tuner and metronome built in. " + STORE_WEB_LINK)
SHARE_COPIED = "The link has been copied. Paste it into a message to share it."
SHARE_FAILED = "Sharing isn't available on this device."

PROGRESS_TITLE = "Progress"
PROGRESS_TEXT = ("Clears your lesson ticks, completed weeks, saved tempos and finished rhythms, "
                 "and goes back to week 1. Your settings are kept.")
RESET_CONFIRM_TITLE = "Reset all progress?"
RESET_CONFIRM = ("This clears every tick, completed week, saved tempo and finished rhythm. "
                 "It cannot be undone.")
RESET_DONE = "Progress cleared. You are back at week 1."

ABOUT_TITLE = "About"
TOUR_AGAIN = "Show the app tour again"
ABOUT_TEXT = ("StringWise Cello works offline and needs no account. Sound from the microphone is "
              "analysed on this phone and never leaves it.")
