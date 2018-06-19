from flask import render_template,url_for,flash,redirect,request,abort,jsonify
from candyucab.forms import RegistrationJForm,LoginForm,PersonaContactoForm,TlfForm,RegistrationNForm,UpdateJForm,UpdateNForm,TiendaJForm,TiendaNForm,ProductoForm
from candyucab import app,bcrypt
from candyucab.user import User
import secrets
import os
from PIL import Image
import psycopg2
from candyucab.db import Database
from flask_login import login_user,current_user,logout_user,login_required


@app.route("/")
@app.route("/home")
def home():
   return render_template('home.html')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/images',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/tiendas/registro",methods=['GET','POST'])
def create_tienda():
    pass

@app.route("/tiendas/<int:ti_id>",methods=['GET','POST'])
def update_tienda(ti_id):
    pass
@app.route("/tiendas",methods=['GET','POST'])
def tiendas():
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT T.*,L.l_nombre AS dir FROM tienda T,lugar L WHERE L.l_id=T.l_id ORDER BY T.ti_id;")
    tiendas = cur.fetchall()
    db.cerrar()
    return render_template('tiendas.html',tiendas=tiendas)

@app.route("/productos/<int:p_id>/update",methods=['GET','POST'])
def update_producto(p_id):
    form = ProductoForm()
    db =Database()
    cur = db.cursor_dict()
    cur.execute("SELECT * FROM producto WHERE p_id =%s;",(p_id,))
    producto = cur.fetchone()
    if form.validate_on_submit():
        if form.picture.data :
            picture_file = save_picture(form.picture.data)
            try:
                cur.execute("""UPDATE producto SET p_nombre = %s,p_imagen=%s,p_desc=%s,p_precio=%s,tp_id =%s WHERE p_id =%s;""",
                (form.nombre.data,picture_file,form.desc.data,form.precio.data,form.tp.data,p_id))
            except:
                print("ERROR updating into producto")
                db.retroceder()
            db.actualizar()
        else:
            try:
                cur.execute("""UPDATE producto SET p_nombre = %s,p_desc=%s,p_precio=%s,tp_id =%s WHERE p_id=%s;""",
                (form.nombre.data,form.desc.data,form.precio.data,form.tp.data,p_id))
            except:
                print("ERROR updating into producto")
                db.retroceder()
            db.actualizar()
        flash('Su producto se ha actualizado exitosamente','success')
        return redirect(url_for('productos'))
    elif request.method == 'GET':
        form.nombre.data = producto['p_nombre']
        form.desc.data = producto['p_desc']
        form.precio.data = producto['p_precio']
    return render_template('createProducto.html',form=form,p_id = p_id)

@app.route("/productos/<int:p_id>/delete",methods=['GET','POST'])
def delete_producto(p_id):
    db = Database()
    cur = db.cursor_dict()
    try:
        cur.execute("DELETE FROM producto WHERE p_id = %s;",(p_id,))
    except:
        print("ERROR deleting into producto")
        db.retroceder()
    db.actualizar()
    return redirect(url_for('productos'))

@app.route("/productos",methods=['GET','POST'])
def productos():
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT T.tp_nombre,P.* FROM producto P,tipo_producto T WHERE P.tp_id = T.tp_id;")
    productos = cur.fetchall()
    return render_template('productos.html',productos = productos)

@app.route("/productos/registro",methods=['GET','POST'])
def create_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.picture.data)
        db = Database()
        cur = db.cursor_dict()
        try:
            cur.execute("""INSERT INTO producto (p_nombre,p_imagen,p_desc,p_precio,tp_id)
                        VALUES (%s, %s,%s,%s,%s);""",
            (form.nombre.data,picture_file,form.desc.data,form.precio.data,form.tp.data))
        except:
            print("ERROR inserting into producto")
            db.retroceder()
        db.actualizar()
        flash('Su producto se ha creado exitosamente','success')
        return redirect(url_for('productos'))
    return render_template('createProducto.html',form=form)

