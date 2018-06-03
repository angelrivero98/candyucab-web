from flask import render_template,url_for,flash,redirect,request
from candyucab.forms import RegistrationJForm,LoginForm,PersonaContactoForm,TlfForm
from candyucab import app,bcrypt
from candyucab.user import User
import psycopg2
from candyucab.db import Database
from flask_login import login_user,current_user,logout_user,login_required

@app.route("/")
@app.route("/home")
def home():
   return render_template('home.html')

@app.route("/register")
def register():
   return render_template('register.html')

@app.route("/register2/<int:cID>&<int:telefonos>&<int:personas>&<string:tipo>",methods=['GET','POST'])
def register2(cID,telefonos,personas,tipo):
    if tipo == 'cj':
        form = Register2JForm()
        if form.validate_on_submit():
            db = Database()
            cur = db.cursor_dict()
            for telefono in form.telefonos:
                if telefono.numero.data != 0:
                    try:
                        cur.execute("""INSERT INTO telefono (t_num,cj_id)
                        VALUES (%s, %s,%s);""",
                        (telefono.numero.data,cID,))
                    except:
                        print("ERROR inserting into telefono")
                        db.retroceder()
            for persona in form.personas:
                try:
                    cur.execute("""INSERT INTO personadecontacto (pc_nombre,pc_apellido,cj_id)
                    VALUES (%s, %s,%s);""",
                    (persona.nombre.data,persona.apellido.data,cID,))
                except:
                    print("ERROR inserting into telefono")
                    db.retroceder()
            db.actualizar()
            flash('Sus datos se han cargado correctamente','success')
            return redirect(url_for('login'))

    return render_template('register2J.html',title='Register',form=form,cID=cID,num_tlf=telefonos,num_per=personas)

@app.route("/new_tlf",methods=['GET','POST'])
@login_required
def new_tlf():
    form = TlfForm()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        if current_user.cj_id != 0:
            try:
                cur.execute("""INSERT INTO telefono (t_num,cj_id)
                VALUES (%s, %s);""",
                (form.numero.data,current_user.cj_id,))
            except:
                print("ERROR inserting into telefono")
                db.retroceder()
            db.actualizar()
        else:
            try:
                cur.execute("""INSERT INTO telefono (t_num,cn_id)
                VALUES (%s, %s);""",
                (form.numero.data,current_user.cn_id,))
            except:
                print("ERROR inserting into telefono")
                db.retroceder()
            db.actualizar()
        flash('Su telefono se ha guardado exitosamente','success')
        return redirect(url_for('home'))

    return render_template('new_tlf.html',title='Nuevo Telefono',form=form)

@app.route("/new_persona",methods=['GET','POST'])
@login_required
def new_persona():
    form = PersonaContactoForm()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        try:
            cur.execute("""INSERT INTO personadecontacto (pc_nombre,pc_apellido,cj_id)
            VALUES (%s, %s,%s);""",
            (form.nombre.data,form.apellido.data,current_user.cj_id,))
        except:
            print("ERROR inserting into telefono")
            db.retroceder()
        db.actualizar()
        flash('Su persona de contacto se ha guardado exitosamente','success')
        return redirect(url_for('home'))

    return render_template('new_persona.html',title='Nueva Persona',form=form)

@app.route("/registerJ",methods=['GET','POST'])
def registerJ():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationJForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db = Database()
        cur = db.cursor_dict()
        cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                    E.l_nombre = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                    P.l_nombre = %s AND P.fk_lugar = M.l_id;
                    """,(form.est1.data,form.municipio1.data,form.par1.data,))
        dirFiscal = cur.fetchone()
        cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                    E.l_nombre = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                    P.l_nombre = %s AND P.fk_lugar = M.l_id;
                    """,(form.est2.data,form.municipio2.data,form.par2.data,))
        dirFisica = cur.fetchone()
        try:
            cur.execute("""INSERT INTO clientejuridico (cj_rif, cj_email,cj_demcom,cj_razsoc,cj_capdis,cj_pagweb)
            VALUES (%s, %s,%s,%s,%s,%s);""",
            (form.rif.data,form.email.data,form.demcom.data,form.razsoc.data,form.capdis.data,form.pagweb.data,))
        except:
            print("ERROR inserting into clientejuridico")
            db.retroceder()
        db.actualizar()
        cur.execute("SELECT cj_id FROM clientejuridico WHERE cj_email = %s;",(form.email.data,))
        cj = cur.fetchone()
        #dirFiscal
        try:
            cur.execute("""INSERT INTO jur_lug (l_id,cj_id,jl_tipo)
            VALUES (%s, %s,%s);""",
            (dirFiscal['l_id'],cj['cj_id'],'fiscal',))
        except:
            print("ERROR inserting into lugar_clientej fiscal")
            db.retroceder()
        #dirFisica
        try:
            cur.execute("""INSERT INTO jur_lug (l_id,cj_id,jl_tipo)
            VALUES (%s, %s,%s);""",
            (dirFisica['l_id'],cj['cj_id'],'fisica',))
        except:
            print("ERROR inserting into lugar_clientej fisica")
            db.retroceder()
        try:
            cur.execute("""INSERT INTO usuario (u_username, u_password,cj_id)
            VALUES (%s, %s,%s);""",
            (form.username.data,hashed_pw,cj['cj_id']))
        except:
            print("ERROR inserting into user")
            db.retroceder()
        db.actualizar()

        flash('Su cuenta se ha creado exitosamente','success')
        return redirect(url_for('login'))
    return render_template('registerJ.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        cur.execute("SELECT * from usuario WHERE u_username = %s;",(form.username.data,))
        user_type = cur.fetchone()
        if user_type:
            user = User(user_type)
            if user and bcrypt.check_password_hash(user.u_password,form.password.data):
                login_user(user,remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(url_for('home'))
            else:
                flash('Contraseña Incorrecta','danger')
        else:
            flash('Usuario no encontrado','danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#@app.route("/account")
#@login_required
#def account():
#    return render_template('account.html',title='Account')
