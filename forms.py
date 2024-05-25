
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, URLField, DateField, RadioField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea

class Intake(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    mname = StringField('Middle Name')
    sname = StringField('Surname', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    gender = StringField('Birth Gender', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class ObsForm(FlaskForm):
    sbp = IntegerField('Systolic BP')
    dbp = IntegerField('Diastolic BP')
    hr = IntegerField('Heart Rate')
    rr = IntegerField('Respiration Rate')
    spo2 = IntegerField('SpO2')
    gcs = IntegerField('GCS')
    temp = IntegerField('Temperature')
    cap_refill = StringField('Capillary Refill')
    l_pupil_size = IntegerField('Left Pupil')
    r_pupil_size = IntegerField('Right Pupil')

