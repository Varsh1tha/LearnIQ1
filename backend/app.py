
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
from pathlib import Path
from datetime import date, datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
DB_DIR = ROOT / "database"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "learniq.db"

app = Flask(
    __name__,
    template_folder=str(ROOT / "templates"),
    static_folder=str(ROOT / "static")
)
CORS(app)


# LESSONS
SUBJECTS = {
    "python": {
        "name": "Python",
        "description": "Learn coding from the very beginning.",
        "color": "pink",
        "lessons": [
            {
                "id": "py1", "title": "What is Python?",
                "duration": 8, "difficulty": "Beginner",
                "content": "Python is a programming language. We use it to give instructions to a computer. It is popular because its code is readable and it can be used for websites, automation, data science, AI, and much more.",
                "example": 'print("Hello, Varshitha!")',
                "tip": "The print() function displays something on the screen. Text is written inside quotation marks.",
                "question": "What does print() do?",
                "options": ["Deletes code", "Displays output", "Creates a folder", "Closes Python"],
                "answer": 1,
                "explanation": "print() displays information in the output area."
            },
            {
                "id": "py2", "title": "Variables",
                "duration": 10, "difficulty": "Beginner",
                "content": "A variable is a name that stores or refers to a value. You can use that name later instead of typing the value again. In Python, use = to assign a value to a variable.",
                "example": 'name = "Varshitha"\nage = 20\nprint(name)\nprint(age)',
                "tip": "Choose clear names like score, student_name, or total. Python variable names cannot contain spaces.",
                "question": "Which line assigns 10 to the variable score?",
                "options": ["10 = score", "score == 10", "score = 10", "variable score 10"],
                "answer": 2,
                "explanation": "Use the variable name, an equals sign, and then the value: score = 10."
            },
            {
                "id": "py3", "title": "Data types",
                "duration": 12, "difficulty": "Beginner",
                "content": "A data type describes what kind of value you're working with. Common Python types include int for whole numbers, float for decimal numbers, str for text, and bool for True or False.",
                "example": 'age = 20          # int\nprice = 49.5      # float\nname = "Mia"      # str\nis_ready = True   # bool',
                "tip": "You can check a value's type with type(value), such as type(20).",
                "question": 'What is the data type of "hello"?',
                "options": ["int", "str", "bool", "float"],
                "answer": 1,
                "explanation": "Text inside quotes is a string, shortened to str."
            },
            {
                "id": "py4", "title": "Operators",
                "duration": 10, "difficulty": "Growing",
                "content": "Operators perform actions on values. Arithmetic operators include +, -, *, and /. The % operator gives a remainder, while ** raises a number to a power.",
                "example": "a = 10\nb = 3\nprint(a + b)  # 13\nprint(a % b)  # 1\nprint(a ** 2) # 100",
                "tip": "Try changing a and b and predicting the output before running the code.",
                "question": "What is 10 % 3?",
                "options": ["3", "1", "0", "10"],
                "answer": 1,
                "explanation": "10 divided by 3 leaves a remainder of 1."
            },
            {
                "id": "py5", "title": "Conditions",
                "duration": 12, "difficulty": "Growing",
                "content": "Conditions let a program make decisions. An if statement runs code when a condition is true. You can add elif for another condition and else for the remaining case.",
                "example": 'marks = 75\nif marks >= 90:\n    print("Excellent")\nelif marks >= 40:\n    print("Pass")\nelse:\n    print("Try again")',
                "tip": "Python uses indentation to show which lines belong inside a condition.",
                "question": "Which keyword handles the alternative when an if condition is false?",
                "options": ["repeat", "else", "then", "next"],
                "answer": 1,
                "explanation": "else runs when the preceding if/elif conditions were not true."
            },
            {
                "id": "py6", "title": "Loops",
                "duration": 12, "difficulty": "Practice",
                "content": "Loops repeat instructions. A for loop is useful when you want to go through a sequence or repeat a known number of times. A while loop repeats as long as its condition remains true.",
                "example": "for number in range(1, 4):\n    print(number)\n\n# Output: 1, 2, 3",
                "tip": "range(1, 4) includes 1, 2, and 3. The ending number is not included.",
                "question": "How many times does range(1, 4) loop?",
                "options": ["2", "3", "4", "1"],
                "answer": 1,
                "explanation": "It produces 1, 2, and 3, so the loop runs three times."
            }
        ]
    },
    "math": {
        "name": "Mathematics",
        "description": "Build your problem-solving skills.",
        "color": "orange",
        "lessons": [
            {
                "id": "ma1", "title": "Understanding percentages",
                "duration": 8, "difficulty": "Beginner",
                "content": "Percent means 'out of 100'. A percentage describes a part of a whole. To find a percentage of a number, convert the percentage into a fraction over 100 and multiply.",
                "example": "20% of 150\n= (20 / 100) × 150\n= 30",
                "tip": "10% is one tenth of a number. You can often find it quickly by dividing by 10.",
                "question": "What is 25% of 200?",
                "options": ["25", "40", "50", "75"],
                "answer": 2,
                "explanation": "25/100 × 200 = 50."
            },
            {
                "id": "ma2", "title": "Fractions",
                "duration": 10, "difficulty": "Beginner",
                "content": "A fraction represents part of a whole. The top number is the numerator and the bottom number is the denominator. Equivalent fractions have the same value even if their numbers look different.",
                "example": "1/2 = 2/4 = 4/8\n\nEach fraction represents one half.",
                "tip": "To simplify a fraction, divide the numerator and denominator by the same common factor.",
                "question": "Which fraction is equivalent to 1/2?",
                "options": ["1/3", "2/4", "3/5", "4/6"],
                "answer": 1,
                "explanation": "2/4 simplifies to 1/2 when both numbers are divided by 2."
            },
            {
                "id": "ma3", "title": "Ratios",
                "duration": 10, "difficulty": "Growing",
                "content": "A ratio compares two quantities. A ratio of 2:3 means that for every 2 parts of the first quantity, there are 3 parts of the second. Ratios can be simplified just like fractions.",
                "example": "4:6\nDivide both parts by 2\n= 2:3",
                "tip": "Keep the order of the quantities the same when simplifying or comparing ratios.",
                "question": "Simplify the ratio 6:9.",
                "options": ["3:2", "2:3", "6:3", "1:9"],
                "answer": 1,
                "explanation": "Divide both parts by 3: 6:9 becomes 2:3."
            },
            {
                "id": "ma4", "title": "Algebra basics",
                "duration": 12, "difficulty": "Growing",
                "content": "Algebra uses letters to represent numbers. These letters are called variables. To solve an equation, use inverse operations to isolate the variable while keeping both sides balanced.",
                "example": "x + 5 = 12\nx = 12 - 5\nx = 7",
                "tip": "Whatever operation you use to one side of an equation, use the same operation on the other side.",
                "question": "If x + 4 = 10, what is x?",
                "options": ["14", "6", "4", "2"],
                "answer": 1,
                "explanation": "Subtract 4 from both sides: x = 10 - 4 = 6."
            },
            {
                "id": "ma5", "title": "Averages",
                "duration": 10, "difficulty": "Practice",
                "content": "The mean, often called the average, is the sum of all values divided by how many values there are. It gives one way to describe the center of a group of numbers.",
                "example": "Scores: 6, 8, 10\nMean = (6 + 8 + 10) / 3\n= 24 / 3 = 8",
                "tip": "Count the numbers carefully. The divisor is how many values you have, not the largest value.",
                "question": "What is the mean of 4, 6, and 8?",
                "options": ["4", "5", "6", "8"],
                "answer": 2,
                "explanation": "(4 + 6 + 8) / 3 = 18 / 3 = 6."
            }
        ]
    },
    "english": {
        "name": "English",
        "description": "Build confidence one sentence at a time.",
        "color": "purple",
        "lessons": [
            {
                "id": "en1", "title": "Building simple sentences",
                "duration": 8, "difficulty": "Beginner",
                "content": "A simple English sentence often has a subject and a verb. The subject tells us who or what the sentence is about. The verb tells us the action or state.",
                "example": "I study.\nShe smiles.\nThe dog runs.",
                "tip": "Start with short sentences when practising speaking. Clear and natural is better than complicated and memorized.",
                "question": "Which word is the verb in 'She sings'?",
                "options": ["She", "sings", "the", "none"],
                "answer": 1,
                "explanation": "Sings is the action, so it is the verb."
            },
            {
                "id": "en2", "title": "Present simple tense",
                "duration": 10, "difficulty": "Beginner",
                "content": "We use the present simple for habits, routines, facts, and things that are generally true. With he, she, or it, the verb usually takes -s or -es.",
                "example": "I read every day.\nShe reads every day.\nThey play badminton.",
                "tip": "Compare 'I work' with 'He works'. Listen for that small ending when you practise.",
                "question": "Choose the correct sentence.",
                "options": ["She walk to class.", "She walks to class.", "She walking to class.", "She walkes to class."],
                "answer": 1,
                "explanation": "With she, the present-simple verb usually takes -s: walks."
            },
            {
                "id": "en3", "title": "Asking questions",
                "duration": 10, "difficulty": "Growing",
                "content": "Questions help us start conversations and get information. Many present-simple questions use do or does. Use does with he, she, or it, and do with I, you, we, and they.",
                "example": "Do you like music?\nDoes she study English?\nWhere do they live?",
                "tip": "After does, use the base verb: 'Does she like…?' not 'Does she likes…?'",
                "question": "Which question is correct?",
                "options": ["Does he plays?", "Do he play?", "Does he play?", "He does play?"],
                "answer": 2,
                "explanation": "Use does with he, followed by the base verb play."
            },
            {
                "id": "en4", "title": "Useful everyday vocabulary",
                "duration": 8, "difficulty": "Growing",
                "content": "Vocabulary grows through repeated use. Learn words in short phrases and real situations rather than memorizing isolated lists. Try using a new word in a sentence today.",
                "example": "Improve: I want to improve my speaking.\nPrefer: I prefer tea to coffee.\nUsually: I usually wake up early.",
                "tip": "Choose three useful words and say one true sentence with each of them.",
                "question": "What does 'prefer' mean?",
                "options": ["Like one thing more", "Forget something", "Arrive late", "Speak loudly"],
                "answer": 0,
                "explanation": "To prefer something means to like or choose it more than another option."
            },
            {
                "id": "en5", "title": "Everyday conversation",
                "duration": 10, "difficulty": "Practice",
                "content": "A conversation is a shared exchange. You can keep it going by answering, adding one small detail, and asking a related question. You do not need a perfect sentence to connect with someone.",
                "example": "A: What did you do today?\nB: I went to college. We had a Python class. How was your day?",
                "tip": "Try the answer + detail + question pattern when you don't know what to say next.",
                "question": "What can help continue a conversation?",
                "options": ["Only saying yes", "Answering and asking a related question", "Changing the topic every time", "Staying silent"],
                "answer": 1,
                "explanation": "A small detail and a related question give the other person something to respond to."
            }
        ]
    },
    "datascience": {
        "name": "Data Science",
        "description": "Explore data, patterns, and insights.",
        "color": "green",
        "lessons": [
            {
                "id": "ds1", "title": "What is Data Science?",
                "duration": 8, "difficulty": "Beginner",
                "content": "Data Science combines data, programming, statistics, and problem-solving to answer questions. It can help people understand trends, make predictions, and support decisions.",
                "example": "A shop could study sales data to learn which products sell most often and during which months.",
                "tip": "Start with a question. Data becomes useful when you know what you want to understand.",
                "question": "What is one purpose of Data Science?",
                "options": ["Decorating documents", "Finding patterns in data", "Only designing logos", "Replacing all decisions"],
                "answer": 1,
                "explanation": "Data Science helps explore information and find patterns that can answer questions."
            },
            {
                "id": "ds2", "title": "Introduction to DataFrames",
                "duration": 10, "difficulty": "Beginner",
                "content": "A DataFrame is a table-like structure with rows and columns. In Python, pandas provides DataFrames for organizing, exploring, and analysing data.",
                "example": "Name     Score\nAsha       90\nMia        85\n\nEach row is a record; each column is a variable.",
                "tip": "Think of a DataFrame as a spreadsheet you can work with using Python.",
                "question": "What does a DataFrame look like?",
                "options": ["A table with rows and columns", "A single number only", "An image filter", "A computer folder"],
                "answer": 0,
                "explanation": "A DataFrame organizes data in a two-dimensional table."
            },
            {
                "id": "ds3", "title": "NumPy basics",
                "duration": 12, "difficulty": "Growing",
                "content": "NumPy is a Python library for working with numerical data. Its main structure is the ndarray, an array that can hold values in one or more dimensions and supports efficient numerical operations.",
                "example": "import numpy as np\nscores = np.array([80, 90, 70])\nprint(scores.mean())\n# 80.0",
                "tip": "NumPy is especially useful when you need to perform calculations on many numbers.",
                "question": "What is NumPy mainly used for?",
                "options": ["Numerical computing", "Writing novels", "Making phone calls", "Editing audio only"],
                "answer": 0,
                "explanation": "NumPy provides arrays and tools for numerical computing."
            },
            {
                "id": "ds4", "title": "Cleaning data",
                "duration": 12, "difficulty": "Growing",
                "content": "Real datasets can contain missing values, duplicates, inconsistent labels, or incorrect entries. Data cleaning helps make information more consistent and useful before analysis.",
                "example": "A table might contain:\nAge: 20, 21, blank, 19\n\nYou should inspect the missing age and decide how to handle it.",
                "tip": "Never remove or change data blindly. First understand what is missing or inconsistent and why it matters.",
                "question": "What is a common data-cleaning task?",
                "options": ["Adding random values", "Finding missing values", "Deleting every row", "Changing all numbers to text"],
                "answer": 1,
                "explanation": "Identifying missing values is a common first step in data cleaning."
            },
            {
                "id": "ds5", "title": "Charts and visualisation",
                "duration": 10, "difficulty": "Practice",
                "content": "Data visualisation uses charts to communicate patterns and comparisons. Bar charts compare categories, line charts show change over an ordered sequence, and scatter plots show relationships between numerical variables.",
                "example": "Use a bar chart to compare the number of books read by different students. Use a line chart to show temperature changes across a week.",
                "tip": "Choose a chart based on the question you're asking, and label it so people can understand it.",
                "question": "Which chart is commonly used to show change over time?",
                "options": ["Line chart", "Pie chart only", "Word cloud", "Icon list"],
                "answer": 0,
                "explanation": "A line chart is commonly used to show how values change over time."
            }
        ]
    }
}


