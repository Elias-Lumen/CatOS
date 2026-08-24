from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from datetime import date

# bring the database functions over here
# otherwise app.py would have to do all the database work by itself
from database import (
    create_tables,
    create_task,
    get_tasks_by_user,
    toggle_task_completion,
    update_task,
    delete_task,
)

# login and register logic is kept in auth.py
# so app.py does not become one giant file
from routes.auth import login_user, register_user


app = Flask(__name__)

# Flask needs this for session and flash messages
# this is only a development key for now
app.config["SECRET_KEY"] = "CatOS-development-secret-key"


# home page and Today page are basically the same thing for now
@app.route("/", methods=["GET", "POST"])
def home():

    # no sneaking into the app without logging in first
    if "user_id" not in session:
        return redirect(url_for("login"))

    # if the user submits the task form, make a new task
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        # if the user does not choose one, just use normal
        priority = request.form.get("priority", "normal")

        # blank due date is easier to deal with as None
        due_date = request.form.get("due_date") or None

        # a task without a title is not very useful
        if title:
            create_task(
                user_id=session["user_id"],
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )

        # reload the page after adding the task
        # this also stops the form being submitted twice on refresh
        return redirect(url_for("home"))

    # only get tasks that belong to the current user
    tasks = get_tasks_by_user(session["user_id"])

    today_date = date.today()

    overdue_tasks = []
    today_tasks = []

    # send the tasks to the Today page so Jinja can display them
    for task in tasks:

        if task["due_date"]:
            task_date = date.fromisoformat(task["due_date"])

            if task_date < today_date:
                overdue_tasks.append(task)
            else:
                today_tasks.append(task)

        else:
            today_tasks.append(task)

    return render_template(
        "today_task.html",
        overdue_tasks=overdue_tasks,
        today_tasks=today_tasks,
        today=today_date.isoformat()
    )


    return render_template(
        "today_task.html",
        tasks=tasks,
        overdue_tasks=overdue_tasks,
        today_tasks=today_tasks,
        today=today_date.isoformat()
    )

@app.route("/task/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    toggle_task_completion(
        task_id=task_id,
        user_id=session["user_id"]
    )

    return redirect(url_for("home"))

@app.route("/task/<int:task_id>/edit", methods=["POST"])
def edit_task(task_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "normal")
    due_date = request.form.get("due_date") or None

    if title:
        update_task(
            task_id=task_id,
            user_id=session["user_id"],
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )

    return redirect(url_for("home"))

@app.route("/task/<int:task_id>/delete", methods=["POST"])
def remove_task(task_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_task(
        task_id=task_id,
        user_id=session["user_id"]
    )

    return redirect(url_for("home"))

# register page
@app.route("/register", methods=["GET", "POST"])
def register():

    # POST means the user actually pressed the register button
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        confirm_password = request.form.get(
            "confirm_password",
            "",
        )

        # stop here if they somehow typed two different passwords
        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("register.html")

        # auth.py does the actual account creation
        user = register_user(username, password)

        # None means something went wrong
        # usually duplicate username or missing information
        if user is None:
            flash(
                "Username already exists, or the form is incomplete."
            )
            return render_template("register.html")

        # registration worked
        # log the user in straight away because making them log in again is annoying
        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(url_for("home"))

    # if they only opened the page, just show the form
    return render_template("register.html")


# login page
@app.route("/login", methods=["GET", "POST"])
def login():

    # user pressed the login button
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # ask auth.py if these login details are actually correct
        user = login_user(username, password)

        # wrong username or password
        if user is None:
            flash("Invalid username or password.")
            return render_template("login.html")

        # remove anything left from an old login session
        session.clear()

        # remember who is logged in
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(url_for("home"))

    # they only opened /login, nothing exciting happened yet
    return render_template("login.html")


# log out button from Settings
@app.route("/logout")
def logout():

    # forget the current user completely
    session.clear()

    # send them back to login
    return redirect(url_for("login"))


# settings page
# avatar stuff will probably live here later
@app.route("/setting")
def setting():
    return render_template("setting.html")


# separate task page
# this is currently another place where tasks can be added
@app.route("/task", methods=["GET", "POST"])
def task():

    # same rule as Home: login first
    if "user_id" not in session:
        return redirect(url_for("login"))

    # user submitted a new task
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

    # get this user's tasks for the page
    tasks = get_tasks_by_user(session["user_id"])

    return render_template(
        "task.html",
        tasks=tasks
    )


# this page should eventually become the floating task editor
# currently still under construction
@app.route("/search")
def search():
    return render_template("search.html")


# filters and labels page
# need to be done
@app.route("/labels")
def labels():
    return render_template("labels.html")


# future tasks will go here
@app.route("/upcoming")
def upcoming():
    return render_template("upcoming.html")


# task data / progress page
@app.route("/data")
def data():
    return render_template("data.html")


# virtual cat page
@app.route("/cat")
def cat():
    return render_template("cat.html")


# later each user should probably have their own cat name
# maybe let them edit it in Settings too?


# help page
@app.route("/help")
def help():
    return render_template("help.html")


# only start the Flask server if this file is run directly
if __name__ == "__main__":

    # make sure all the database tables exist before CatOS starts
    create_tables()

    # debug=True is useful while developing
    # definitely not something I want forever
    app.run(debug=True)