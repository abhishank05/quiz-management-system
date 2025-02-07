#starting of app
from flask import Flask,render_template,request
from models.model1 import *
from flask import current_app as app

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        usr=User_Info.query().filter_by(email=uname,password=pwd).first()
        if usr:
            return render_template("admin_dashboard.html")

    return render_template("login.html")

@app.route("/register")
def signup():
    return render_template("signup.html")



# Many controllers/Routes here