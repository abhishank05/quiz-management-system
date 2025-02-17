#starting of app
from datetime import datetime
from flask import Flask, redirect,render_template,request, session, url_for
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
            return redirect(url_for("admin_dashboard",name=uname)) # redirects to admin_dashboard fn route
        elif usr and usr.qualification!="Administrator":
           return redirect(url_for("user_dashboard",name=uname)) # redirects to user_dashboard fn route
        else:
            return render_template("login.html",msg="Invalid user Credentials ...")

    return render_template("login.html",msg="")

@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        fname=request.form.get("full_name")
        qual=request.form.get("qualification")
        dob=request.form.get("dob")
        if dob:
            dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        else:
            dob_date=None    
        new_usr=User_Info(email=uname,password=pwd,full_name=fname,qualification=qual,dob=dob_date)
        if new_usr:
            return render_template("signup.html",msg="Sorry,the mail is already registered!!!")
        db.session.add(new_usr)
        db.session.commit()
        db.session.close()
        return render_template("login.html")
    
    return render_template("signup.html")

#common route for admin dashboard
@app.route('/admin/<name>')
def admin_dashboard(name):
    subject=get_subject()
    return render_template("admin_dashboard.html",name=name,subject=subject)

#common route for user dashboard
@app.route('/user/<name>')
def user_dashboard(name):
    return render_template("user_dashboard.html",name=name)

# Many controllers/Routes here
@app.route('/subject/<name>',methods=["GET","POST"])
def add_subject(name):
    if request.method=='POST':
        sub_id=request.form.get('id')
        sub_name=request.form.get('name')
        des=request.form.get('description')
        #user_id=request.form.get('user_id')
        new_subj=Subject(id=sub_id,name=sub_name,description=des)
        db.session.add(new_subj)
        db.session.commit()
        db.session.close()
        return redirect(url_for("admin_dashboard",name=name))

    return render_template("add_subject.html")

def get_subject():
    subject=Subject.query.all()
    return subject