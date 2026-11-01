# Mandarin Pinyin Trainer (汉语拼音)

**A desktop application for practicing Mandarin Chinese vocabulary, Chinese character recognition (Hanzi), and accurate Hanyu Pinyin transcription through tone validation, spaced repetition, and progress tracking.**

Built with Python and Tkinter, Mandarin Pinyin Trainer is a free, offline study tool designed to help Mandarin learners strengthen vocabulary retention, pronunciation awareness, and familiarity with Chinese characters.

**Tested on Windows 11.**

---

## Project Purpose

Mandarin Pinyin Trainer was developed to support Mandarin Chinese learners in building stronger connections between three essential components of the language:

- **Hanzi (汉字):** The Chinese characters used in written Mandarin.
- **Hanyu Pinyin (汉语拼音):** The romanization system used to represent Mandarin pronunciation with the Latin alphabet.
- **Tones:** The tonal distinctions that affect pronunciation and often determine the meaning of Chinese words.

The primary objective is not simply to recognize vocabulary, but to develop the ability to actively recall pronunciation, identify correct tones, and retain vocabulary through repeated practice.

Unlike conventional vocabulary lists, the application uses an interactive flashcard system with spaced repetition. The learner's performance influences how frequently individual vocabulary items are presented.

The project originated from the need to systematically review vocabulary introduced in Mandarin Chinese lessons. Its initial vocabulary database combines study sentences, classroom slides, and textbook material from Lesson 16, covering topics such as sports, hobbies, preferences, daily activities, questions, and common grammatical constructions.

Vocabulary is divided into manageable study sessions, allowing learners to concentrate on smaller groups of characters while progressively consolidating their knowledge.

The application is particularly suitable for beginners and students who want a structured, self-paced way to practice Mandarin vocabulary independently.

## Features

### Interactive Vocabulary Flashcards

Each flashcard presents a Chinese word or vocabulary unit written in Hanzi.

The learner must recall and enter the corresponding Pinyin transcription, including the appropriate tones.

Flashcards focus on individual vocabulary units rather than requiring the transcription of entire sentences.

### Pinyin and Tone Validation

The application checks both the spelling and tonal accuracy of the submitted answer.

Correct letters alone are not sufficient when the expected tones are incorrect.

The validation system supports numerical Pinyin notation and includes normalization for accented Pinyin input.

### Adaptive Spaced Repetition

A custom review algorithm adjusts the frequency of vocabulary repetition according to the learner's performance.

Words answered incorrectly return for review after shorter intervals, while words answered correctly advance through progressively longer review stages.

The system also considers historical mistakes, increasing the reinforcement required for vocabulary that has previously caused difficulty.

### Organized Study Sessions

Vocabulary is divided into sessions containing up to 100 Chinese characters, without splitting individual words between sessions.

Learners can select sessions and navigate between them using the graphical interface.

### Portuguese Translations and Contextual Examples

After answering a flashcard, the application displays:

- The expected numerical Pinyin transcription.
- The Pinyin with tone marks.
- The vocabulary translation in Brazilian Portuguese.
- An example sentence written in Chinese characters.
- The example sentence's Pinyin transcription.
- The example sentence's Portuguese translation.

This helps learners connect isolated vocabulary with meaningful language usage.

### Performance Statistics

The application tracks several learning indicators, including:

- Total vocabulary items in the selected session.
- Vocabulary items already studied.
- Correct answers.
- Pending errors.
- Answer accuracy rate.
- Session progress and pending reviews.

### Automatic Progress Saving

Learning progress is automatically saved locally, allowing users to resume studying without restarting their entire review history.

### Offline Operation

The application does not require an internet connection, user account, cloud service, or external API.

The vocabulary database and learning logic are included directly in the Python source code.

---

## Download and Installation

There are two ways to use Mandarin Pinyin Trainer.

The first option is recommended for users who simply want to study Mandarin without installing programming tools.

### Option 1: Download the Windows Executable (.exe)

**Recommended for beginners and users without programming experience.**

This method does not require Python to be installed.

**Step 1 — Find the executable**

1. Open this project's GitHub repository.
2. Find the **Releases** section.
3. Open the latest published release.
4. Under **Assets**, locate `TreinoPinyin.exe` or the corresponding executable filename.
5. Download the file.

**Step 2 — Run the application**

1. Open your Downloads folder.
2. Locate the downloaded `.exe` file.
3. Double-click it.
4. The Mandarin Pinyin Trainer interface should appear.

The program is ready to use.

**Important notes:**

- The executable is available through Releases only when a compiled version has been published.
- Python does not need to be installed separately.
- No internet connection is required.
- The `.exe` is a standalone application, not an installer.
- Download executable files only from trusted sources. If Windows displays a security warning, verify the file's origin before proceeding.

### Option 2: Download and Run the Python Source Code

This option is intended for users who prefer to run the original Python script, inspect the source code, or modify the application.

No advanced programming experience is required.

**Step 1 — Install Python**

Visit the official Python website:

https://www.python.org/downloads/

Download and install Python 3.9 or newer.

If your installer provides an **Add Python to PATH** option, enable it.

**Step 2 — Download the repository**

1. Open the GitHub repository.
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Wait for the download to finish.
5. Extract the ZIP archive.
6. Open the extracted folder.

Locate the main Python script:

`treino_pinyin_tkinter.py`

**Step 3 — Open a terminal**

On Windows 11:

1. Open the folder containing the Python script.
2. Click the File Explorer address bar.
3. Type `cmd`.
4. Press Enter.

