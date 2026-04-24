from __future__ import annotations

import io
import json
import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
CONTENT_FILE = BASE_DIR / "content" / "python.json"

app = Flask(__name__)

with CONTENT_FILE.open("r", encoding="utf-8") as file:
    LESSONS = json.load(file)

LESSON_INDEX = {lesson["slug"]: idx for idx, lesson in enumerate(LESSONS)}


@app.route("/")
def index():
    first_lesson = LESSONS[0]["slug"] if LESSONS else None
    return render_template("index.html", lessons=LESSONS, first_lesson=first_lesson)


@app.route("/lesson/<slug>")
def lesson(slug: str):
    if slug not in LESSON_INDEX:
        abort(404)

    idx = LESSON_INDEX[slug]
    current = LESSONS[idx]
    previous_lesson = LESSONS[idx - 1] if idx > 0 else None
    next_lesson = LESSONS[idx + 1] if idx < len(LESSONS) - 1 else None

    return render_template(
        "lesson.html",
        lessons=LESSONS,
        lesson=current,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
    )


@app.post("/run-code")
def run_code():
    payload = request.get_json(silent=True) or {}
    code = (payload.get("code") or "").strip()

    if not code:
        return jsonify({"output": "Please enter Python code before running."}), 400

    if len(code) > 4000:
        return jsonify({"output": "Code is too long. Keep it under 4000 characters."}), 400

    blocked_terms = [
        "import os",
        "import sys",
        "import subprocess",
        "from os",
        "from sys",
        "from subprocess",
        "open(",
        "exec(",
        "eval(",
        "__import__",
        "socket",
        "pathlib",
        "shutil",
    ]

    lowered = code.lower()
    for term in blocked_terms:
        if term in lowered:
            return jsonify({"output": f"Blocked for safety: {term}"}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = Path(temp_dir) / "snippet.py"
        script_path.write_text(code, encoding="utf-8")

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=3,
                cwd=temp_dir,
                env={"PYTHONIOENCODING": "utf-8"},
            )
        except subprocess.TimeoutExpired:
            return jsonify({"output": "Execution stopped after 3 seconds."}), 408
        except Exception as exc:
            return jsonify({"output": f"Server error: {exc}"}), 500

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    if stdout and stderr:
        output = f"{stdout}\n\nErrors:\n{stderr}"
    else:
        output = stdout or stderr or "Program finished with no output."

    return jsonify({"output": output})


if __name__ == "__main__":
    app.run(debug=True)
