#starting of app
from datetime import datetime
from flask import Flask, redirect,render_template,request, session, url_for
from models.model1 import *
from flask import current_app as app
from sqlalchemy import create_engine

engine = create_engine('sqlite:///mydatabase.db', connect_args={'timeout': 15})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz/<int:chapter_id>/<quiz_name>",methods=['GET','POST'])
def quiz(chapter_id,quiz_name):
    quiz = {
        'chapter_id': chapter_id,
        'quiz_name': quiz_name
    }
    return render_template("quizManagement_dashboard.html",quiz=quiz)

@app.context_processor
def inject_default_quiz():
    # Define your default quiz here (you could also load this from a config or database)
    default_quiz = {'chapter_id': 1, 'quiz_name': 'Math_Quiz'}
    return dict(quiz=default_quiz)

@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        usr=User_Info.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.qualification=="Administrator":
            subject=get_subjects()
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
        return render_template("login.html")
    
    return render_template("signup.html")

#common route for admin dashboard
@app.route('/admin/<name>')
def admin_dashboard(name):
    subject=get_subjects()
    return render_template("admin_dashboard.html",name=name,subjects=subject)

#common route for user dashboard
@app.route('/user/<name>')
def user_dashboard(name):
    return render_template("user_dashboard.html",name=name)

@app.route('/quizManagement_dashboard/chapter_id/<quiz_name>')
def quizManagement_dashboard(chapter_id,quiz_name):
    return render_template("quizManagement_dashboard.html",chapter_id=chapter_id,quiz_name=quiz_name)

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
        
        return redirect(url_for("admin_dashboard",name=name))

    return render_template("add_subject.html")


@app.route('/chapter/<sub_id>/<name>',methods=["GET","POST"])
def add_chapter(sub_id,name):
    if request.method=='POST':
        chap_id=request.form.get('id')
        chap_name=request.form.get('name')
        des=request.form.get('description')
        new_chap=Chapter(id=chap_id,name=chap_name,description=des,subject_id=sub_id)
        db.session.add(new_chap)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))

    return render_template("add_chapter.html",sub_id=sub_id,name=name)

@app.route('/ques/<quiz_id>/<id>',methods=["GET","POST"])
def add_question(quiz_id,id):
    if request.method=='POST':
        ques_id=request.form.get('id')
        ques_name=request.form.get('question_statement')
        op1=request.form.get('option1')
        op2=request.form.get('option2')
        op3=request.form.get('option3')
        op4=request.form.get('option4')
        correct_op=request.form.get('correct_option')
        new_ques=Questions(id=ques_id,question_statement=ques_name,quiz_id=quiz_id,option1=op1,option2=op2,option3=op3,option4=op4,correct_option=correct_op)
        db.session.add(new_ques)
        db.session.commit()
        return redirect(url_for("quiz_dashboard",id=id))

    return render_template("add_question.html",quiz_id=quiz_id,id=id)
       

@app.route('/quiz/<int:chapter_id>/<quiz_name>',methods=["GET","POST"])
def add_quiz(chapter_id,quiz_name):
    print(f"Received request for chapter_id: {chapter_id}, quiz_name: {quiz_name}")
    if request.method=='POST':
        quiz_id=request.form.get('id')
        quiz_name_from_form=request.form.get('quiz_name')
        date_quiz=request.form.get('date_of_quiz')
        duration=request.form.get('time_duration')
        remark=request.form.get('remarks')
        new_quiz=Quiz(id=quiz_id,chapter_id=chapter_id,quiz_name=quiz_name_from_form,date_of_quiz=date_quiz,time_duration=duration,remarks=remark) #parameters here have to match the definitions in the model
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for("quizManagement_dashboard",chapter_id=chapter_id,quiz_name=quiz_name_from_form))
    
    return render_template("add_quiz.html",chapter_id=chapter_id,quiz_name=quiz_name)


#other supported function
def get_subjects():
    subject=Subject.query.all()
    return subject