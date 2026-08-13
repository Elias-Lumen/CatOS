from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database import create_tables, create_task, get_tasks_by_user # connect database.py
from routes.auth import login_user, register_user # connect 


app = Flask(__name__)

app.config["SECRET_KEY"] = "CatOS-development-secret-key"


# home page and the today page is the same page
@app.route("/", methods=["GET", "POST"])
def home():
    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Add a new task
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "normal")# if don't select priority, it will be normal
        due_date = request.form.get("due_date") or None

        if title:
            create_task(
                user_id=session["user_id"],
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )

        return redirect(url_for("home"))

    # Get all tasks belonging to the current user
    tasks = get_tasks_by_user(session["user_id"])

    # Show tasks on the Today page
    return render_template(
        "today_task.html",
        tasks=tasks
    )

# register function
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        confirm_password = request.form.get(
            "confirm_password",
            "",
        )

        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("register.html")

        user = register_user(username, password)

        if user is None:
            flash(
                "Username already exists, or the form is incomplete."
            )
            return render_template("register.html")

        # if sign up successful, login derictly
        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(url_for("home"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])

# login function
def login():
    # user post login table
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user = login_user(username, password)

        if user is None:
            flash("Invalid username or password.")
            return render_template("login.html")

        # clean perious any login
        session.clear()

        # remember user
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(url_for("home"))

    # 用户只是打开 /login 页面
    return render_template("login.html")

# the botton in the setting to make sure can logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# setting 
@app.route("/setting")
def setting():
    return render_template("setting.html")


@app.route("/task", methods=["GET", "POST"])
def task():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "normal")
        due_date = request.form.get("due_date") or None

        if title:
            create_task(
                user_id=session["user_id"],
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )

        return redirect(url_for("task"))

    tasks = get_tasks_by_user(session["user_id"])

    return render_template(
        "task.html",
        tasks=tasks
    )
# this should be the fload task additor (CSS)
# 

@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/labels")
def labels():
    return render_template("labels.html")


@app.route("/upcoming")
def upcoming():
    return render_template("upcoming.html")


@app.route("/data")
def data():
    return render_template("data.html")


@app.route("/cat")
def cat():
    return render_template("cat.html")

# should add a use's individual cat name (maybe user can edit it?)

@app.route("/help")
def help():
    return render_template("help.html")


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)