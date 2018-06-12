from flask import render_template,url_for,flash,redirect,request,abort
from candyucab.forms import RegistrationJForm,LoginForm,PersonaContactoForm,TlfForm,RegistrationNForm
from candyucab import app,bcrypt
from candyucab.user import User
import psycopg2
from candyucab.db import Database
from flask_login import login_user,current_user,logout_user,login_required

@app.route("/")
@app.route("/home")
def home():
   return render_template('home.html')

@app.route("/clientes")
def clientes():
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT * FROM clientenatural;")
    cn = cur.fetchall()
    cur.execute("SELECT * FROM clientejuridico;")
    cj = cur.fetchall()
    db.cerrar()
    return render_template('clientes.html',title = 'Clientes',cj = cj,cn = cn)

<<<<<<< HEAD
@app.route("/clientes/<int:c_id>")
def cliente(c_id):
    return render_template('cliente.html')
=======
@app.route('/municipio/<int:fk_lugar>',methods=['GET','POST'])
def municipio(fk_lugar):
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT M.* from lugar M WHERE  M.fk_lugar = %s;",(fk_lugar,))
    municipios = cur.fetchall()
    db.cerrar()
    munArray = []
    for municipio in municipios:
        munArray.append(municipio)

    return jsonify({'municipios': munArray})

@app.route('/parroquia/<string:municipio>/<int:estado>',methods=['GET','POST'])
def parroquia(municipio,estado):
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT distinct P.* from lugar M,lugar P,lugar E where M.l_nombre =%s AND P.fk_lugar = M.l_id AND P.l_tipo = 'P' AND M.fk_lugar = %s ;",(municipio,estado,))
    parroquias = cur.fetchall()
    db.cerrar()
    paqArray = []
    for parroquia in parroquias:
        paqArray.append(parroquia)

    return jsonify({'parroquias': paqArray})