A Command Prompt window will open in the selected directory.

**Step 4 — Start the application**

Run:

```bash
py treino_pinyin_tkinter.py
```

Alternatively, if the `py` command is unavailable:

```bash
python treino_pinyin_tkinter.py
```

The application should launch its graphical interface.

**Dependencies**

The program relies on Python's standard library, including Tkinter, JSON handling, and file-system utilities.

No additional third-party Python packages are required to run the source code, provided that Tkinter is available in the Python installation.

---

## How to Use

Once the application is running, follow these steps.

### 1. Select a Study Session

Choose the vocabulary session you want to practice.

The current vocabulary collection is organized under Block 16.

Each session contains a limited number of Chinese characters to make studying more manageable.

### 2. Read the Chinese Characters

A flashcard will display a Chinese word or vocabulary unit.

Try to remember its pronunciation before submitting an answer.

### 3. Enter the Pinyin

Type the Pinyin transcription in the input field, including the tone numbers.

For example:

| Chinese | Meaning | Expected Pinyin |
|---|---|---|
| 喜欢 | To like | `xi3huan` |
| 游泳 | To swim | `you2yong3` |
| 篮球 | Basketball | `lan2qiu2` |
| 跑步 | To run | `pao3bu4` |
| 朋友 | Friend | `peng2you` |

### 4. Check Your Answer

Click **Verificar** (Check) or press Enter.

The application will indicate whether the answer is correct.

After evaluation, it displays the expected Pinyin, translation, and an example sentence with its corresponding pronunciation and meaning.

### 5. Continue Studying

Click **Próxima palavra** (Next Word) or press Enter again to move to the next flashcard.

If you cannot remember a word, click **Não sei (erro)** (I Don't Know).

The application will record the answer as incorrect and schedule that vocabulary item for additional review.

### Understanding Mandarin Tone Numbers

Mandarin Chinese has four main lexical tones and a neutral tone.

| Tone | Example | Numerical Pinyin |
|---|---|---|
| First tone | mā | ma1 |
| Second tone | má | ma2 |
| Third tone | mǎ | ma3 |
| Fourth tone | mà | ma4 |
| Neutral tone | ma | ma, ma5, or ma0 |

Numerical notation is recommended because it is straightforward to enter using a conventional keyboard.

**Tone accuracy matters:** an incorrect tone may cause an otherwise correctly spelled answer to be marked incorrect.

---

## How Spaced Repetition Works

The application's spaced repetition mechanism is designed to reinforce difficult vocabulary while gradually reducing unnecessary repetition of familiar words.

Every flashcard has an individual learning record.

When a word is answered correctly, it progresses through stages with increasingly longer review intervals.

When a word is answered incorrectly, its learning stage is reset and it becomes eligible for review after a shorter interval.

The application also tracks historical mistakes, which influence how much repetition is required before advancing through learning stages.

### Review Intervals

The review system uses the number of evaluated answers within the active study session rather than calendar time.

For example, a word may become eligible for review after several other answers have been evaluated.

As performance improves, review intervals increase. Words with repeated errors require additional reinforcement.

This makes the system suitable for continuous practice sessions without depending on daily schedules or internet-based reminders.

When no new or currently due vocabulary is available, the program can present an upcoming review early.

---

## Saving and Managing Progress

Mandarin Pinyin Trainer automatically stores the learner's progress on the local computer.

Saved information includes answer history, learning stages, pending reviews, and study-session information.

On Windows 11, the progress file is stored in the user's home directory:

```text
.treino_pinyin_sessoes_progresso.json
```

The progress file is separate from the application executable.

This allows study history to remain available after moving the executable to another directory, provided that the same Windows user account and progress file are retained.

### Backing Up Your Progress

To preserve your progress, make a backup copy of the JSON file.

The file can also be transferred to another computer to restore the saved learning history, provided that the application version supports the saved data format.

### Resetting Progress

The **Zerar tudo** (Reset All) button resets the learning history across all sessions after user confirmation.

This includes stored answer statistics and review history.

**Warning:** resetting progress removes the existing learning records.

The application does not provide cloud synchronization or automatic online backups.

---

## System Requirements and Compatibility

**Tested operating system: Windows 11.**

For running the Python source code:

- Python 3.9 or newer.
- Tkinter support.
- A graphical desktop environment.
- A font capable of displaying Chinese characters.

For running the Windows executable:

- Windows 11.
- The compiled `.exe` file.

An internet connection is not required for normal operation.

---

## Current Scope and Limitations

The current version focuses on written vocabulary recognition and Pinyin recall.

The application is designed as a supplementary study tool rather than a complete Mandarin language course.

The following limitations apply:

- The vocabulary database is based on the educational material incorporated into the application.
- The application does not evaluate spoken pronunciation or microphone input.
- It does not provide audio playback or speech recognition.
- The interface and vocabulary explanations are primarily in Brazilian Portuguese.
- Learning progress is stored locally rather than synchronized online.
- The review algorithm uses answer-based intervals rather than real-time calendar scheduling.

The project is intended to support active recall, accurate tone identification, vocabulary reinforcement, and independent Mandarin study.

---

## License

This project is released under **The Unlicense**, allowing unrestricted use, modification, copying, and redistribution of the source code.

See the `LICENSE` file for the complete terms.

---

**Mandarin Pinyin Trainer** — A simple, structured, and offline approach to strengthening Mandarin vocabulary recognition, Pinyin accuracy, and long-term retention through active recall and spaced repetition.
