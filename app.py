import os
from functools import wraps

import bcrypt
import pymysql
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]


def run(sql, params=(), fetch=None):
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database="registration",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            if fetch == "one":
                return cur.fetchone()
            if fetch == "all":
                return cur.fetchall()
            return cur.rowcount
    finally:
        conn.close()


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper


def find_user(email):
    return run(
        "SELECT user_id, name, password_hash FROM users WHERE email = %s",
        (email,), "one",
    )


def start_session(user):
    session.clear()
    session["user_id"] = user["user_id"]
    session["name"] = user["name"]


def check_title(raw):
    title = raw.strip()
    if not title:
        return title, "Title is required"
    if len(title) > 200:
        return title, "Title is too long (200 characters at most)"
    return title, ""


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", errors={}, form={})

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    errors = {}
    if not name:
        errors["name"] = "Name is required"
    if not email:
        errors["email"] = "Email is required"
    if not password:
        errors["password"] = "Password is required"
    if not confirm:
        errors["confirm_password"] = "Confirm password is required"
    elif password and password != confirm:
        errors["confirm_password"] = "Passwords do not match"
    if errors:
        return render_template("register.html", errors=errors, form=request.form)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()
    try:
        run(
            "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
            (email, name, hashed),
        )
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            errors["email"] = "Email Already Exists"
            return render_template("register.html", errors=errors, form=request.form)
        raise

    start_session(find_user(email))
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", errors={}, form={})

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    errors = {}
    if not email:
        errors["email"] = "Email is required"
    if not password:
        errors["password"] = "Password is required"
    if errors:
        return render_template("login.html", errors=errors, form=request.form)

    user = find_user(email)
    if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        start_session(user)
        return redirect(url_for("index"))

    errors["general"] = "Invalid email or password"
    return render_template("login.html", errors=errors, form=request.form)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


def show(**ctx):
    todos = run(
        "SELECT todo_id, title, is_done, created_at FROM todos "
        "WHERE user_id = %s ORDER BY todo_id DESC",
        (session["user_id"],), "all",
    )
    return render_template("todos.html", todos=todos, **ctx)


@app.route("/")
@login_required
def index():
    return show()


@app.route("/add", methods=["POST"])
@login_required
def add():
    title, error = check_title(request.form.get("title", ""))
    if error:
        return show(add_title=request.form.get("title", ""), add_error=error)
    run("INSERT INTO todos (user_id, title) VALUES (%s, %s)", (session["user_id"], title))
    return redirect(url_for("index"))


@app.route("/edit/<int:todo_id>", methods=["POST"])
@login_required
def edit(todo_id):
    title, error = check_title(request.form.get("title", ""))
    if error:
        return show(edit_id=todo_id, edit_title=request.form.get("title", ""), edit_error=error)
    run(
        "UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
        (title, todo_id, session["user_id"]),
    )
    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>", methods=["POST"])
@login_required
def toggle(todo_id):
    value = 1 if request.form.get("is_done") == "1" else 0
    run(
        "UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s",
        (value, todo_id, session["user_id"]),
    )
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
@login_required
def delete(todo_id):
    run(
        "DELETE FROM todos WHERE todo_id = %s AND user_id = %s",
        (todo_id, session["user_id"]),
    )
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", message="This page does not exist."), 404


@app.errorhandler(Exception)
def server_error(e):
    app.logger.exception("Unhandled error")  # prints the real error in the terminal
    return render_template("error.html", message="Something went wrong. Please try again."), 500


if __name__ == "__main__":
    app.run(debug=False)