QUIZZES = {
    "python": [
        ("Which function displays output?", ["input()", "print()", "type()", "range()"], 1),
        ("Which symbol assigns a value?", ["=", "==", "!=", ">"], 0),
        ("Which type stores True or False?", ["str", "float", "bool", "int"], 2)
    ],
    "math": [
        ("What is 10% of 80?", ["4", "8", "10", "18"], 1),
        ("Which fraction equals 3/6?", ["1/2", "1/3", "2/3", "3/4"], 0),
        ("What is the mean of 2, 4, 6?", ["2", "3", "4", "6"], 2)
    ],
    "english": [
        ("Choose the correct sentence.", ["He go home.", "He goes home.", "He going home.", "He gone home."], 1),
        ("Which is a verb?", ["quickly", "blue", "dance", "table"], 2),
        ("Choose the correct question.", ["Does she like tea?", "Does she likes tea?", "Do she likes tea?", "She does like tea?"], 0)
    ],
    "datascience": [
        ("Which library is used for DataFrames?", ["pandas", "turtle", "pygame", "random"], 0),
        ("What is a common use of NumPy?", ["Numerical computing", "Video calling", "Email", "Web browsing"], 0),
        ("Which chart often shows change over time?", ["Line chart", "Word cloud", "Icon grid", "Flowchart"], 0)
    ]
}


