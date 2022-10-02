from flask import Flask

app = Flask("JobsScrapper")

@app.route("/")
def home():
    return "Hello World!"

app.run("127.0.0.1")