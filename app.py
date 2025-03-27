#starting of app
from flask import Flask,render_template
from models.model1 import db
from sqlalchemy.pool import NullPool


app=None

def setup_app():
    app=Flask(__name__)
    app.secret_key = 'your_secret_key_here'
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///quiz_master.sqlite3"#Having db file

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Allow access from multiple threads
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'check_same_thread': False,  # Allows cross-thread usage
        'timeout': 30  # Increase timeout to wait longer for locks
    },
    'poolclass': NullPool,  # Disable connection pooling
}

    db.init_app(app) #Flask app connected to db
    app.app_context().push()# Direct access to other modules
    app.debug=True
    print("Quizz Master app is started...")
    

setup_app()


from controllers.routes import *

if __name__=="__main__":
    with app.app_context():
        setup_admin()
    app.run(debug=True)

