from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def today():
    return render_template("today.html")

@app.route("/upcoming")
def upcoming():
    return "Upcoming Tasks Page"

@app.route("/Cat")
def about():
    return "Cat Page"

if __name__ == "__main__":
    app.run(debug=True)