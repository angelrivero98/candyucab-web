from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from candyucab.db import Database
import psycopg2,psycopg2.extras

class RegistrationForm(FlaskForm):
    username=StringField('Nombre de Usuario',validators=[DataRequired(),Length(min=2,max=20)])
    #email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Contraseña',validators=[DataRequired()])
    confim_password = PasswordField('Confirmar Contraseña',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Registrate')
    def validate_username(self,username):

        db = Database()
        cur = db.cursor_dict()
        cur.execute("SELECT u_username from usuario WHERE u_username = %s;",(username.data,))
        if cur.fetchone():
            raise ValidationError('El nombre de usuario ya esta tomado')

    #def validate_email(self,email):
        #db = Database()
        #cur = db.cursor_dict()
        #cur.execute("SELECT email from public.user WHERE email = %s;",(email.data,))
        #if cur.fetchone():
            #raise ValidationError('El email ya esta tomado')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember =BooleanField('Recuerdame')
    submit=SubmitField('Iniciar')
