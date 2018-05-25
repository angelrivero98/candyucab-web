from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from candyucab.db import Database
import psycopg2,psycopg2.extras

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confim_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')
    def validate_username(self,username):
        cur = Database.cursor_dict()
        cur.execute("SELECT username from public.user WHERE username = %s;",(username.data,))
        if cur.fetchone():
            raise ValidationError('That username is taken')

    def validate_email(self,email):
        cur = Database.cursor_dict()
        cur.execute("SELECT email from public.user WHERE email = %s;",(email.data,))
        if cur.fetchone():
            raise ValidationError('That email is taken')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember =BooleanField('Remember Me')
    submit=SubmitField('Sign In')
