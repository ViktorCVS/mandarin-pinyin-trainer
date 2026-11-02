# Mandarin Pinyin Trainer (汉语拼音)

**An offline desktop application for practicing Mandarin vocabulary, recognizing Chinese characters, and recalling accurate Hanyu Pinyin with tones.**

Built with Python and Tkinter. The interface is available in Brazilian Portuguese, English, Spanish, and Simplified Chinese. English and Spanish modes also display vocabulary meanings and example translations in the selected language. Portuguese mode uses Brazilian Portuguese translations. Simplified Chinese mode hides translations while keeping Chinese text and Pinyin.

**Tested on Windows 11.**

<img width="1264" height="1057" alt="image" src="https://github.com/user-attachments/assets/bf5221b9-b129-4ce3-8dcd-30dd8173285e" />

## Project Purpose

Mandarin Pinyin Trainer connects Hanzi, Pinyin, and meaning through active recall. Each flashcard presents a word or vocabulary unit; the learner types its pronunciation with tones and receives feedback, a translation, and a contextual example.

The application supports independent review of classroom vocabulary. It focuses on written recognition and Pinyin transcription rather than evaluating spoken pronunciation.

## Current Vocabulary

The current collection includes **1,009 flashcards across 5 blocks and 20 sessions**, incorporating textbook material and classroom slides from Lessons 16–20.

| Block | Main topics | Cards | Sessions | Chinese characters per session |
|---|---|---:|---:|---|
| 16 | Sports, hobbies, preferences, and daily activities | 234 | 5 | 100, 100, 100, 100, 26 |
| 17 | Calligraphy, cooking, home, furniture, and ongoing actions | 167 | 3 | 100, 100, 62 |
| 18 | Comparisons, food, weather, and transportation | 197 | 4 | 100, 100, 100, 48 |
| 19 | Lost belongings, city locations, accidents, and past-event details | 196 | 4 | 100, 100, 100, 58 |
| 20 | Job interviews, personal qualities, teaching, and result complements | 215 | 4 | 100, 100, 100, 74 |
| **Total** | | **1,009** | **20** | |

Each session contains **at most 100 Chinese characters**, counted across its cards. This does not mean 100 cards or 100 distinct characters. Words are never split between sessions.

Words may appear in more than one block. Each occurrence has independent progress, so the total above counts cards rather than globally unique words.

## Features

- **Interface language selector:** switch between Português, English, Español, and 简体中文 while preserving your current card and progress. Your choice is saved automatically.
- **English and Spanish study translations:** both modes include word meanings and example translations for all 1,009 cards in Blocks 16–20, bundled for offline use.
- **Tone-aware answers:** numerical Pinyin and accented Pinyin input, with supported pronunciation variants.
- **Contextual feedback:** numerical Pinyin, tone marks, and a Chinese example with Pinyin. Word meanings and example translations are shown in English, Spanish, or Brazilian Portuguese according to the selected mode. Simplified Chinese mode hides both translations and keeps the Pinyin.
- **Adaptive review:** intervals measured in answers within the selected session, with extra reinforcement after mistakes.
- **Growing priority for new cards:** a gradually increasing chance of introducing unseen vocabulary ahead of due reviews.
- **Individual training index:** consecutive correct answers minus pending errors.
- **Session completion:** trained cards leave the queue; completed sessions receive a visible indicator.
- **Detailed progress:** total correct answers, consecutive correct answers, pending errors, training index, and status for each card.
- **Independent reset:** restart one session or reset all progress.
- **Settings tab:** customize review intervals, repetitions, error recovery, training thresholds, and new-card priority. The original training values are the defaults.
- **Automatic local saving:** resume learning without an account or internet connection.

## Installation

### Run the Python Source

Requirements:

- Python 3.9 or newer.
- Tkinter support.
- A graphical desktop environment and a font capable of displaying Chinese characters.

The application uses Python's standard library. No third-party Python packages are required to run it.

1. Install Python if necessary.
2. Download and extract the repository, or download the main script.
3. Open a terminal in the folder containing the script.
4. Run:

```bash
py mandarin-pinyin-trainer.py
```

If `py` is unavailable:

```bash
python mandarin-pinyin-trainer.py
```

If your copy uses the alternative filename `treino_pinyin_tkinter.py`, substitute that filename in the commands.

To check whether Tkinter is available:

```bash
python -m tkinter
```

### Run a Windows Executable

If a compiled Windows version has been published in the repository's **Releases**, download the executable from that release's assets and open it.

