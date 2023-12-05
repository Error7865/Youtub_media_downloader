from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class Login(FlaskForm):         #this form for User login
    email=EmailField('Email: ', validators=([DataRequired()]))
    password=PasswordField('Password: ', validators=[DataRequired()])
    submit=SubmitField('Done')

class You(FlaskForm):       #This form for take youtube link
    link=StringField(render_kw={"placeholder":"link"}, validators=[DataRequired()])

class Download(FlaskForm):      #This form with a submit and a hidden which will contain itag value
    sub=SubmitField()
    itag=HiddenField()