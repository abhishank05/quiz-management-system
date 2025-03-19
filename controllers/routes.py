#starting of app
from datetime import datetime
from flask import Flask, flash, redirect,render_template,request, session, url_for
from models.model1 import *
from flask import current_app as app
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine('sqlite:///mydatabase.db', connect_args={'timeout': 15})

@app.route("/")
def home():
    return render_template("index.html")

def setup_admin():
    # Create tables if they don't exist
    db.create_all()
    # Check if an admin already exists
    if not User_Info.query.first():
        # Default admin credentials
        id=1
        full_name = "admin"
        email = "admin@iitm.ac.in"
        password = "Admin123"
        role = "Administrator"
        dob="1995-02-07"
        # Hash the password
        hashed_password = generate_password_hash(password) # type: ignore
        # Create and add the admin
        new_admin = User_Info(id=id,email = email, password=hashed_password,full_name=full_name, qualification=role,dob=dob)
        db.session.add(new_admin)
        db.session.commit()
        print(f"Admin user '{full_name}' has been created.")



@app.route("/quiz/<int:chapter_id>/<quiz_name>", methods=['GET', 'POST'])
def quiz(chapter_id, quiz_name):
    quiz_obj = Quiz.query.filter_by(chapter_id=chapter_id, quiz_name=quiz_name).first()
    
    if not quiz_obj:
        flash("Quiz not found!", "danger")
        return redirect(url_for("add_quiz", chapter_id=chapter_id, quiz_name=quiz_name))

    return render_template("quizManagement_dashboard.html", quiz=quiz_obj, chapter_id=chapter_id, quiz_name=quiz_name)



@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        usr=User_Info.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.qualification=="Administrator":
            session['name']=uname
            subject=get_subjects()
            return redirect(url_for("admin_dashboard")) # redirects to admin_dashboard fn route
        elif usr and usr.qualification!="Administrator":
           return redirect(url_for("user_dashboard")) # redirects to user_dashboard fn route
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
@app.route('/admin')
def admin_dashboard():
    name=session.get('name','Admin')
    subject=get_subjects()
    quiz_obj=Quiz.query.first()
    return render_template("admin_dashboard.html",name=name,subjects=subject,quiz=quiz_obj)

#common route for user dashboard
@app.route('/user')
def user_dashboard():
    name=session.get('name','')
    return render_template("user_dashboard.html",name=name)

@app.route('/quizManagement_dashboard/<int:chapter_id>/<string:quiz_name>', methods=['GET', 'POST'])
def quizManagement_dashboard(chapter_id, quiz_name):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    if not quizzes:
        flash("No quizzes found! Please add a quiz first.", "warning")
        return redirect(url_for("add_quiz", chapter_id=chapter_id, quiz_name=quiz_name))

    return render_template("quizManagement_dashboard.html", chapter_id=chapter_id, quiz_name=quiz_name, quizzes=quizzes,name=session.get("name"))


# Many controllers/Routes here
#CRUD Operations for Subject
@app.route('/subject_detail/<int:subject_id>', methods=["GET", "POST"])
def subject_detail(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return render_template("subject_detail.html", subject=subject)


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
        return redirect(url_for("admin_dashboard"))
    return render_template("add_subject.html")

@app.route('/edit_subject/<int:subject_id>/<string:name>', methods=["GET", "POST"])
def edit_subject(subject_id,name):
    subject = Subject.query.get_or_404(subject_id)  # Fetch the subject
    if request.method == 'POST':
        subject.name = request.form.get('name')
        subject.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for("admin_dashboard"))  # Redirect to admin dashboard
    return render_template("edit_subject.html", subject=subject)

@app.route('/delete_subject/<int:subject_id>/<name>', methods=["POST"])
def delete_subject(subject_id,name):
    subject = Subject.query.get_or_404(subject_id)  # Fetch the subject

    db.session.delete(subject)
    db.session.commit()

    return redirect(url_for("admin_dashboard"))  # Redirect after deletion

