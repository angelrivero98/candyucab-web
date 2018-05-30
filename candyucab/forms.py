from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField
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

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember =BooleanField('Recuerdame')
    submit=SubmitField('Iniciar')

class RegistrationJForm(FlaskForm):
        username=StringField('Nombre de Usuario',validators=[DataRequired(),Length(min=2,max=20)])
        email = StringField('Email',validators=[DataRequired(),Email()])
        password = PasswordField('Contraseña',validators=[DataRequired()])
        confim_password = PasswordField('Confirmar Contraseña',validators=[DataRequired(),EqualTo('password')])
        rif = StringField('RIF',validators=[DataRequired(),Length(min=2,max=20)])
        demcom = StringField('Denominacion Comercial',validators=[DataRequired(),Length(min=2,max=50)])
        razsoc = StringField('Razon Social',validators=[DataRequired(),Length(min=2,max=50)])
        pagweb = StringField('Pagina Web',validators=[DataRequired(),Length(min=2,max=30)])
        capdis = IntegerField('Capital Disponible',validators=[DataRequired()])
        #Direccion Fiscal
        est1 = StringField('Estado',validators=[DataRequired()])
        municipio1 = StringField('Municipio',validators=[DataRequired()])
        par1  = StringField('Parroquia',validators=[DataRequired()])
        # Direccion Fisica
        est2 = StringField('Estado',validators=[DataRequired()])
        municipio2 = StringField('Municipio',validators=[DataRequired()])
        par2  = StringField('Parroquia',validators=[DataRequired()])
        submit=SubmitField('Registrate')
        def validate_username(self,username):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT u_username from usuario WHERE u_username = %s;",(username.data,))
            if cur.fetchone():
                raise ValidationError('El nombre de usuario ya esta tomado')

        def validate_email(self,email):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT cj_email,cn_email from clientejuridico,clientenatural WHERE cj_email = %s OR cn_email = %s;",(email.data,email.data))
            if cur.fetchone():
                raise ValidationError('El email ya esta tomado')

        def validate_rif(self,rif):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT cj_rif,cn_rif from clientejuridico,clientenatural WHERE cj_rif = %s OR cn_rif = %s;",(rif.data,rif.data))
            if cur.fetchone():
                raise ValidationError('El rif ya esta tomado')

        def validate_dirF(self,est1,municipio1,par1):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                        E.l_nombre = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                        P.l_nombre = %s AND P.fk_lugar = M.l_id;
                        """,(est1.data,municipio1.data,par1.data,))
            if cur.fetchone() == None:
                raise ValidationError('La direccion Fiscal no existe')

        def validate_dirFisica(self,est2,municipio2,par2):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                        E.l_nombre = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                        P.l_nombre = %s AND P.fk_lugar = M.l_id;
                        """,(est2.data,municipio2.data,par2.data,))
            if cur.fetchone() == None:
                raise ValidationError('La direccion Fisica no existe')
