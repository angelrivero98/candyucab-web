from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField,FieldList,FormField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,Optional,InputRequired
from candyucab.db import Database
import psycopg2,psycopg2.extras

class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario',validators=[DataRequired()])
    password = PasswordField('Contraseña',validators=[DataRequired()])
    remember =BooleanField('Recuérdame')
    submit=SubmitField('Iniciar')

class TlfForm(FlaskForm):
    numero = IntegerField('Ingrese el Telefono sin el 0',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
    submit=SubmitField('Añadir Campo')

    def validate_numero(self,numero):
        if len(str(numero.data)) != 10 :
            raise ValidationError('El numero de telefono es invalido')

class PersonaContactoForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
    apellido = StringField('Apellido',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
    submit=SubmitField('Añadir Campos')

class RegistrationJForm(FlaskForm):
        username=StringField('Nombre de Usuario',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=20)])
        email = StringField('Email',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Email(message='Ingrese un email valido')])
        password = PasswordField('Contraseña',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        confim_password = PasswordField('Confirmar Contraseña',validators=[DataRequired(message='Este campo no puede dejarse vacio'),EqualTo('password')])
        rif = StringField('RIF',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=20)])
        demcom = StringField('Denominacion Comercial',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=50)])
        razsoc = StringField('Razon Social',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=50)])
        pagweb = StringField('Pagina Web',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=30)])
        capdis = IntegerField('Capital Disponible',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        #Direccion Fiscal
        est1 = StringField('Estado',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        municipio1 = StringField('Municipio',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        par1  = StringField('Parroquia',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        # Direccion Fisica
        est2 = StringField('Estado',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        municipio2 = StringField('Municipio',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        par2  = StringField('Parroquia',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        #tlf1 = IntegerField('Capital Disponible',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
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
            cur.execute("SELECT cj_email from clientejuridico WHERE cj_email = %s;",(email.data,))
            if cur.fetchone():
                raise ValidationError('El email ya esta tomado')
            else:
                cur.execute("SELECT cn_email from clientenatural WHERE cn_email = %s;",(email.data,))
                raise ValidationError('El email ya esta tomado')

        def validate_rif(self,rif):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT cj_rif from clientejuridico WHERE cj_rif = %s;",(rif.data,))
            if cur.fetchone():
                raise ValidationError('El rif ya esta tomado')
            else:
                cur.execute("SELECT cn_rif from clientenatural WHERE cn_rif = %s;",(rif.data,))
                raise ValidationError('El rif ya esta tomado')

        def validate_est1(self,est1):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                        E.l_nombre = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                        P.l_nombre = %s AND P.fk_lugar = M.l_id;
                        """,(est1.data,self.municipio1.data,self.par1.data,))
            if cur.fetchone() == None:
                  raise ValidationError('La direccion Fiscal no existe')

        def validate_par2(self,par2):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                        E.l_nombre = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                        P.l_nombre = %s AND P.fk_lugar = M.l_id;
                        """,(self.est2.data,self.municipio2.data,par2.data,))
            if cur.fetchone() == None:
                raise ValidationError('La direccion Fisica no existe')

class RegistrationNForm(FlaskForm):
        username=StringField('Nombre de Usuario',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=2,max=20)])
        email = StringField('Email',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Email(message='Ingrese un email valido')])
        password = PasswordField('Contraseña',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        confim_password = PasswordField('Confirmar Contraseña',validators=[DataRequired(message='Este campo no puede dejarse vacio'),EqualTo('password')])
        rif = StringField('RIF',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=2,max=20)])
        nom1 = StringField('Primer Nombre',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        nom2 = StringField('Segundo Nombre',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        ap1 = StringField('Primer Apellido',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        ap2 = StringField('Segundo Apellido',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        ci = IntegerField('Cedula',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        #Direccion
        est1 = StringField('Estado',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        municipio1 = StringField('Municipio',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        par1  = StringField('Parroquia',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        submit=SubmitField('Registrate')
        def validate_username(self,username):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT u_username from usuario WHERE u_username = %s;",(username.data,))
            if cur.fetchone():
                raise ValidationError('El nombre de usuario ya esta tomado')


        def validate_ci(self,ci):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT cn_ci from clientenatural WHERE cn_ci = %s;",(ci.data,))
            if cur.fetchone():
                raise ValidationError('La cedula ya esta tomada')

        def validate_email(self,email):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT cj_email from clientejuridico WHERE cj_email = %s;",(email.data,))
            if cur.fetchone():
                raise ValidationError('El email ya esta tomado')
            else:
                cur.execute("SELECT cn_email from clientenatural WHERE cn_email = %s;",(email.data,))
                raise ValidationError('El email ya esta tomado')

        def validate_rif(self,rif):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT cj_rif from clientejuridico WHERE cj_rif = %s;",(rif.data,))
            if cur.fetchone():
                raise ValidationError('El rif ya esta tomado')
            else:
                cur.execute("SELECT cn_rif from clientenatural WHERE cn_rif = %s;",(rif.data,))
                raise ValidationError('El rif ya esta tomado')

        def validate_est1(self,est1):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                        E.l_nombre = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                        P.l_nombre = %s AND P.fk_lugar = M.l_id;
                        """,(est1.data,self.municipio1.data,self.par1.data,))
            if cur.fetchone() == None:
                  raise ValidationError('La direccion no existe')