@app.route("/clientes/<int:c_id>/<string:tipo>",methods=['GET','POST'])
def update_cliente(c_id,tipo):
    db = Database()
    cur = db.cursor_dict()
    if tipo == 'cj':
        cur.execute("SELECT * FROM clientejuridico",(c_id,))
        cliente = cur.fetchone()
        form = UpdateJForm()
        form.current_rif.data = cliente['cj_rif']
        form.current_email.data = cliente['cj_email']
        if form.validate_on_submit():
            cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                        E.l_id = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                        P.l_nombre = %s AND P.fk_lugar = M.l_id;
                        """,(form.estados1.data,form.municipios1.data,form.parroquias1.data,))
            dirFiscal = cur.fetchone()
            cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                        E.l_id = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                        P.l_nombre = %s AND P.fk_lugar = M.l_id;
                        """,(form.estados2.data,form.municipios2.data,form.parroquias2.data,))
            dirFisica = cur.fetchone()

            try:
                cur.execute("""UPDATE clientejuridico SET cj_rif = %s,cj_email = %s,cj_capdis = %s,cj_demcom = %s,cj_razsoc=%s ,cj_pagweb = %s WHERE cj_id= %s;""",
                (form.rif.data, form.email.data,form.capdis.data,form.demcom.data,form.razsoc.data,form.pagweb.data,c_id))
            except:
                print("ERROR updating into clientejuridico")
                db.retroceder()
            db.actualizar()
            flash('Tu cliente ha sido actualizada','success')
            return redirect(url_for('clientes'))
        elif request.method == 'GET':
            form.rif.data = cliente['cj_rif']
            form.email.data = cliente['cj_email']
            form.capdis.data = cliente['cj_capdis']
            form.demcom.data = cliente['cj_demcom']
            form.razsoc.data = cliente['cj_razsoc']
            form.pagweb.data = cliente['cj_pagweb']
        return render_template('clienteJ.html',form = form,c_id = c_id)
    elif tipo == 'cn':

        cur.execute("SELECT * FROM clientenatural",(c_id,))
        cliente = cur.fetchone()
        form = UpdateNForm()
        form.current_rif.data = cliente['cn_rif']
        form.current_email.data = cliente['cn_email']
        form.current_ci.data = cliente['cn_ci']
        if form.validate_on_submit():
            cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                        E.l_id = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                        P.l_nombre = %s AND P.fk_lugar = M.l_id;
                        """,(form.estados.data,form.municipios.data,form.parroquias.data,))
            direccion = cur.fetchone()
            if direccion == None:
                direccion = cliente
            try:
                cur.execute("""UPDATE clientenatural SET cn_rif = %s,cn_email = %s,cn_nom1 = %s,cn_nom2 = %s,cn_ap1=%s, cn_ap2=%s,cn_ci = %s,l_id = %s WHERE cn_id= %s;""",
                (form.rif.data, form.email.data,form.nom1.data,form.nom2.data,form.ap1.data,form.ap2.data,form.ci.data,direccion['l_id'],c_id))
            except:
                print("ERROR updating into clientenatural")
                db.retroceder()
            db.actualizar()
            flash('Tu cliente ha sido actualizada','success')
            return redirect(url_for('clientes'))
        elif request.method == 'GET':
            form.rif.data = cliente['cn_rif']
            form.email.data = cliente['cn_email']
            form.nom1.data = cliente['cn_nom1']
            form.nom2.data = cliente['cn_nom2']
            form.ap1.data = cliente['cn_ap1']
            form.ap2.data = cliente['cn_ap2']
            form.ci.data = cliente['cn_ci']

        return render_template('clienteN.html',form = form,c_id = c_id)

@app.route("/clientes/<int:c_id>/<string:tipo>/delete",methods=['GET','POST'])
def delete_cliente(c_id,tipo):
    db = Database()
    cur = db.cursor_dict()
    if tipo == 'cj':
        try:
            cur.execute("DELETE FROM clientejuridico WHERE cj_id = %s;",(c_id,))
        except:
            print("ERROR deleting clientejuridico")
            db.retroceder()
        db.actualizar()
        db.cerrar()
        flash('Tu cliente ha sido eliminado','success')
        return redirect(url_for('clientes'))
    elif tipo == 'cn':
        print(c_id)
        try:
            cur.execute("DELETE FROM clientenatural WHERE cn_id = %s;",(c_id,))
        except:
            print("ERROR deleting clientenatural")
            db.retroceder()
        db.actualizar()
        db.cerrar()
        flash('Tu cliente ha sido eliminado','success')
        return redirect(url_for('clientes'))
>>>>>>> 19c64345d5ffeec56569c78f51ed6b0ce02f8b81

@app.route("/register")
def register():
   return render_template('register.html')

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

@app.route("/registerN",methods=['GET','POST'])
def registerN():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationNForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db = Database()
        cur = db.cursor_dict()
        cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                    E.l_nombre = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                    P.l_nombre = %s AND P.fk_lugar = M.l_id;
                    """,(form.est1.data,form.municipio1.data,form.par1.data,))
        direccion = cur.fetchone()
        try:
            cur.execute("""INSERT INTO clientenatural (cn_rif, cn_email,cn_nom1,cn_nom2,cn_ap1,cn_ap2,l_id,cn_ci)
            VALUES (%s, %s,%s,%s,%s,%s,%s,%s);""",
            (form.rif.data,form.email.data,form.nom1.data,form.nom2.data,form.ap1.data,form.ap2.data,direccion['l_id'],form.ci.data))
        except:
            print("ERROR inserting into clientenatural")
            db.retroceder()
        cur.execute("SELECT cn_id FROM clientenatural WHERE cn_email = %s;",(form.email.data,))
        cn = cur.fetchone()
        try:
            cur.execute("""INSERT INTO usuario (u_username, u_password,cn_id)
            VALUES (%s, %s,%s);""",
            (form.username.data,hashed_pw,cn['cn_id']))
        except:
            print("ERROR inserting into user")
            db.retroceder()
        db.actualizar()

        flash('Su cuenta se ha creado exitosamente','success')
        return redirect(url_for('login'))
    return render_template('registerN.html',title='Register',form=form)


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
