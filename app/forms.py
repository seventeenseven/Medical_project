from flask_wtf import FlaskForm
from wtforms.validators import *
from wtforms import StringField, SelectField, IntegerField, TextAreaField, \
    SubmitField, RadioField, PasswordField, DateField, FloatField, FileField


class IllnessForm(FlaskForm):
    category = SelectField('Choose Illness Category', choices=[('general practitioner', 'GENERAL PRACTITIONER'),
        ('cardiologist', 'CARDIOLOGIST'), ('gastroenterologist', 'GASTROENTEROLOGIST'),
        ('pneumonologist', 'PNEUMONOLOGIST'), ('naturopath', 'NATUROPATH'), ('psychiatrist', 'PSYCHIATRIST')])
    content = TextAreaField('Describe Your Health Problem')
    document = FileField("Upload a file")
    submit = SubmitField('Send Your Illness Request')


class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    role = RadioField('Your are Doctor Or Patient', choices=[('patient','PATIENT'),('doctor','DOCTOR')])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    first_name = StringField("Enter your name")
    last_name = StringField("Enter your last_name")
    password = PasswordField("Enter your password")
    password_confirm = PasswordField("Confirm your password")
    profession = StringField("Which profession are you in ?")
    birth_date = DateField("The date of your birth")
    email = StringField("Your email address")
    phone = StringField("Your phone number")
    address = StringField("Your address")
    city = StringField("Your city")
    country = StringField("Your country")
    height = StringField("Your height")
    weight = StringField("Your weight in kg")
    blood_group = StringField("Your blood group")
    allergies = TextAreaField("Which allergies you have?")
    medicines = StringField("Which medication are you taking ?")
    medical_background = TextAreaField("Your medical antecedents")
    submit = SubmitField("Send informations")


class AnswerForm(FlaskForm):
    answer = TextAreaField('Answer to this request', validators=[data_required()])
    submit = SubmitField("Doctors Answer")
