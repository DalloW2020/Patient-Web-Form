from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, foreign
from sqlalchemy import Integer, String, Float, Column, Integer, ForeignKey
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, URLField, DateField, RadioField
from wtforms.validators import DataRequired, Email
import requests
from flask_migrate import Migrate
from datetime import datetime
from forms import Intake, ObsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it-is-a-secret-key-for-test-purposes'
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
base = DeclarativeBase()

"""
TYPE THIS INTO THE PYTHON TERMINAL TO CREATE DATABASE
from main import app, db
app.app_context().push()
db.create_all()
"""
"""
Flask migrate commands:
flask db migrate -m "enter a tag"
flask db upgrade
"""


class dbregistration(db.Model):
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
    primary_notes = db.Column(db.String)
    observations = db.relationship('Observation', backref='dbregistration')

    def __repr__(self):
        return '<Name %r>' % self.name

class Observation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dbregistration_id = db.Column(db.Integer, db.ForeignKey('dbregistration.id'))
    sbp = db.Column(db.Integer)
    dbp = db.Column(db.Integer)
    hr = db.Column(db.Integer)
    rr = db.Column(db.Integer)
    spo2 = db.Column(db.Integer)
    gcs = db.Column(db.Integer)
    temp = db.Column(db.Integer)
    cap_refill = db.Column(db.String)
    l_pupil_size = db.Column(db.Integer)
    r_pupil_size = db.Column(db.Integer)

    def __repr__(self):
        return '<Name %r>' % self.name



@app.route('/patient_notes<int:id>')
def patient_notes(id):
    patient_details = dbregistration.query.get_or_404(id)
    obsform = ObsForm()
    return render_template('patient_notes.html',
                           patient_details=patient_details,
                           obsform=obsform)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_record(id):
    user_to_update = dbregistration.query.get_or_404(id)
    form = Intake()
    registration = dbregistration()
    patient = registration.query.order_by(registration.id)
    if request.method == "POST":
        user_to_update.first_name = request.form['fname']
        user_to_update.middle_name = request.form['mname']
        user_to_update.surname = request.form['sname']
        user_to_update.gender = request.form['gender']
        user_to_update.dob = request.form['dob']
        user_to_update.address = request.form['address']
        user_to_update.state = request.form['state']
        user_to_update.city = request.form['city']
        user_to_update.postcode = request.form['postcode']
        user_to_update.email = request.form['email']
        db.session.commit()
        return redirect("/")
    return render_template("update_registration.html", user_to_update=user_to_update,
                           form=form, patient=patient)


@app.route('/delete/<int:id>')
def delete_entry(id):
    user_to_delete = dbregistration.query.get_or_404(id)
    form = Intake()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        patient = dbregistration.query.order_by(dbregistration.id)
        return render_template("home.html", form=form,
                               user_to_delete=user_to_delete,
                               patient=patient)
    except:
        patient = dbregistration.query.order_by(dbregistration.id)
        return render_template("home.html", form=form,
                               user_to_delete=user_to_delete,
                               patient=patient)


@app.route('/')
def home():
    registration = dbregistration()
    patients = registration.query.order_by(registration.id)
    return render_template('home.html', patients=patients)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Intake()
    registration = dbregistration()
    if request.method == 'POST':
        person = registration.query.filter_by(email=form.email.data).first()
        if person is None:
            person = dbregistration(first_name=form.fname.data,
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
            patient = dbregistration.query.order_by(dbregistration.id)
            return render_template('register.html', form=form,
                                   registration=registration,
                                   patient=patient)
        patient = dbregistration.query.order_by(dbregistration.id)
        return render_template('register.html', form=form,
                               registration=registration,
                               patient=patient)
    patient = dbregistration.query.order_by(dbregistration.id)
    return render_template('register.html', form=form,
                           registration=registration,
                           patient=patient)


if __name__ == '__main__':
    app.run(debug=True)
