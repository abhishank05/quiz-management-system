#Data Models

from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

#First Entity
class User_Info(db.Model):
    __tablename__="user_info"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    full_name=db.Column(db.String,nullable=False)
    qualification=db.Column(db.String,nullable=False)
    dob=db.Column(db.Date,nullable=False)
    subjects=db.relationship("Subject",cascade="all,delete",backref="user_info",lazy=True)#Cascade all,delete will remove all the child entries when the parent entry is deleted in the table

#Second Entity Subject
class Subject(db.Model):
    __tablename__="subject"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)
    chapters=db.relationship("Chapter",cascade="all,delete",backref="subject",lazy=True)

#Third Entity Chapter
class Chapter(db.Model):
    __tablename__="chapter"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    quizes=db.relationship("Quiz",cascade="all,delete",backref="chapter",lazy=True)

#Fourth Entity Quiz
class Quiz(db.Model):
    __tablename__="quiz"
    id=db.Column(db.Integer,primary_key=True)
    chapter_id=db.Column(db.Integer,db.ForeignKey("chapter.id"),nullable=False)
    date_of_quiz=db.Column(db.Date,nullable=False)
    time_duration=db.Column(db.Time,nullable=False)
    remarks=db.Column(db.String,nullable=False)
    questions=db.relationship("Questions",cascade="all,delete",backref="quiz",lazy=True)

#Fifth Entity Questions
class Questions(db.Model):
    __tablename__="questions"
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey("quiz.id"),nullable=False)
    question_statement=db.Column(db.String,nullable=False)
    option1=db.Column(db.String,nullable=False)
    option2=db.Column(db.String,nullable=False)
    option3=db.Column(db.String,nullable=False)
    option4=db.Column(db.String,nullable=False)
    correct_option=db.Column(db.String,nullable=False)
    scores=db.relationship("Scores",cascade="all,delete",backref="questions",lazy=True)

#Sixth Entity Scores
class Scores(db.Model):
    __tablename__="scores"
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey("quiz.id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user_info.id"),nullable=False)
    time_stamp_of_attempt=db.Column(db.Time,nullable=False)
    total_scored=db.Column(db.Float,default=0)
    users=db.relationship("User_Info",cascade="all,delete",backref="scores",lazy=True)

