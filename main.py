from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, URLField, DateField, RadioField
from wtforms.validators import DataRequired, Email
import requests
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it-is-a-secret-key-for-test-purposes'
Bootstrap5(app)
class Intake(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    mname = StringField('Middle Name')
    sname = StringField('Surname', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    allergies = RadioField('Allergies', choices=[("Yes",'I do have allergies'),('No', 'No i do not have allergies')])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    form = Intake()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
