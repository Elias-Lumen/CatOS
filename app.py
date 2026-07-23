from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("today_task.html")


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


@app.route("/cat")  # can here be the specific cat name of user?
def cat():
    return render_template("cat.html")


@app.route("/help")
def help():
    return render_template("help.html")


if __name__ == "__main__":
    app.run(debug=True)