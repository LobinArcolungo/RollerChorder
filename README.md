<div align="center">

![RollerChorder Icon](icon_tests/OFFICIAL_ICON.png)

**RollerChorder — chord tools and apps**

</div>

A collection of utilities for extracting, managing and displaying song chords. The project contains three main components: a Python chord extractor, a Telegram bot for remote access, and an Apple Watch app for on-wrist chord display. The 

**Components**
- **`chord_getter_py`**: Python scripts that parse text files containing chords and return relevant chords for a song. The main script is `getSongChord.py` and the `chords/` folder holds sample source files.
- **`RollerChorderBot`**: a Telegram bot and supporting scripts that provide remote access to the project's features. Key files include `RollerChordBot.py`, `qr_reading_test.py` and `database_test_0.py`.
- **`RollerChorder`**: an Apple Watch app (Xcode project) to display chords and provide a simple UI for scrolling through content while playing. App logic is under `RollerChorder WatchKit Extension/Model` and UI files are in `View`.

**Quick overview**
- Purpose: make it easy to find, manage and display musical chords for live playing and practice.
- Audience: musicians, developers who need chord lookup functionality, and Apple Watch users who want chords on their wrist.

**Quick start**
- Prerequisites: `python3` for the Python scripts; Xcode to open and build the WatchOS app; a Telegram Bot API token to run the bot.
- Example commands:

```bash
# Run the chord extractor on a test file
python3 chord_getter_py/getSongChord.py chord_getter_py/oldtests/content.txt

# Start the Telegram bot (configure credentials in the bot script first)
python3 RollerChorderBot/RollerChordBot.py

# Open the Watch app project in Xcode
open RollerChorder/RollerChorder.xcodeproj
```

**Repository structure (relevant folders)**
- `chord_getter_py/` — chord extractor and test files.
- `RollerChorderBot/` — Telegram bot and utility scripts.
- `RollerChorder/` — Xcode project for the WatchOS app.

**Contributing**
- File an issue or submit a pull request for improvements or bug fixes. For Watch changes, test in Xcode or the Simulator.

**License**
- Add license information here (e.g., MIT) or ask the maintainer which license to use.

---

If you want, I can extend this README with detailed Python dependency installation, sample outputs from `getSongChord.py`, or a template for configuring the Telegram bot.
