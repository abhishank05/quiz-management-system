#starting of app
from datetime import datetime
from flask import Flask, redirect,render_template,request, session
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
        usr=User_Info.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.qualification=="Administrator":
            return render_template("admin_dashboard.html")
        elif usr and usr.qualification!="Administrator":
            return render_template("user_dashboard.html")
        else:
            return render_template("login.html",msg="Invalid user Credentials ...")

    return render_template("login.html",msg="")
'''
@app.route("/login", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        uname = request.form.get("user_name")
        pwd = request.form.get("password")
        print(pwd)

        # Fetch user by email
        usr = User_Info.query.filter_by(email=uname).first()

        if usr:
            print("User found:", usr.email)
            
            # Check if the user is an Administrator
            if usr.qualification == "Administrator":
                print("User is an Administrator")
                
                # Verify password
                if usr.password == pwd:
                    print("Password matches!")
                    session['user_id'] = usr.id
                    return render_template("admin_dashboard.html")
                else:
                    print("Password mismatch!")
                    return render_template("login.html", error="Incorrect password.")
            else:
                print("User is not an Administrator")
                return render_template("login.html", error="Access denied. Not an Administrator.")
        else:
            print("User not found")
            return render_template("login.html", error="User does not exist.")  # Handle NoneType here

    return render_template("login.html")
'''

@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        fname=request.form.get("full_name")
        qual=request.form.get("qualification")
        dob=request.form.get("dob")
        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()    
        new_usr=User_Info(email=uname,password=pwd,full_name=fname,qualification=qual,dob=dob_date)
        if new_usr:
            return render_template("signup.html",msg="Sorry,the mail is already registered!!!")
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html")
    
    return render_template("signup.html")



# Many controllers/Routes here