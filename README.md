# Mandarin Pinyin Trainer (汉语拼音)

**An offline desktop application for practicing Mandarin vocabulary, recognizing Chinese characters, and recalling accurate Hanyu Pinyin with tones.**

Built with Python and Tkinter. The interface, vocabulary translations, and example translations are in Brazilian Portuguese.

**Tested on Windows 11.**

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

- **Tone-aware answers:** numerical Pinyin and accented Pinyin input, with supported pronunciation variants.
- **Contextual feedback:** numerical Pinyin, tone marks, Brazilian Portuguese translation, and an example with Chinese text, Pinyin, and translation.
- **Adaptive review:** intervals measured in answers within the selected session, with extra reinforcement after mistakes.
- **Growing priority for new cards:** a gradually increasing chance of introducing unseen vocabulary ahead of due reviews.
- **Individual training index:** consecutive correct answers minus pending errors.
- **Session completion:** trained cards leave the queue; completed sessions receive a visible indicator.
- **Detailed progress:** total correct answers, consecutive correct answers, pending errors, training index, and status for each card.
- **Independent reset:** restart one session or reset all progress.
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

1. Select a **Bloco** (Block), then a **Sessão** (Session).
2. Read the Chinese word and recall its pronunciation.
3. Enter Pinyin with the correct tones.
4. Click **Verificar** or press **Enter** to check the answer.
5. Review the pronunciation, translation, and example.
6. Click **Próxima palavra** or press **Enter** again to continue.

Use **Não sei (erro)** when you cannot recall an answer. It counts as a mistake and schedules additional review.

Open **Progresso da sessão** to inspect each card's learning record.

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

## Review Scheduling

Review intervals use the number of **other evaluated answers within the same session**, not minutes or calendar days. Studying another session does not advance the current session's review clock.

### Correct Answers

| Stage | Review interval | Correct answers required at this stage, without historical errors |
|---|---|---:|
| 1 | 5–10 answers | 1 |
| 2 | 15–20 answers | 2 |
| 3 | 25–50 answers | 3 |
| 4 | 50–100 answers | 4 |

The interval is randomly selected within the current range. The final range remains **50–100** while the card is still in training.

Each historical mistake adds **one additional correct repetition to every stage's requirement**. After one mistake, the requirements become 2, 3, 4, and 5; after two mistakes, they become 3, 4, 5, and 6.

### Incorrect Answers

An incorrect answer:

- Adds one pending error and one historical error.
- Resets the consecutive-correct streak and review stage.
- Schedules a review after **3–7 other answers** in that session.

A subsequent correct answer removes **one pending error**, down to zero. Historical errors remain recorded and continue to increase the reinforcement requirement until the session is reset.

### Growing Priority for New Cards

When both new cards and due reviews are available, the application can choose a new card first:

- The chance starts at **0%**.
- Each evaluated answer to a previously attempted card adds **1 percentage point**.
- The chance is capped at **20%**.
- Answering a new card for the first time resets the chance to **0%**, whether the answer is correct or incorrect.

For example, five rounds without a newly attempted card produce a 5% chance; fifteen rounds produce 15%.

Review intervals are soft scheduling targets. A new card can delay a due review without changing that review's stored due value. When no reviews are due, new cards already have priority. When neither new cards nor due reviews remain, an upcoming review may appear early.

## Training Index and Session Completion

Each card has a training index:

```text
Training index = consecutive correct answers − pending errors
```

An incorrect answer restarts the consecutive-correct sequence at zero.

| Index | Status | Behavior |
|---|---|---|
| Below 1 | Novo / Em treino | New or still in training |
| 1–4 | OK | Remains in the review queue |
| 5–9 | Bom | Remains in the review queue |
| 10 or above | Treinado | Leaves the review queue |

Once every card in a session reaches the trained threshold, the session receives a **✓ Treinada** indicator. The progress bar measures the percentage of trained cards, not merely cards that have appeared.

The training threshold takes precedence over scheduled reviews: a trained card no longer appears unless its progress is reset.

## Statistics

The selected session shows its card count, studied cards, total correct answers, pending errors, and accuracy rate. The footer also reports unseen cards, pending reviews, local answer counts, and overall progress.

The displayed accuracy rate uses **pending errors**, not lifetime mistakes:

```text
Accuracy = correct answers / (correct answers + pending errors) × 100
```

After all pending errors are cleared, the rate returns to **100%**. A session with no answers displays **—**.

The **Progresso da sessão** window lists each card's total correct answers, consecutive correct answers, pending errors, training index, and status.

## Saving and Resetting Progress

Progress is saved automatically in the current user's home directory:

```text
.treino_pinyin_sessoes_progresso.json
```

On Windows, this is normally:

```text
%USERPROFILE%\.treino_pinyin_sessoes_progresso.json
```

The save file is separate from the script or executable. Moving the program does not remove progress when the same user profile and save file are retained.

The current version preserves existing blocks when adding new ones and supports migration from earlier supported save formats. New blocks start with fresh progress.

### Backups

Close the application and copy the JSON file to back up your progress. To restore it, close the application and place the backup in the same location, using a compatible application version.

### Reset Options

- **Zerar esta sessão:** resets only the selected session, including its card records, review clock, and new-card priority. Other sessions remain unchanged.
- **Zerar tudo:** resets progress across every block and session.

Both actions request confirmation. Back up the save file beforehand if you want to retain the previous history.

## Built-in Self-Test

Run the built-in checks without opening the study interface:

```bash
py -X utf8 mandarin-pinyin-trainer.py --self-test
```

The UTF-8 option allows Chinese test output to display correctly in compatible Windows terminals. The checks cover vocabulary structure, session sizes, tone normalization, review intervals, and progress migration.

## Scope and Limitations

- The interface and translations are primarily in Brazilian Portuguese.
- Vocabulary is bundled in the Python source; the application does not import PDFs automatically.
- There is no microphone input, pronunciation scoring, audio playback, or speech recognition.
- Review scheduling is based on answered cards rather than calendar time.
- Progress is stored locally, without cloud synchronization.
- CSV export is not included.
- A trained card's status is an application practice milestone, not a certification of language proficiency.

## License

This project is released under **The Unlicense**. See the `LICENSE` file for the complete terms.
