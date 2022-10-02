from flask import Flask, render_template

app = Flask("JobsScrapper")

@app.route("/")
def home():
    return render_template("home.html")

app.run("127.0.0.1", debug=True)