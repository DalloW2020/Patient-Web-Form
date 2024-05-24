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
from forms import Intake

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it-is-a-secret-key-for-test-purposes'
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
db = SQLAlchemy(app)

"""
TYPE THIS INTO THE PYTHON TERMINAL TO CREATE DATABASE
from main import app, db
app.app_context().push()
db.create_all()
"""


class DbRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    dob = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


@app.route('/delete/<int:id>')
def delete_entry(id):
    user_to_delete = DbRegistration.query.get_or_404(id)
    form = Intake()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        patient = DbRegistration.query.order_by(DbRegistration.id)
        return render_template("home.html", form=form,
                               user_to_delete=user_to_delete,
                               patient=patient)
    except:
        patient = DbRegistration.query.order_by(DbRegistration.id)
        return render_template("home.html", form=form,
                               user_to_delete=user_to_delete,
                               patient=patient)


@app.route('/')
def home():
    registration = DbRegistration()
    patients = registration.query.order_by(registration.id)
    return render_template('home.html', patients=patients)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Intake()
    registration = DbRegistration()
    if request.method == 'POST':
        person = registration.query.filter_by(email=form.email.data).first()
        if person is None:
            person = DbRegistration(first_name=form.fname.data,
                                    middle_name=form.mname.data,
                                    surname=form.sname.data,
                                    gender=form.gender.data,
                                    dob=form.dob.data,
                                    address=form.address.data,
                                    state=form.state.data,
                                    city=form.city.data,
                                    postcode=form.postcode.data,
                                    email=form.email.data)
            db.session.add(person)
            db.session.commit()
            patient = DbRegistration.query.order_by(DbRegistration.id)
            return render_template('register.html', form=form,
                                   registration=registration,
                                   patient=patient)
        patient = DbRegistration.query.order_by(DbRegistration.id)
        return render_template('register.html', form=form,
                               registration=registration,
                               patient=patient)
    patient = DbRegistration.query.order_by(DbRegistration.id)
    return render_template('register.html', form=form,
                           registration=registration,
                           patient=patient)


if __name__ == '__main__':
    app.run(debug=True)