BADGES = [
    {"id": "first_lesson", "name": "First Steps", "description": "Complete your first lesson.", "icon": "🌱", "kind": "lessons", "target": 1},
    {"id": "five_lessons", "name": "Little Learner", "description": "Complete 5 lessons.", "icon": "📚", "kind": "lessons", "target": 5},
    {"id": "ten_lessons", "name": "Curious Mind", "description": "Complete 10 lessons.", "icon": "🧠", "kind": "lessons", "target": 10},
    {"id": "first_quiz", "name": "Quiz Explorer", "description": "Finish your first quiz.", "icon": "⭐", "kind": "quizzes", "target": 1},
    {"id": "three_day", "name": "Three-Day Spark", "description": "Build a 3-day streak.", "icon": "🔥", "kind": "streak", "target": 3},
    {"id": "seven_day", "name": "Weekly Wonder", "description": "Build a 7-day streak.", "icon": "🏆", "kind": "streak", "target": 7},
    {"id": "all_subjects", "name": "All-Rounder", "description": "Study every subject.", "icon": "🌈", "kind": "subjects", "target": 4}
]


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                name TEXT NOT NULL DEFAULT 'Varshitha',
                level TEXT NOT NULL DEFAULT 'Beginner',
                focus TEXT NOT NULL DEFAULT 'Learning something new'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lesson_progress (
                lesson_id TEXT PRIMARY KEY,
                subject TEXT NOT NULL,
                completed_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS study_days (
                study_date TEXT PRIMARY KEY
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                attempted_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_goal (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                target INTEGER NOT NULL DEFAULT 1
            )
        """)
        conn.execute(
            "INSERT OR IGNORE INTO profile (id, name, level, focus) VALUES (1, 'Varshitha', 'Beginner', 'Learning something new')"
        )
        conn.execute(
            "INSERT OR IGNORE INTO daily_goal (id, target) VALUES (1, 1)"
        )


def get_streak(conn):
    days = {
        row["study_date"]
        for row in conn.execute("SELECT study_date FROM study_days")
    }
    today = date.today()
    check = today if today.isoformat() in days else today - timedelta(days=1)
    streak = 0
    while check.isoformat() in days:
        streak += 1
        check -= timedelta(days=1)
    return streak


def get_badges(conn, completed, quiz_count, streak):
    studied_subjects = {
        row["subject"]
        for row in conn.execute("SELECT DISTINCT subject FROM lesson_progress")
    }
    unlocked = []
    for badge in BADGES:
        kind = badge["kind"]
        if kind == "lessons":
            earned = completed >= badge["target"]
        elif kind == "quizzes":
            earned = quiz_count >= badge["target"]
        elif kind == "streak":
            earned = streak >= badge["target"]
        else:
            earned = len(studied_subjects) >= badge["target"]
        unlocked.append({**badge, "unlocked": earned})
    return unlocked


def dashboard_data(conn):
    profile = dict(conn.execute("SELECT * FROM profile WHERE id=1").fetchone())
    completed_rows = conn.execute(
        "SELECT lesson_id, subject, completed_at FROM lesson_progress"
    ).fetchall()
    completed_ids = {r["lesson_id"] for r in completed_rows}
    completed = len(completed_ids)
    total = sum(len(s["lessons"]) for s in SUBJECTS.values())
    streak = get_streak(conn)
    quiz_count = conn.execute("SELECT COUNT(*) FROM quiz_attempts").fetchone()[0]
    today = date.today().isoformat()
    today_completed = conn.execute(
        "SELECT COUNT(*) FROM lesson_progress WHERE substr(completed_at,1,10)=?",
        (today,)
    ).fetchone()[0]
    goal = conn.execute("SELECT target FROM daily_goal WHERE id=1").fetchone()["target"]
    week_start = date.today() - timedelta(days=date.today().weekday())
    week = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        week.append({
            "date": day.isoformat(),
            "label": day.strftime("%a"),
            "number": day.day,
            "studied": conn.execute(
                "SELECT 1 FROM study_days WHERE study_date=?",
                (day.isoformat(),)
            ).fetchone() is not None,
            "today": day == date.today()
        })
    subjects = []
    for key, subject in SUBJECTS.items():
        ids = {lesson["id"] for lesson in subject["lessons"]}
        count = len(ids & completed_ids)
        subjects.append({
            "id": key,
            "name": subject["name"],
            "description": subject["description"],
            "total": len(ids),
            "completed": count
        })
    percent = round((completed / total) * 100) if total else 0
    goal_percent = min(100, round((today_completed / goal) * 100)) if goal else 0
    return {
        "profile": profile,
        "completed": completed,
        "total_lessons": total,
        "progress": percent,
        "streak": streak,
        "quiz_attempts": quiz_count,
        "today_completed": today_completed,
        "goal": goal,
        "goal_percent": goal_percent,
        "goal_reached": today_completed >= goal,
        "week": week,
        "badges": get_badges(conn, completed, quiz_count, streak),
        "subjects": subjects
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/dashboard")
def dashboard():
    with connect() as conn:
        return jsonify(dashboard_data(conn))


@app.route("/api/profile", methods=["GET", "POST"])
def profile():
    with connect() as conn:
        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            name = str(data.get("name", "Varshitha")).strip()[:40] or "Learner"
            level = str(data.get("level", "Beginner")).strip()[:30]
            focus = str(data.get("focus", "")).strip()[:100]
            conn.execute(
                "UPDATE profile SET name=?, level=?, focus=? WHERE id=1",
                (name, level, focus)
            )
        row = conn.execute("SELECT * FROM profile WHERE id=1").fetchone()
        return jsonify(dict(row))


@app.route("/api/goal", methods=["POST"])
def update_goal():
    data = request.get_json(silent=True) or {}
    try:
        target = int(data.get("target", 1))
    except (TypeError, ValueError):
        return jsonify({"error": "Goal must be a number."}), 400
    target = max(1, min(10, target))
    with connect() as conn:
        conn.execute("UPDATE daily_goal SET target=? WHERE id=1", (target,))
        return jsonify({"target": target})


@app.route("/api/subjects")
def subjects():
    return jsonify([
        {
            "id": key,
            "name": value["name"],
            "description": value["description"],
            "total": len(value["lessons"])
        }
        for key, value in SUBJECTS.items()
    ])


@app.route("/api/lessons/<subject_id>")
def lessons(subject_id):
    subject = SUBJECTS.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404
    with connect() as conn:
        done = {
            row["lesson_id"] for row in
            conn.execute("SELECT lesson_id FROM lesson_progress").fetchall()
        }
    items = []
    for lesson in subject["lessons"]:
        items.append({
            **lesson,
            "completed": lesson["id"] in done
        })
    return jsonify({
        "subject": {
            "id": subject_id,
            "name": subject["name"],
            "description": subject["description"]
        },
        "lessons": items
    })


@app.route("/api/lessons/<lesson_id>/complete", methods=["POST"])
def complete_lesson(lesson_id):
    subject_id = None
    for key, subject in SUBJECTS.items():
        if any(lesson["id"] == lesson_id for lesson in subject["lessons"]):
            subject_id = key
            break
    if not subject_id:
        return jsonify({"error": "Lesson not found"}), 404
    today = date.today().isoformat()
    with connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO lesson_progress (lesson_id, subject, completed_at) VALUES (?, ?, ?)",
            (lesson_id, subject_id, datetime.now().isoformat(timespec="seconds"))
        )
        conn.execute(
            "INSERT OR IGNORE INTO study_days (study_date) VALUES (?)",
            (today,)
        )
        return jsonify({"success": True, "dashboard": dashboard_data(conn)})


@app.route("/api/quick-check/<lesson_id>", methods=["POST"])
def quick_check(lesson_id):
    lesson = None
    for subject in SUBJECTS.values():
        lesson = next((x for x in subject["lessons"] if x["id"] == lesson_id), None)
        if lesson:
            break
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    data = request.get_json(silent=True) or {}
    try:
        answer = int(data.get("answer", -1))
    except (TypeError, ValueError):
        answer = -1
    return jsonify({
        "correct": answer == lesson["answer"],
        "correct_index": lesson["answer"],
        "explanation": lesson["explanation"]
    })


@app.route("/api/quiz/<subject_id>")
def quiz(subject_id):
    if subject_id not in QUIZZES:
        return jsonify({"error": "Quiz not found"}), 404
    return jsonify({
        "subject": SUBJECTS[subject_id]["name"],
        "questions": [
            {"question": q, "options": opts}
            for q, opts, answer in QUIZZES[subject_id]
        ]
    })


@app.route("/api/quiz/<subject_id>/submit", methods=["POST"])
def submit_quiz(subject_id):
    if subject_id not in QUIZZES:
        return jsonify({"error": "Quiz not found"}), 404
    data = request.get_json(silent=True) or {}
    answers = data.get("answers", [])
    questions = QUIZZES[subject_id]
    review = []
    score = 0

    for i, (question, options, correct_index) in enumerate(questions):
        try:
            selected = int(answers[i])
        except (IndexError, TypeError, ValueError):
            selected = -1

        correct = selected == correct_index
        if correct:
            score += 1

        review.append({
            "question": question,
            "options": options,
            "selected": selected,
            "correct_index": correct_index,
            "correct": correct,
            "explanation": f"The correct answer is: {options[correct_index]}."
        })

    with connect() as conn:
        conn.execute(
            "INSERT INTO quiz_attempts (subject, score, total, attempted_at) VALUES (?, ?, ?, ?)",
            (subject_id, score, len(questions), datetime.now().isoformat(timespec="seconds"))
        )

    return jsonify({
        "score": score,
        "total": len(questions),
        "review": review,
        "message": "Amazing effort!" if score == len(questions) else "Every try helps you learn!"
    })


@app.route("/api/results")
def results():
    with connect() as conn:
        rows = conn.execute(
            "SELECT subject, score, total, attempted_at FROM quiz_attempts ORDER BY id DESC LIMIT 30"
        ).fetchall()
        return jsonify([dict(r) for r in rows])


@app.route("/api/badges")
def badges():
    with connect() as conn:
        data = dashboard_data(conn)
        return jsonify(data["badges"])


@app.route("/api/week")
def week():
    with connect() as conn:
        return jsonify(dashboard_data(conn)["week"])


# PEEP CHATBOT
# Rule-based tutor with explanations for common beginner questions.

def contains_any(text, words):
    return any(word in text for word in words)


def python_answer(message):
    # Data types
    if contains_any(message, [
        "what is int", "int in python", "integer", "int type",
        "explain int", "int()"
    ]):
        return (
            "🐣 int means integer. It is a Python data type for whole "
            "numbers without decimal points.\n\n"
            "Example:\n"
            "age = 20\n"
            "print(type(age))\n\n"
            "Output: <class 'int'>\n\n"
            "You can also use int() to convert a value:\n"
            "number = int('25')\n"
            "print(number)  # 25\n\n"
            "Remember: int('25') works because '25' contains a whole number."
        )

    if contains_any(message, [
        "what is float", "float in python", "float type",
        "decimal", "explain float", "float()"
    ]):
        return (
            "🐣 float is a Python data type for numbers with a decimal "
            "point.\n\n"
            "Example:\n"
            "price = 49.5\n"
            "print(type(price))\n\n"
            "Output: <class 'float'>\n\n"
            "You can convert a number or suitable text using float():\n"
            "value = float('3.14')"
        )

    if contains_any(message, [
        "what is str", "str in python", "string", "str type",
        "explain str", "str()"
    ]):
        return (
            "🐣 str means string. It is the Python data type used for "
            "text, such as names, words, and sentences.\n\n"
            "Example:\n"
            "name = 'Varshitha'\n"
            "print(type(name))\n\n"
            "Output: <class 'str'>\n\n"
            "str() can convert suitable values into text:\n"
            "age_text = str(20)\n"
            "print(age_text)  # '20'"
        )

    if contains_any(message, [
        "what is bool", "bool in python", "boolean",
        "bool type", "explain bool", "bool()"
    ]):
        return (
            "🐣 bool means Boolean. It has only two values: True and False. "
            "Booleans are often used in conditions.\n\n"
            "Example:\n"
            "is_ready = True\n"
            "print(type(is_ready))\n\n"
            "Output: <class 'bool'>\n\n"
            "Example condition:\n"
            "if is_ready:\n"
            "    print('Let us start!')"
        )

    if contains_any(message, [
        "data type", "data types", "type of", "type()",
        "check type", "check data"
    ]):
        return (
            "🐣 A data type tells Python what kind of value something is.\n\n"
            "int = whole numbers, like 20\n"
            "float = decimal numbers, like 3.5\n"
            "str = text, like 'hello'\n"
            "bool = True or False\n\n"
            "Use type() to check a value:\n"
            "print(type(20))  # int\n"
            "print(type(3.5))  # float\n"
            "print(type('hi'))  # str"
        )

    # Variables
    if contains_any(message, ["variable", "variables"]):
        return (
            "🐣 A variable is a name that refers to a value.\n\n"
            "Example:\n"
            "score = 10\n"
            "name = 'Mia'\n"
            "print(score)\n\n"
            "Here, score refers to 10. The = sign assigns a value; "
            "it is not the same as ==, which compares values."
        )

    # print and input
    if contains_any(message, ["print", "display output", "show output"]):
        return (
            "🐣 print() displays information in the output area.\n\n"
            "Example:\n"
            "print('Hello!')\n\n"
            "Output:\n"
            "Hello!\n\n"
            "You can print variables too:\n"
            "age = 20\n"
            "print(age)"
        )

    if contains_any(message, ["input", "user input"]):
        return (
            "🐣 input() lets a program ask the user to type something.\n\n"
            "Example:\n"
            "name = input('Enter your name: ')\n"
            "print('Hello', name)\n\n"
            "Important: input() returns text (str). If you need a whole "
            "number, convert it with int()."
        )

    # Operators
    if contains_any(message, ["operator", "operators", "modulo", "remainder"]):
        return (
            "🐣 Operators perform actions on values.\n\n"
            "+ addition: 5 + 2 = 7\n"
            "- subtraction: 5 - 2 = 3\n"
            "* multiplication: 5 * 2 = 10\n"
            "/ division: 5 / 2 = 2.5\n"
            "% remainder: 5 % 2 = 1\n"
            "** power: 5 ** 2 = 25\n\n"
            "Try changing the numbers and predicting the result!"
        )

    # Conditions
    if contains_any(message, ["if statement", "condition", "elif", "else"]):
        return (
            "🐣 Conditions let Python make decisions.\n\n"
            "Example:\n"
            "age = 20\n"
            "if age >= 18:\n"
            "    print('Adult')\n"
            "else:\n"
            "    print('Under 18')\n\n"
            "if checks a condition. else runs when the if condition "
            "is false. elif lets you check another condition."
        )

    # Loops
    if contains_any(message, ["loop", "loops", "for loop", "while loop", "range"]):
        return (
            "🐣 A loop repeats code.\n\n"
            "A for loop example:\n"
            "for i in range(1, 4):\n"
            "    print(i)\n\n"
            "Output:\n"
            "1\n2\n3\n\n"
            "range(1, 4) gives 1, 2, and 3. The ending number, 4, "
            "is not included. A while loop repeats while its condition is true."
        )

    # Functions
    if contains_any(message, ["function", "functions", "def ", "return"]):
        return (
            "🐣 A function is a reusable block of code. You define one "
            "with def.\n\n"
            "Example:\n"
            "def greet():\n"
            "    print('Hello!')\n\n"
            "greet()\n\n"
            "The line greet() calls the function, so its code runs. "
            "Functions help organize programs and avoid repeating code."
        )

    # Lists
    if contains_any(message, ["list", "lists", "append", "index"]):
        return (
            "🐣 A list stores multiple items in one variable.\n\n"
            "Example:\n"
            "fruits = ['apple', 'mango', 'grape']\n"
            "print(fruits[0])  # apple\n\n"
            "Python list indexes start at 0. Use append() to add an item:\n"
            "fruits.append('orange')"
        )

    # Dictionaries
    if contains_any(message, ["dictionary", "dict", "key value", "keys"]):
        return (
            "🐣 A dictionary stores information as key-value pairs.\n\n"
            "Example:\n"
            "student = {'name': 'Mia', 'age': 20}\n"
            "print(student['name'])  # Mia\n\n"
            "Here, 'name' is a key and 'Mia' is its value."
        )

    # Errors
    if contains_any(message, ["error", "bug", "exception", "traceback"]):
        return (
            "🐣 Errors are clues that something went wrong. Read the "
            "last line of the error first; it often tells you the error type.\n\n"
            "Common examples:\n"
            "SyntaxError = code structure is invalid\n"
            "NameError = a name is not defined\n"
            "TypeError = an operation used an unsuitable type\n"
            "IndentationError = indentation is incorrect\n\n"
            "Paste your error message here and I can help explain it."
        )

    return None


def chat_reply(message):
    msg = " ".join(message.lower().strip().split())

    if not msg:
        return "Type a question and I'll help you out! 🌼"

    if contains_any(msg, ["hello", "hi", "hey", "hii"]):
        return "Hiii! 🌼 I'm Peep, your study buddy. What are we learning today?"

    answer = python_answer(msg)
    if answer:
        return answer

    if contains_any(msg, ["percentage", "percent"]):
        return (
            "🌷 Percent means out of 100. To find 20% of 50, calculate "
            "20/100 × 50 = 10.\n\n"
            "Try one: what's 10% of 90?"
        )

    if contains_any(msg, ["fraction", "fractions"]):
        return (
            "🌷 A fraction represents part of a whole. The numerator is "
            "the top number and the denominator is the bottom number.\n\n"
            "For example, 1/2 means one of two equal parts. "
            "2/4 is equivalent to 1/2."
        )

    if contains_any(msg, ["dataframe", "pandas"]):
        return (
            "🌷 A pandas DataFrame is like a spreadsheet: it has rows "
            "and columns. Each row is usually one record, and each "
            "column represents a variable.\n\n"
            "Example:\n"
            "import pandas as pd\n"
            "df = pd.DataFrame({'Name': ['Mia'], 'Score': [90]})"
        )

    if contains_any(msg, ["numpy", "ndarray", "array"]):
        return (
            "🌷 NumPy is a Python library for numerical computing. "
            "Its main structure is the ndarray, which stores values "
            "in one or more dimensions.\n\n"
            "Example:\n"
            "import numpy as np\n"
            "numbers = np.array([1, 2, 3])"
        )

    if contains_any(msg, ["english", "speak", "conversation"]):
        return (
            "🌷 Try this speaking trick: answer, add one detail, then "
            "ask a related question.\n\n"
            "Example: 'I went to class. We learned Python. What did "
            "you do today?'"
        )

    if contains_any(msg, ["streak"]):
        return (
            "🔥 Your streak grows when you study on different days. "
            "Even one completed lesson can count as today's learning "
            "session. Keep it gentle and consistent!"
        )

    if contains_any(msg, ["motivate", "lazy", "tired", "can't", "cannot"]):
        return (
            "You don't need to do everything right now. 💗 Pick one "
            "tiny task and give it five minutes. Starting is a win too."
        )

    if contains_any(msg, ["help", "teach", "explain"]):
        return (
            "Of course! 🐣 Ask me about a topic, and I'll try to explain "
            "it in simple steps with an example. You can ask about "
            "Python, Mathematics, English, or Data Science."
        )

    return (
        "Hmm, I'm not sure about that one yet. 🐣 "
        "Try asking in a different way, or tell me the subject and "
        "the exact topic. For Python, you can ask about int, float, "
        "str, bool, variables, loops, conditions, or functions."
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    return jsonify({"reply": chat_reply(message)})


if __name__ == "__main__":
    init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)