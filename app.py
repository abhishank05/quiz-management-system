#starting of app
from flask import Flask,render_template

app=Flask(__name__)

app=None

def setup_app():
    app=Flask(__name__)
    app.debug=True
    #Pending sqlite connection to be added
    app.app_context().push() # Direct access to other modules
    print("Quizz Master app is started...")
    

setup_app()

from controllers.routes import *

if __name__=="__main__":
    app.run(debug=True)