An executable does not require a separate Python installation. Check the release description for its included lesson blocks: a previously published executable may contain an older vocabulary collection than the current source code.

## How to Use

The window has two tabs: **Practice** for studying and **Settings** for adjusting training values. Labels in this README refer to the English interface.

### Interface Language

Use the language selector at the top of the window to choose:

| Option | Interface language | Word and example translations |
|---|---|---|
| Português | Brazilian Portuguese (default) | Brazilian Portuguese |
| English | English | English |
| Español | Spanish | Spanish |
| 简体中文 | Simplified Chinese | Hidden; Chinese text and Pinyin remain visible |

The selection takes effect immediately and is saved for the next launch. It updates interface labels, buttons, feedback messages, and progress displays while preserving the current card, typed answer, and learning progress.

**English and Spanish modes also switch word meanings and example translations to the selected language.** Portuguese mode uses the original Brazilian Portuguese translations. **Simplified Chinese mode hides both word and example translations**, keeping the Chinese text and the word and example Pinyin. If an answer is already visible, changing languages immediately hides, restores, or updates its translations. Accepted answers, review scheduling, and learning progress stay the same.

### Practice a Session

The instructions below use the English interface labels. Select **English** from the language selector to follow along.

1. Select a **Block**, then a **Session**.
2. Read the Chinese word and recall its pronunciation.
3. Enter Pinyin with the correct tones.
4. Click **Check** or press **Enter** to check the answer.
5. Review the pronunciation, translation, and example.
6. Click **Next word** or press **Enter** again to continue.

Use **I don't know (incorrect)** when you cannot recall an answer. It counts as a mistake and schedules additional review.

Open **Session progress** to inspect each card's learning record.

### Pinyin Input

| Chinese | Meaning | Numerical Pinyin |
|---|---|---|
| 喜欢 | To like | `xi3huan` |
| 游泳 | To swim | `you2yong3` |
| 篮球 | Basketball | `lan2qiu2` |
| 朋友 | Friend | `peng2you` |
| 面试 | Interview | `mian4shi4` |

The four main tones use numbers **1–4**. A neutral tone can omit its number or use **5** or **0**. For example, `peng2you`, `peng2you5`, and `peng2you0` are equivalent.

Spaces between syllables are accepted. Accented Pinyin is also supported, for example `miàn shì`.

Tone accuracy matters: correct letters with an incorrect tone are not enough. Supported pronunciation variants are handled explicitly.

## Training Settings

Open the **Settings** tab, edit the values, and click **Save settings**. These settings apply to all blocks and sessions and are saved locally with your progress.

| Setting | Default |
|---|---|
| Correct-answer intervals, stages 1–4 | 5–10, 15–20, 25–50, 50–100 other answers |
| Base repetitions, stages 1–4 | 1, 2, 3, 4 |
| Interval after an error | 3–7 other answers |
| Extra repetitions per historical error, at each stage | 1 |
| Pending errors cleared per correct answer | 1 |
| Minimum indices for OK / Good / Trained | 1 / 5 / 10 |
| New-card chance increase per round without a new card | 1 percentage point |
| Maximum new-card chance | 20% |

Intervals accept whole numbers from 1 to 10,000 and repetitions from 1 to 1,000. Each interval's minimum must not exceed its maximum, and correct-answer intervals must stay the same or increase between stages. Training thresholds must follow **OK < Good < Trained**. The form shows the allowed ranges for the remaining fields. Invalid changes are rejected without changing the saved settings.

Saving preserves your answers, errors, streaks, and scheduled review times. New intervals and repetition requirements apply to future answers. Training statuses, session completion indicators, and the progress bar update immediately: raising the trained threshold can return previously trained cards to the queue. Lowering it can mark more cards as trained.

Click **Restore defaults**, then **Save settings**, to apply the original values. Resetting session or overall learning progress preserves your settings. Changing the interface language also preserves unsaved settings while the application remains open.

## Review Scheduling

The values described below are the defaults; the **Settings** tab lets you customize them.

Review intervals use the number of **other evaluated answers within the same session**, not minutes or calendar days. Studying another session does not advance the current session's review clock.

### Correct Answers

| Stage | Review interval | Correct answers required at this stage, without historical errors |
|---|---|---:|
| 1 | 5–10 answers | 1 |
| 2 | 15–20 answers | 2 |
| 3 | 25–50 answers | 3 |
| 4 | 50–100 answers | 4 |

The interval is randomly selected within the current range. The final stage repeats while the card is still in training; its default range is **50–100**.

