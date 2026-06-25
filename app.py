from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks")
def tasks():
    return "Tasks Page"

@app.route("/Cat")
def about():
    return "About Cat"

if __name__ == "__main__":
    app.run(debug=True)