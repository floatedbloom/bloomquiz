import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

#Plan - quiz website with preloaded quizzes and quiz creation

#Set up is from finance
#Login and register system is from finance

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

#From finance
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """Escape special characters."""
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    try:
        if request.method == "GET":
            return render_template("register.html")
        else:
            try:
                username = request.form.get("username")
                password = request.form.get("password")
                confirm = request.form.get("confirmation")

                if not confirm or not password or not username:
                    return apology("Input into all fields")
                n = db.execute("SELECT * FROM users WHERE username=?", username)

                if password == confirm:
                    if len(n) != 0:
                        return apology("Username taken")
                    else:
                        hash = generate_password_hash(
                            password, method="pbkdf2", salt_length=16
                        )
                        db.execute(
                            "INSERT INTO users (username, hash, type) VALUES(?,?,?)",
                            username,
                            hash,
                            1,
                        )
                        new_user = db.execute(
                            "SELECT id FROM users WHERE username=?", username
                        )
                        session["user_id"] = new_user[0]["id"]
                        return redirect("/")
                else:
                    return apology("Passwords don't match")

            except (ValueError, KeyError, IndexError):
                return apology("Error")

    except (ValueError, KeyError, IndexError, TypeError):
        return apology("Error")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password"""
    if request.method == "GET":
        return render_template("change.html")
    else:
        user_id = session["user_id"]
        old_hash_dict = db.execute("SELECT hash FROM users WHERE id=?", user_id)
        old_hash = old_hash_dict[0]["hash"]
        input_pass = request.form.get("current")
        input_new = request.form.get("new")
        input_confirm = request.form.get("confirm")
        if input_pass is None or input_confirm is None or input_new is None:
            return apology("Input into all fields")
        else:
            if input_new == input_confirm:
                if check_password_hash(old_hash, input_pass):
                    return apology("New password can't be the same as current password")
                else:
                    new_hash = generate_password_hash(
                        input_new, method="pbkdf2", salt_length=16
                    )
                    db.execute("UPDATE users SET hash=? WHERE id=?", new_hash, user_id)
                    return redirect("/")
            else:
                return apology("New passwords don't match")

@app.route("/")
@login_required
def home():
    stats = db.execute("SELECT * FROM stats WHERE id=?", session["user_id"])
    return render_template("home.html", stats=stats)

@app.route("/cs50",methods=["GET", "POST"])
@login_required
def cs50():
    if request.method == "GET":
        return render_template("cs50.html")
    else:
        selected = {}
        amount = 5
        question_count = 0
        for i in range(1, amount+1):
            current = f'question_{i}'
            selected[current] = request.form.get(current)
            question_count += 1
        corrects = 0
        for j in range(1, question_count + 1):
            n = f'question_{j}'
            if selected[n] == 'correct':
                corrects += 1
            else:
                continue
        percent = (float(corrects) / float(question_count)) * 100
        topic = "CS50 Quiz"
        db.execute("INSERT INTO stats VALUES(?,?,?,?,?)",session["user_id"],corrects,question_count,percent,topic)
        return render_template("result.html", questions=question_count, corrects=corrects, percent=percent, topic=topic)

@app.route("/math",methods=["GET", "POST"])
@login_required
def math():
    if request.method == "GET":
        return render_template("math.html")
    else:
        selected = {}
        amount = 5
        question_count = 0
        for i in range(1, amount + 1):
            current = f'question_{i}'
            selected[current] = request.form.get(current)
            question_count += 1
        corrects = 0
        for j in range(1, question_count + 1):
            n = f'question_{j}'
            if selected[n] == 'correct':
                corrects += 1
            else:
                continue
        percent = float(corrects) / float(question_count)
        percent = percent * 100
        topic = "Math Quiz"
        db.execute("INSERT INTO stats VALUES(?,?,?,?,?)",session["user_id"],corrects,question_count,percent,topic)
        return render_template("result.html", questions=question_count, corrects=corrects, percent=percent, topic=topic)

@app.route("/grammar",methods=["GET", "POST"])
@login_required
def grammar():
    if request.method == "GET":
        return render_template("grammar.html")
    else:
        selected = {}
        amount = 5
        question_count = 0
        for i in range(1, amount + 1):
            current = f'question_{i}'
            selected[current] = request.form.get(current)
            question_count += 1
        corrects = 0
        for j in range(1, question_count + 1):
            n = f'question_{j}'
            if selected[n] == 'correct':
                corrects += 1
            else:
                continue
        percent = float(corrects) / float(question_count)
        percent = percent * 100
        topic = "Grammar Quiz"
        db.execute("INSERT INTO stats VALUES(?,?,?,?,?)",session["user_id"],corrects,question_count,percent,topic)
        return render_template("result.html", questions=question_count, corrects=corrects, percent=percent, topic=topic)

@app.route("/create",methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        difficulty = request.form.get("difficulty")
        quiz_title = request.form.get("quiz_title")
        if not quiz_title or not difficulty:
            return apology("Fill in all fields")
        else:
            difficulty = int(difficulty)
            quiz_id = db.execute("INSERT INTO quizzes (user,name, difficulty) VALUES (?,?,?)",session["user_id"],quiz_title, difficulty)
            for i in range(1,5):
                question_text = request.form.get(f"{i}_text")
                answer_1 = request.form.get(f"{i}_1")
                answer_2 = request.form.get(f"{i}_2")
                answer_3 = request.form.get(f"{i}_3")
                answer_4 = request.form.get(f"{i}_4")
                correct = request.form.get(f"{i}_correct")
                if not question_text or not answer_1 or not answer_2 or not answer_3 or not answer_4 or not correct:
                    return apology("Fill in all fields")
                else:
                    db.execute("INSERT INTO questions (quiz_id, question_text, answer_1, answer_2, answer_3, answer_4, correct_answer) VALUES (?,?,?,?,?,?,?)",quiz_id, question_text, answer_1, answer_2, answer_3, answer_4, correct)

            flash('Quiz created successfully!')
            return redirect("/")

@app.route("/result")
@login_required
def result():
    return render_template("result.html")

@app.route("/quizzes")
@login_required
def quizzes():
    quizzes = db.execute("SELECT * FROM quizzes WHERE user=?", session["user_id"])
    return render_template("quizzes.html", quizzes=quizzes)

@app.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def open_quiz(quiz_id):
    if request.method == "GET":
        quiz = db.execute("SELECT * FROM quizzes WHERE id=?", quiz_id)
        questions = db.execute("SELECT * FROM questions WHERE quiz_id=?", quiz_id)
        return render_template("quiz.html", quiz=quiz, questions=questions)
    else:
        questions = db.execute("SELECT * FROM questions WHERE quiz_id=?", quiz_id)
        quiz = db.execute("SELECT * FROM quizzes WHERE id=?", quiz_id)
        answers = {}
        for question in questions:
            question_id = question['id']
            answer = request.form.get(f"question_{question_id}")
            answers[f"question_{question_id}"] = answer

        corrects = 0

        for question in questions:
            question_id = question['id']
            answer = answers.get(f"question_{question_id}")
            if answer is not None:
                correct_answer = question['correct_answer']
                if int(answer) == correct_answer:
                    corrects += 1

        print(corrects)
        percent = (float(corrects)/float(4))*100
        topic = f"{quiz[0]["name"]} Quiz"

        db.execute("INSERT INTO stats VALUES(?,?,?,?,?)",session["user_id"],corrects,4,percent,topic)
        return render_template("result.html", questions=4, corrects=corrects, percent=percent, topic=topic)