By default, each historical mistake adds **one additional correct repetition to every stage's requirement**. After one mistake, the requirements become 2, 3, 4, and 5; after two mistakes, they become 3, 4, 5, and 6. Set the extra-repetition value to zero to disable this penalty.

### Incorrect Answers

An incorrect answer:

- Adds one pending error and one historical error.
- Resets the consecutive-correct streak and review stage.
- Schedules a review after **3–7 other answers** in that session.

A subsequent correct answer removes **one pending error** by default, down to zero. This recovery amount is configurable. Historical errors remain recorded and contribute to the configured reinforcement requirement until the session is reset.

### Growing Priority for New Cards

When both new cards and due reviews are available, the application can choose a new card first:

- The chance starts at **0%**.
- Each evaluated answer to a previously attempted card adds **1 percentage point**.
- The chance is capped at **20%**.
- Answering a new card for the first time resets the chance to **0%**, whether the answer is correct or incorrect.

With the defaults, five rounds without a newly attempted card produce a 5% chance; fifteen rounds produce 15%. The increase and cap are configurable from 0 to 100; setting either to zero disables this extra priority.

Review intervals are soft scheduling targets. A new card can delay a due review without changing that review's stored due value. When no reviews are due, new cards already have priority. When neither new cards nor due reviews remain, an upcoming review may appear early.

## Training Index and Session Completion

Each card has a training index:

```text
Training index = consecutive correct answers − pending errors
```

An incorrect answer restarts the consecutive-correct sequence at zero.

| Default index | Status | Behavior |
|---|---|---|
| Below 1 | New / In training | New or still in training |
| 1–4 | OK | Remains in the review queue |
| 5–9 | Good | Remains in the review queue |
| 10 or above | Trained | Leaves the review queue |

Once every card in a session reaches the configured trained threshold (10 by default), the session receives a **✓ Trained** indicator. The progress bar measures the percentage of trained cards, not merely cards that have appeared.

The training threshold takes precedence over scheduled reviews: a trained card no longer appears unless its progress is reset or the trained threshold is raised above its current index.

## Statistics

The selected session shows its card count, studied cards, total correct answers, pending errors, and accuracy rate. The footer also reports unseen cards, pending reviews, local answer counts, and overall progress.

The displayed accuracy rate uses **pending errors**, not lifetime mistakes:

```text
Accuracy = correct answers / (correct answers + pending errors) × 100
```

After all pending errors are cleared, the rate returns to **100%**. A session with no answers displays **—**.

The **Session progress** window lists each card's total correct answers, consecutive correct answers, pending errors, training index, and status.

## Saving and Resetting Progress

Progress, interface language, and applied training settings are saved in the current user's home directory:

```text
.treino_pinyin_sessoes_progresso.json
```

On Windows, this is normally:

```text
%USERPROFILE%\.treino_pinyin_sessoes_progresso.json
```

The save file is separate from the script or executable. Moving the program does not remove progress when the same user profile and save file are retained.

The current version preserves existing blocks when adding new ones and supports migration from earlier supported save formats. Saves without training settings receive the original defaults while keeping their learning history. New blocks start with fresh progress.

### Backups

Close the application and copy the JSON file to back up your progress. To restore it, close the application and place the backup in the same location, using a compatible application version.

### Reset Options

- **Reset this session:** resets only the selected session, including its card records, review clock, and new-card priority. Other sessions remain unchanged.
- **Reset all:** resets progress across every block and session.

Both actions request confirmation. Back up the save file beforehand if you want to retain the previous history.

## Built-in Self-Test

Run the built-in checks without opening the study interface:

```bash
py -X utf8 mandarin-pinyin-trainer.py --self-test
```

The UTF-8 option allows Chinese test output to display correctly in compatible Windows terminals. The checks cover vocabulary structure, English and Spanish translation coverage, session sizes, tone normalization, review intervals, and progress migration.

## Scope and Limitations

- The interface supports Portuguese, English, Spanish, and Simplified Chinese. Study translations are in English, Spanish, or Brazilian Portuguese in their respective modes. Simplified Chinese mode hides translations while retaining Chinese text and Pinyin.
- Vocabulary is bundled in the Python source; the application does not import PDFs automatically.
- There is no microphone input, pronunciation scoring, audio playback, or speech recognition.
- Review scheduling is based on answered cards rather than calendar time.
- Progress is stored locally, without cloud synchronization.
- CSV export is not included.
- A trained card's status is an application practice milestone, not a certification of language proficiency.

## License

This project is released under **The Unlicense**. See the `LICENSE` file for the complete terms.