#CRUD Operations for Chapter
@app.route('/chapter/<int:subject_id>/<name>',methods=["GET","POST"])
def add_chapter(subject_id,name):
    if request.method=='POST':
        chap_id=request.form.get('id')
        chap_name=request.form.get('name')
        des=request.form.get('description')
        new_chap=Chapter(id=chap_id,name=chap_name,description=des,subject_id=subject_id)
        db.session.add(new_chap)
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
    return render_template("add_chapter.html",sub_id=subject_id,name=name)

@app.route('/edit_chapter/<int:chapter_id>/<string:name>', methods=["GET", "POST"])
def edit_chapter(chapter_id,name):
    chapter = Chapter.query.get_or_404(chapter_id)  # Fetch the chapter
    if request.method == 'POST':
        chapter.name = request.form.get('name')
        chapter.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for("admin_dashboard"))  # Redirect to admin dashboard
    return render_template("edit_chapter.html", chapter=chapter)

@app.route('/delete_chapter/<int:chapter_id>/<string:name>', methods=["POST"])
def delete_chapter(chapter_id,name):
    chapter = Chapter.query.get_or_404(chapter_id)  # Fetch the chapter

    db.session.delete(chapter)
    db.session.commit()

    return redirect(url_for("admin_dashboard"))  # Redirect after deletion



#CRUD OPERATIONS for quiz

@app.route('/quiz_detail/<int:id>', methods=["GET", "POST"])
def quiz_detail(id):
    quiz = Quiz.query.get_or_404(id)
    return render_template("quiz_detail.html", quiz=quiz)

@app.route('/add_quiz/<int:chapter_id>/<string:quiz_name>', methods=["GET", "POST"])
def add_quiz(chapter_id, quiz_name):
    if request.method == 'POST':
        # Get form values for creating a new quiz
        #quiz_id = request.form.get('id')
        quiz_name_from_form = request.form.get('quiz_name')
        date_quiz_str = request.form.get('date_of_quiz')
        date_quiz = datetime.strptime(date_quiz_str, '%Y-%m-%d').date()
        duration_str = request.form.get('time_duration')
        time_duration = datetime.strptime(duration_str, '%H:%M').time()
        remark = request.form.get('remarks')
        
        new_quiz = Quiz(
            #id=quiz_id, 
            chapter_id=chapter_id, 
            quiz_name=quiz_name_from_form,
            date_of_quiz=date_quiz, 
            time_duration=time_duration, 
            remarks=remark
        )
        db.session.add(new_quiz)
        db.session.commit()
        
        # Redirect to the quiz management dashboard after successfully adding a quiz
        return redirect(url_for("quizManagement_dashboard", chapter_id=chapter_id, quiz_name=quiz_name_from_form))
    
    # GET branch: simply render the form to add a quiz.
    return render_template("add_quiz.html", chapter_id=chapter_id, quiz_name=quiz_name)


