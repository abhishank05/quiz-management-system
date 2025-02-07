#starting of app
from flask import Flask,render_template
from models.model1 import db


app=None

def setup_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///quiz_master.sqlite3"#Having db file
    db.init_app(app) #Flask app connected to db
    app.app_context().push()# Direct access to other modules
    app.debug=True
    print("Quizz Master app is started...")
    

setup_app()

from controllers.routes import *

if __name__=="__main__":
    app.run(debug=True)

