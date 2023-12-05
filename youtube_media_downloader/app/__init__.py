from flask import Flask

app=Flask(__name__)

app.config['SECRET_KEY']='Hard to fucking guess'

# from . import views
from . import error
from .you import you
app.register_blueprint(you)