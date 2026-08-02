from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database import create_tables  # connect database.py
from routes.auth import login_user, register_user # connect 


app = Flask(__name__)

app.config["SECRET_KEY"] = "flowist-development-secret-key"


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("today_task.html")


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


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/setting")
def setting():
    return render_template("setting.html")


@app.route("/task")
def task():
    return render_template("task.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/today")
def today_task():
    return render_template("today_task.html")


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