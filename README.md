# Python Tutorial Lesson Page

A Flask project that recreates the structure of a tutorial lesson page with a left sidebar, lesson navigation, code examples, and a simple Python runner.

## Features

- Fixed-style lesson sidebar
- Five Python tutorial lessons
- Previous and Next lesson navigation
- Editable code area
- Run Code button with backend execution
- JSON-based lesson content

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open `http://127.0.0.1:5000/` in your browser.

## Notes

- Lesson content is stored in `content/python.json`.
- Code execution includes basic restrictions and a short timeout.
- This project is intended for tutorial demos, not production sandboxing.
