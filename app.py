from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
from collections import Counter
import os

app = Flask(__name__)
CORS(app)

DATABASE = "mindmate.db"


# ----------------------------
# DATABASE INITIALIZATION
# ----------------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    


    # Mood tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Journals
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Breathing sessions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS breathing_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT NOT NULL,
            duration INTEGER,
            date TEXT NOT NULL
        )
    """)

    # Grounding sessions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grounding_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Anger logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS anger_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Overwhelm reflections
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS overwhelm_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Focus sessions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration INTEGER,
            completed INTEGER,
            date TEXT NOT NULL
        )
    """)

    # Quick reset actions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quick_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    

    conn.commit()
    conn.close()


init_db()


# ----------------------------
# ADD MOOD
# ----------------------------
@app.route('/add_mood', methods=['POST'])
def add_mood():
    data = request.get_json()
    mood = data.get("mood")

    if not mood:
        return jsonify({"error": "Mood required"}), 400

    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO moods (mood, date) VALUES (?, ?)", (mood.lower(), today))
    conn.commit()
    conn.close()

    return jsonify({"message": f"{mood.capitalize()} mood saved 💛"})


# ----------------------------
# SAVE JOURNAL
# ----------------------------
@app.route('/add_journal', methods=['POST'])
def add_journal():
    data = request.get_json()
    mood = data.get("mood")
    content = data.get("content")

    if not mood or not content:
        return jsonify({"error": "Mood and content required"}), 400

    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO journals (mood, content, date) VALUES (?, ?, ?)",
        (mood.lower(), content, today)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Your thoughts are safely saved 💛"})


# ----------------------------
# GET JOURNALS
# ----------------------------
@app.route('/get_journals', methods=['GET'])
def get_journals():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT mood, content, date FROM journals ORDER BY id DESC")
    entries = cursor.fetchall()
    conn.close()

    journal_list = [
        {"mood": row[0], "content": row[1], "date": row[2]}
        for row in entries
    ]

    return jsonify(journal_list)


# ----------------------------
# BREATHING COMPLETED
# ----------------------------
@app.route('/breathing_complete', methods=['POST'])
def breathing_complete():
    data = request.get_json()
    mood = data.get("mood")
    duration = data.get("duration", 30)

    if not mood:
        return jsonify({"error": "Mood required"}), 400

    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO breathing_sessions (mood, duration, date) VALUES (?, ?, ?)",
        (mood.lower(), duration, today)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Breathing session logged 🌬️"})


# ----------------------------
# GROUNDING COMPLETED
# ----------------------------
@app.route('/grounding_complete', methods=['POST'])
def grounding_complete():
    data = request.get_json()
    mood = data.get("mood")

    if not mood:
        return jsonify({"error": "Mood required"}), 400

    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO grounding_sessions (mood, date) VALUES (?, ?)",
        (mood.lower(), today)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Grounding exercise completed 🌿"})


# ----------------------------
# ANGER VENT SAVE
# ----------------------------
@app.route('/vent_anger', methods=['POST'])
def vent_anger():
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Content required"}), 400

    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO anger_logs (content, date) VALUES (?, ?)",
        (content, today)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Vent released safely 🌶️"})


# ----------------------------
# SAVE OVERWHELM
# ----------------------------
@app.route('/save_overwhelm', methods=['POST'])
def save_overwhelm():
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Content required"}), 400

    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO overwhelm_entries (content, date) VALUES (?, ?)",
        (content, today)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "You're not carrying this alone 💜"})


# ----------------------------
# FOCUS SESSION COMPLETE
# ----------------------------
@app.route('/focus_complete', methods=['POST'])
def focus_complete():
    data = request.get_json()
    duration = data.get("duration", 25)
    completed = data.get("completed", True)

    completed = 1 if completed else 0
    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO focus_sessions (duration, completed, date) VALUES (?, ?, ?)",
        (duration, completed, today)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Momentum built 🌟"})


# ----------------------------
# QUICK RESET
# ----------------------------
@app.route('/quick_reset', methods=['POST'])
def quick_reset():
    data = request.get_json()
    action = data.get("action")

    if not action:
        return jsonify({"error": "Action required"}), 400

    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quick_resets (action, date) VALUES (?, ?)",
        (action, today)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Small reset done 🌿"})


# ----------------------------
# DASHBOARD SUMMARY
# ----------------------------
@app.route('/dashboard_summary', methods=['GET'])
def dashboard_summary():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM moods")
    moods = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM journals")
    journals = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM breathing_sessions")
    breathing = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM grounding_sessions")
    grounding = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM overwhelm_entries")
    overwhelm = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM focus_sessions")
    focus = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM quick_resets")
    resets = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "total_moods_logged": moods,
        "journals_written": journals,
        "breathing_sessions": breathing,
        "grounding_sessions": grounding,
        "overwhelm_entries": overwhelm,
        "focus_sessions": focus,
        "quick_resets": resets
    })
# ----------------------------
# REGISTER USER
# ----------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not full_name or not email or not password or not confirm_password:
        return jsonify({"error": "All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (full_name, email, password, created_at)
            VALUES (?, ?, ?, ?)
        """, (full_name, email.lower(), hashed_password, today))

        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Email already registered"}), 400

    conn.close()

    return jsonify({"message": "Account created successfully 🌱"})
# ----------------------------
# LOGIN USER
# ----------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    
  

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, full_name, password FROM users WHERE email = ?", (email.lower(),))
    user = cursor.fetchone()

    conn.close()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    user_id, full_name, stored_password = user

    if not check_password_hash(stored_password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful 💚",
        "user": {
            "id": user_id,
            "full_name": full_name,
            "email": email
        }
    })


# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "MindMate backend running 💚"})
# ----------------------------
# WEEKLY MOOD DATA
# ----------------------------
@app.route('/weekly_moods', methods=['GET'])
def weekly_moods():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get last 7 days moods
    cursor.execute("""
        SELECT mood, date 
        FROM moods 
        WHERE date >= date('now', '-6 days')
        ORDER BY date ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    mood_data = {}

    for mood, date in rows:
        mood_data[date] = mood.capitalize()

    return jsonify(mood_data)


# ----------------------------
# RUN SERVER
# ----------------------------
if __name__ == '__main__':
   port = int(os.environ.get("PORT", 10000))
   app.run(host="0.0.0.0", port=port, debug=True)