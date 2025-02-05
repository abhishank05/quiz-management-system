#starting of app
from flask import Flask,render_template
from flask import current_app as app

@app.route("/")
def home():
    return render_template("index.html")

# Many controllers/Routes here