@app.route("/clientes",methods=['GET','POST'])
def clientes():
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT C.*,L.l_nombre AS dir FROM clientenatural C,lugar L WHERE L.l_id=C.l_id ORDER BY C.cn_id;")
    cn = cur.fetchall()
    cur.execute(""" SELECT C.*, fl.l_nombre as fiscal, fa.l_nombre as fisica from clientejuridico C,lugar fl, jur_lug jll,
                    lugar fa,jur_lug jla where C.cj_id = jll.cj_id AND fl.l_id = jll.l_id AND jll.jl_tipo = 'fiscal'
                    AND C.cj_id = jla.cj_id AND fa.l_id = jla.l_id AND jla.jl_tipo = 'fisica'
                    ORDER BY cj_id;""")
    cj = cur.fetchall()
    db.cerrar()
    return render_template('clientes.html',title = 'Clientes',cj = cj,cn = cn)

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
    cur.execute("SELECT distinct P.* from lugar M,lugar P,lugar E where M.l_nombre =%s AND P.fk_lugar = M.l_id AND M.fk_lugar = %s ;",(municipio,estado,))
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
        cur.execute("SELECT * FROM clientejuridico WHERE cj_id = %s",(c_id,))
        cliente = cur.fetchone()
        form = UpdateJForm()
        form.current_rif.data = cliente['cj_rif']
        form.current_email.data = cliente['cj_email']
        if form.validate_on_submit():
            try:
                cur.execute("""UPDATE clientejuridico SET cj_rif = %s,cj_email = %s,cj_capdis = %s,cj_demcom = %s,cj_razsoc=%s ,cj_pagweb = %s WHERE cj_id= %s;""",
                (form.rif.data, form.email.data,form.capdis.data,form.demcom.data,form.razsoc.data,form.pagweb.data,c_id))
            except:
                print("ERROR updating into clientejuridico")
                db.retroceder()
            db.actualizar()

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
            if dirFisica != None:
                try:
                    cur.execute("""UPDATE jur_lug SET l_id = %s WHERE cj_id = %s AND jl_tipo = 'fisica';""",
                    (dirFisica['l_id'],c_id,))
                except:
                    print("ERROR updating into lugar_clientej fisica")
                    db.retroceder()

            if dirFiscal != None:
                try:
                    cur.execute("""UPDATE jur_lug SET l_id = %s WHERE cj_id = %s AND jl_tipo = 'fiscal';""",
                    (dirFiscal['l_id'],c_id,))
                except:
                    print("ERROR updating into lugar_clientej fiscal")
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

        cur.execute("SELECT * FROM clientenatural WHERE cn_id = %s",(c_id,))
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

@app.route("/clientes/<int:c_id>/<string:tipo>/carnet",methods=['GET','POST'])
def carnet(c_id,tipo):
    db = Database()
    cur = db.cursor_dict()
    if tipo == 'cj':
        cur.execute("""SELECT C.car_num,J.cj_demcom,J.cj_rif,ti_nombre FROM carnet C,clientejuridico J,tienda
                    WHERE J.ti_cod = ti_id AND J.cj_id=%s AND J.cj_id=C.cj_id;""",(c_id,))
        cliente = cur.fetchone()
        return render_template('carnet.html',cliente=cliente,tipo = 'cj')
    else:
        cur.execute("""SELECT C.car_num,N.cn_nom1,N.cn_ap1,N.cn_ci,ti_nombre FROM carnet C,clientenatural N,tienda
                    WHERE N.ti_cod = ti_id AND N.cn_id=%s AND N.cn_id=C.cn_id;""",(c_id,))
        cliente = cur.fetchone()
        return render_template('carnet.html',cliente=cliente,tipo = 'cn')