@app.route('/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        # Update quiz fields from form data
        quiz.quiz_name = request.form.get('quiz_name')
        quiz.date_of_quiz = datetime.strptime(request.form.get('date_of_quiz'), '%Y-%m-%d').date()
        quiz.time_duration = datetime.strptime(request.form.get('time_duration'), '%H:%M').time()
        quiz.remarks = request.form.get('remarks')
        db.session.commit()
        flash("Quiz updated successfully", "success")
        return redirect(url_for('quizManagement_dashboard', chapter_id=quiz.chapter_id, quiz_name=quiz.quiz_name,name=session.get("name")))
    # Render an edit form (create a template edit_quiz.html accordingly)
    return render_template("edit_quiz.html", quiz=quiz)


@app.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id=quiz.chapter_id
    quiz_name=quiz.quiz_name
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted successfully", "success")
    return redirect(url_for('quizManagement_dashboard', chapter_id=chapter_id, quiz_name=quiz_name,name=session.get("name")))


#CRUD Operations for Question
@app.route('/ques/<int:quiz_id>/<int:id>', methods=["GET", "POST"])
def add_question(quiz_id, id):
    quiz = Quiz.query.get(quiz_id)

    if not quiz:
        flash(f"Quiz not found for quiz_id: {quiz_id}", "danger")
        return redirect(url_for("quizManagement_dashboard", chapter_id=1, quiz_name="default"))

    if request.method == 'POST':
        ques_name = request.form.get('question_statement')
        op1 = request.form.get('option1')
        op2 = request.form.get('option2')
        op3 = request.form.get('option3')
        op4 = request.form.get('option4')
        correct_op = request.form.get('correct_option')

        new_ques = Questions(
            question_statement=ques_name,
            quiz_id=quiz_id,
            option1=op1,
            option2=op2,
            option3=op3,
            option4=op4,
            correct_option=correct_op
        )
        
        db.session.add(new_ques)
        db.session.commit()

        flash("Question added successfully!", "success")
        return redirect(url_for("quizManagement_dashboard", chapter_id=quiz.chapter_id, quiz_name=quiz.quiz_name))

    return render_template(
        "add_question.html",
        quiz_id=quiz_id,
        id=id,
        chapter_id=quiz.chapter_id if quiz else 0,  # Use a safe fallback value
        quiz_name=quiz.quiz_name if quiz else "default",
        name=session.get("user_name")
    )

@app.route('/edit_question/<id>',methods=['GET','POST'])
def edit_question(id):
    ques = Questions.query.get_or_404(id)
    if request.method == 'POST':
        #ques.id=request.form.get('id')
        #ques.quiz_id=request.form.get('quiz_id')
        ques.question_statement=request.form.get('question_statement')
        ques.option1=request.form.get('option1')
        ques.option2 = request.form.get('option2')
        ques.option3 = request.form.get('option3')
        ques.option4 = request.form.get('option4')
        ques.correct_option = request.form.get('correct_option')
        db.session.commit()
        flash("Question updated successfully", "success")
        return redirect(url_for('quizManagement_dashboard', chapter_id=ques.quiz.chapter_id, quiz_name=ques.quiz.quiz_name,name=session.get("name")))
    # Render an edit form (create a template edit_ques.html accordingly)
    return render_template("edit_question.html", ques=ques)

@app.route('/delete_question/<int:id>',methods=['POST'])
def delete_question(id):
    ques = Questions.query.get_or_404(id)
    chapter_id=ques.quiz.chapter_id
    quiz_name=ques.question_statement
    quiz_id=ques.quiz_id
    id=ques.id
    db.session.delete(ques)
    db.session.commit()
    flash("Quiz deleted successfully", "success")
    return redirect(url_for('quizManagement_dashboard', chapter_id=ques.quiz.chapter_id, quiz_name=ques.quiz.quiz_name,name=session.get("name")))

#Search Functionality
@app.route('/search/<string:name>', methods=['POST'])
def search(name):
    # Get the search text from the form
    search_txt = request.form.get("search_txt")
    if not search_txt:
        flash("Please enter a search term", "warning")
        return redirect(url_for("admin_dashboard"))
    
    # Query the models for matching entries
    subjects = Subject.query.filter(Subject.name.ilike(f"%{search_txt}%")).all()
    chapters = Chapter.query.filter(Chapter.name.ilike(f"%{search_txt}%")).all()
    quizzes = Quiz.query.filter(Quiz.quiz_name.ilike(f"%{search_txt}%")).all()
    questions = Questions.query.filter(Questions.question_statement.ilike(f"%{search_txt}%")).all()
    
    # Bundle results into a dictionary to pass to the template
    results = {
       "subjects": subjects,
       "chapters": chapters,
       "quizzes": quizzes,
       "questions": questions,
    }
    
    return render_template("search_results.html", results=results, search_txt=search_txt, name=name)




#other supported function
def get_subjects():
    subject=Subject.query.all()
    return subject