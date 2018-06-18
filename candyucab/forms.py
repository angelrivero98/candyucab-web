from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField,FieldList,FormField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,Optional,InputRequired
from candyucab.db import Database
import psycopg2,psycopg2.extras

def estados():
    db =Database()
    cur = db.cursor_dict()
    cur.execute("SELECT l_id,l_nombre FROM lugar WHERE l_tipo = 'E';")
    return cur.fetchall()

def tiendas():
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT ti_id,ti_nombre FROM tienda;")
    return cur.fetchall()

def tipo_productos():
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT * FROM tipo_producto;")
    return cur.fetchall()

class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember =BooleanField('Recuerdame')
    submit=SubmitField('Iniciar')

class TlfForm(FlaskForm):
    numero = IntegerField('Ingrese el Telefono sin el 0',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
    submit=SubmitField('Añadir Telefono')

    def validate_numero(self,numero):
        if len(str(numero.data)) != 10 :
            raise ValidationError('El numero de telefono es invalido')

class PersonaContactoForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
    apellido = StringField('Apellido',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
    submit=SubmitField('Añadir Persona')

class UpdateNForm(FlaskForm):
        email = StringField('Email',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Email(message='Ingrese un email valido')])
        rif = StringField('RIF',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=2,max=20)])
        nom1 = StringField('Primer Nombre',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        nom2 = StringField('Segundo Nombre',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        ap1 = StringField('Primer Apellido',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        ap2 = StringField('Segundo Apellido',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        ci = IntegerField('Cedula',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        #Direccion
        estados = NonValidatingSelectField('Estado',choices=tuple(estados()))
        municipios = NonValidatingSelectField('Municipio',choices=[])
        parroquias = NonValidatingSelectField('Parroquia',choices=[])
        submit=SubmitField('Actualizar')

        current_ci = IntegerField()
        current_rif = StringField()
        current_email = StringField()

        def validate_ci(self,ci):
            db = Database()
            cur = db.cursor_dict()
            if self.current_ci.data != ci.data:
                cur.execute("SELECT cn_ci from clientenatural WHERE cn_ci = %s;",(ci.data,))
                if cur.fetchone():
                    raise ValidationError('La cedula ya esta tomada')

        def validate_email(self,email):
            db = Database()
            cur = db.cursor_dict()
            if self.current_email.data != email.data:
                cur.execute("SELECT cj_email from clientejuridico WHERE cj_email = %s;",(email.data,))
                if cur.fetchone():
                    raise ValidationError('El email ya esta tomado')
                else:
                    cur.execute("SELECT cn_email from clientenatural WHERE cn_email = %s;",(email.data,))
                    if cur.fetchone():
                        raise ValidationError('El email ya esta tomado')

        def validate_rif(self,rif):
            db = Database()
            cur = db.cursor_dict()
            if self.current_rif.data != rif.data:
                cur.execute("SELECT cj_rif from clientejuridico WHERE cj_rif = %s;",(rif.data,))
                if cur.fetchone():
                    raise ValidationError('El rif ya esta tomado')
                else:
                    cur.execute("SELECT cn_rif from clientenatural WHERE cn_rif = %s;",(rif.data,))
                    if cur.fetchone():
                        raise ValidationError('El rif ya esta tomado')


class UpdateJForm(FlaskForm):
        email = StringField('Email',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Email(message='Ingrese un email valido'),])
        rif = StringField('RIF',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=20)])
        demcom = StringField('Denominacion Comercial',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=50)])
        razsoc = StringField('Razon Social',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=50)])
        pagweb = StringField('Pagina Web',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=30)])
        capdis = IntegerField('Capital Disponible',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        #Direccion Fiscal
        estados1 = NonValidatingSelectField('Estado',choices=tuple(estados()))
        municipios1 = NonValidatingSelectField('Municipio',choices=[])
        parroquias1 = NonValidatingSelectField('Parroquia',choices=[])
        # Direccion Fisica
        estados2 = NonValidatingSelectField('Estado',choices=tuple(estados()))
        municipios2 = NonValidatingSelectField('Municipio',choices=[])
        parroquias2 = NonValidatingSelectField('Parroquia',choices=[])
        #tlf1 = IntegerField('Capital Disponible',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        submit=SubmitField('Actualizar')
        current_rif = StringField()
        current_email = StringField()

        def validate_email(self,email):
            db = Database()
            cur = db.cursor_dict()
            if self.current_email.data != email.data:
                cur.execute("SELECT cj_email from clientejuridico WHERE cj_email = %s;",(email.data,))
                if cur.fetchone():
                    raise ValidationError('El email ya esta tomado')
                else:
                    cur.execute("SELECT cn_email from clientenatural WHERE cn_email = %s;",(email.data,))
                    if cur.fetchone():
                        raise ValidationError('El email ya esta tomado')

        def validate_rif(self,rif):
            db = Database()
            cur = db.cursor_dict()
            if self.current_rif.data != rif.data:
                cur.execute("SELECT cj_rif from clientejuridico WHERE cj_rif = %s;",(rif.data,))
                if cur.fetchone():
                    raise ValidationError('El rif ya esta tomado')
                else:
                    cur.execute("SELECT cn_rif from clientenatural WHERE cn_rif = %s;",(rif.data,))
                    if cur.fetchone():
                        raise ValidationError('El rif ya esta tomado')


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
        estados1 = NonValidatingSelectField('Estado',choices=tuple(estados()))
        municipios1 = NonValidatingSelectField('Municipio',choices=[])
        parroquias1 = NonValidatingSelectField('Parroquia',choices=[])
        # Direccion Fisica
        estados2 = NonValidatingSelectField('Estado',choices=tuple(estados()))
        municipios2 = NonValidatingSelectField('Municipio',choices=[])
        parroquias2 = NonValidatingSelectField('Parroquia',choices=[])
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
                if cur.fetchone():
                    raise ValidationError('El email ya esta tomado')


        def validate_rif(self,rif):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT cj_rif from clientejuridico WHERE cj_rif = %s;",(rif.data,))
            if cur.fetchone():
                raise ValidationError('El rif ya esta tomado')
            else:
                cur.execute("SELECT cn_rif from clientenatural WHERE cn_rif = %s;",(rif.data,))
                if cur.fetchone():
                    raise ValidationError('El rif ya esta tomado')

        def validate_estados1(self,estados1):
            x =str(estados1.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_estados2(self,estados2):
            x =str(estados2.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_municipios1(self,municipios1):
            x = str(municipios1.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_municipios2(self,municipios2):
            x =str(municipios2.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_parroquias1(self,parroquias1):
            x =str(parroquias1.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_parroquias2(self,parroquias2):
            x =str(parroquias2.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')


class TiendaJForm(FlaskForm):
        rif = StringField('RIF',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=20)])
        email = StringField('Email',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Email(message='Ingrese un email valido')])
        demcom = StringField('Denominacion Comercial',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=50)])
        razsoc = StringField('Razon Social',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=50)])
        pagweb = StringField('Pagina Web',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=1,max=30)])
        capdis = IntegerField('Capital Disponible',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        #Direccion Fiscal
        estados1 = NonValidatingSelectField('Estado',choices=tuple(estados()))
        municipios1 = NonValidatingSelectField('Municipio',choices=[])
        parroquias1 = NonValidatingSelectField('Parroquia',choices=[])
        # Direccion Fisica
        estados2 = NonValidatingSelectField('Estado',choices=tuple(estados()))
        municipios2 = NonValidatingSelectField('Municipio',choices=[])
        parroquias2 = NonValidatingSelectField('Parroquia',choices=[])
        carnet =BooleanField('Desea generar carnet?')
        tienda = NonValidatingSelectField('Seleccione la tienda',choices=tuple(tiendas()))
        submit=SubmitField('Registrar Cliente')

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
                if cur.fetchone():
                    raise ValidationError('El email ya esta tomado')


        def validate_rif(self,rif):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT cj_rif from clientejuridico WHERE cj_rif = %s;",(rif.data,))
            if cur.fetchone():
                raise ValidationError('El rif ya esta tomado')
            else:
                cur.execute("SELECT cn_rif from clientenatural WHERE cn_rif = %s;",(rif.data,))
                if cur.fetchone():
                    raise ValidationError('El rif ya esta tomado')

        def validate_estados1(self,estados1):
            x =str(estados1.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_estados2(self,estados2):
            x =str(estados2.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_municipios1(self,municipios1):
            x = str(municipios1.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_municipios2(self,municipios2):
            x =str(municipios2.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_parroquias1(self,parroquias1):
            x =str(parroquias1.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_parroquias2(self,parroquias2):
            x =str(parroquias2.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')


class TiendaNForm(FlaskForm):
        email = StringField('Email',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Email(message='Ingrese un email valido')])
        rif = StringField('RIF',validators=[DataRequired(message='Este campo no puede dejarse vacio'),Length(min=2,max=20)])
        nom1 = StringField('Primer Nombre',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        nom2 = StringField('Segundo Nombre',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        ap1 = StringField('Primer Apellido',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        ap2 = StringField('Segundo Apellido',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        ci = IntegerField('Cedula',validators=[DataRequired(message='Este campo no puede dejarse vacio')])
        #Direccion
        estados = NonValidatingSelectField('Estado',choices=tuple(estados()))
        municipios = NonValidatingSelectField('Municipio',choices=[])
        parroquias = NonValidatingSelectField('Parroquia',choices=[])
        carnet =BooleanField('Desea generar carnet?')
        tienda = NonValidatingSelectField('Seleccione la tienda',choices=tuple(tiendas()))
        submit=SubmitField('Registrar Cliente')

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
                if cur.fetchone():
                    raise ValidationError('El email ya esta tomado')


        def validate_rif(self,rif):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT cj_rif from clientejuridico WHERE cj_rif = %s;",(rif.data,))
            if cur.fetchone():
                raise ValidationError('El rif ya esta tomado')
            else:
                cur.execute("SELECT cn_rif from clientenatural WHERE cn_rif = %s;",(rif.data,))
                if cur.fetchone():
                    raise ValidationError('El rif ya esta tomado')

        def validate_estados(self,estados):
            x =str(estados.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_municipios(self,municipios):
            x =str(municipios.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_parroquias(self,parroquias):
            x =str(parroquias.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')


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
        estados = NonValidatingSelectField('Estado',choices=tuple(estados()))
        municipios = NonValidatingSelectField('Municipio',choices=[])
        parroquias = NonValidatingSelectField('Parroquia',choices=[])
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
                if cur.fetchone():
                    raise ValidationError('El email ya esta tomado')


        def validate_rif(self,rif):
            db = Database()
            cur = db.cursor_dict()
            cur.execute("SELECT cj_rif from clientejuridico WHERE cj_rif = %s;",(rif.data,))
            if cur.fetchone():
                raise ValidationError('El rif ya esta tomado')
            else:
                cur.execute("SELECT cn_rif from clientenatural WHERE cn_rif = %s;",(rif.data,))
                if cur.fetchone():
                    raise ValidationError('El rif ya esta tomado')

        def validate_estados(self,estados):
            x =str(estados.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_municipios(self,municipios):
            x =str(municipios.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')

        def validate_parroquias(self,parroquias):
            x =str(parroquias.data)
            if x == 'None':
                raise ValidationError('Este campo no puede dejarse vacio')