@app.route("/clientes/register/<string:tipo>",methods=['GET','POST'])  #Registro de tienda
def registro(tipo):
    db = Database()
    cur = db.cursor_dict()
    if tipo == 'cj':
        form = TiendaJForm()
        if form.validate_on_submit():
            db = Database()
            cur = db.cursor_dict()
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
            cur = db.cursor()
            try:
                cur.execute("""INSERT INTO clientejuridico (cj_rif, cj_email,cj_demcom,cj_razsoc,cj_capdis,cj_pagweb,ti_cod)
                VALUES (%s, %s,%s,%s,%s,%s,%s) RETURNING cj_id;""",
                (form.rif.data,form.email.data,form.demcom.data,form.razsoc.data,form.capdis.data,form.pagweb.data,form.tienda.data,))
            except:
                print("ERROR inserting into clientejuridico")
                db.retroceder()
            cj = cur.fetchone()[0]
            db.actualizar()
            try:
                cur.execute("""INSERT INTO jur_lug (l_id,cj_id,jl_tipo)
                VALUES (%s, %s,%s);""",
                (dirFiscal['l_id'],cj,'fiscal',))
            except:
                print("ERROR inserting into lugar_clientej fiscal")
                db.retroceder()
            #dirFisica
            try:
                cur.execute("""INSERT INTO jur_lug (l_id,cj_id,jl_tipo)
                VALUES (%s, %s,%s);""",
                (dirFisica['l_id'],cj,'fisica',))
            except:
                print("ERROR inserting into lugar_clientej fisica")
                db.retroceder()
            db.actualizar()
            if form.carnet.data == True:
                cur = db.cursor_dict()
                cur.execute("SELECT C.car_num,C.d_id from carnet C, departamento D where D.ti_cod = %s AND C.d_id = D.d_id ORDER BY C.car_num DESC LIMIT 1;",(form.tienda.data,))
                carnet_num = cur.fetchone()
                num = carnet_num['car_num'][3:]
                if int(form.tienda.data) < 10:
                    carnet = "0{}-{}"
                    if int(num)+1 < 10:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"0000000"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()

                    elif int (num)+1 <100:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"000000"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 1000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"00000"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 10000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"0000"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 100000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"000"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 1000000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"00"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 10000000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"0"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                else:
                    carnet = "{}-{}"
                    if int(num)+1 < 10:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"0000000"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int (num)+1 <100:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"000000"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 1000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"00000"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 10000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"0000"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 100000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"000"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 1000000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"00"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 10000000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cj_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"0"+str(int(num)+1)),cj,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                db.actualizar()
                return redirect(url_for('carnet',c_id = cj,tipo = 'cj'))

            flash('Su cuenta se ha creado exitosamente','success')
            return redirect(url_for('clientes'))
        return render_template('TiendaJ.html',title='Register',form=form)
    elif tipo == 'cn':
        form = TiendaNForm()
        if form.validate_on_submit():
            db = Database()
            cur = db.cursor_dict()
            cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                        E.l_id = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                        P.l_nombre = %s AND P.fk_lugar = M.l_id;
                        """,(form.estados.data,form.municipios.data,form.parroquias.data,))
            direccion = cur.fetchone()
            cur = db.cursor()
            try:
                cur.execute("""INSERT INTO clientenatural (cn_rif, cn_email,cn_nom1,cn_nom2,cn_ap1,cn_ap2,l_id,cn_ci,ti_cod)
                VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s) RETURNING cn_id;""",
                (form.rif.data,form.email.data,form.nom1.data,form.nom2.data,form.ap1.data,form.ap2.data,direccion['l_id'],form.ci.data,form.tienda.data))
            except:
                print("ERROR inserting into clientenatural")
                db.retroceder()

            cn = cur.fetchone()[0]
            db.actualizar()
            if form.carnet.data == True:
                cur = db.cursor_dict()
                cur.execute("SELECT C.car_num,C.d_id from carnet C, departamento D where D.ti_cod = %s AND C.d_id = D.d_id ORDER BY C.car_num DESC LIMIT 1;",(form.tienda.data,))
                carnet_num = cur.fetchone()
                num = carnet_num['car_num'][3:]
                if int(form.tienda.data) < 10:
                    carnet = "0{}-{}"
                    if int(num)+1 < 10:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"0000000"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()

                    elif int (num)+1 <100:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"000000"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 1000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"00000"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 10000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"0000"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 100000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"000"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 1000000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"00"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 10000000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s);""",
                            (carnet.format(form.tienda.data,"0"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                else:
                    carnet = "{}-{}"
                    if int(num)+1 < 10:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"0000000"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int (num)+1 <100:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"000000"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 1000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"00000"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 10000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"0000"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 100000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"000"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 1000000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"00"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                    elif int(num)+1 < 10000000:
                        try:
                            cur.execute("""INSERT INTO carnet (car_num,cn_id,d_id) VALUES (%s,%s,%s)""",
                            (carnet.format(form.tienda.data,"0"+str(int(num)+1)),cn,carnet_num['d_id'],))
                        except:
                            print("ERROR inserting into carnet")
                            db.retroceder()
                db.actualizar()
                return redirect(url_for('carnet',c_id = cn,tipo = 'cn'))

            flash('Su cuenta se ha creado exitosamente','success')
            return redirect(url_for('clientes'))
        return render_template('TiendaN.html',title='Register',form=form) #Registro tienda fisica

@app.route("/register")  #Registro online
def register():
   return render_template('register.html')  #Registro online

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
                    E.l_id = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                    P.l_nombre = %s AND P.fk_lugar = M.l_id;
                    """,(form.estados1.data,form.municipios1.data,form.parroquias1.data,))
        dirFiscal = cur.fetchone()
        cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                    E.l_id = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                    P.l_nombre = %s AND P.fk_lugar = M.l_id;
                    """,(form.estados2.data,form.municipios2.data,form.parroquias2.data,))
        dirFisica = cur.fetchone()
        cur = db.cursor()
        try:
            cur.execute("""INSERT INTO clientejuridico (cj_rif, cj_email,cj_demcom,cj_razsoc,cj_capdis,cj_pagweb)
            VALUES (%s, %s,%s,%s,%s,%s) RETURNING cj_id;""",
            (form.rif.data,form.email.data,form.demcom.data,form.razsoc.data,form.capdis.data,form.pagweb.data,))
        except:
            print("ERROR inserting into clientejuridico")
            db.retroceder()
        cj = cur.fetchone()[0]
        db.actualizar()
        try:
            cur.execute("""INSERT INTO jur_lug (l_id,cj_id,jl_tipo)
            VALUES (%s, %s,%s);""",
            (dirFiscal['l_id'],cj,'fiscal',))
        except:
            print("ERROR inserting into lugar_clientej fiscal")
            db.retroceder()
        #dirFisica
        try:
            cur.execute("""INSERT INTO jur_lug (l_id,cj_id,jl_tipo)
            VALUES (%s, %s,%s);""",
            (dirFisica['l_id'],cj,'fisica',))
        except:
            print("ERROR inserting into lugar_clientej fisica")
            db.retroceder()
        try:
            cur.execute("""INSERT INTO usuario (u_username, u_password,cj_id)
            VALUES (%s, %s,%s);""",
            (form.username.data,hashed_pw,cj))
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
                    E.l_id = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                    P.l_nombre = %s AND P.fk_lugar = M.l_id;
                    """,(form.estados.data,form.municipios.data,form.parroquias.data,))
        direccion = cur.fetchone()
        cur = db.cursor()
        try:
            cur.execute("""INSERT INTO clientenatural (cn_rif, cn_email,cn_nom1,cn_nom2,cn_ap1,cn_ap2,l_id,cn_ci)
            VALUES (%s, %s,%s,%s,%s,%s,%s,%s) RETURNING cn_id;""",
            (form.rif.data,form.email.data,form.nom1.data,form.nom2.data,form.ap1.data,form.ap2.data,direccion['l_id'],form.ci.data))
        except:
            print("ERROR inserting into clientenatural")
            db.retroceder()

        cn = cur.fetchone()[0]
        db.actualizar()
        try:
            cur.execute("""INSERT INTO usuario (u_username, u_password,cn_id)
            VALUES (%s, %s,%s);""",
            (form.username.data,hashed_pw,cn))
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
