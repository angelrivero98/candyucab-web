from flask import render_template,url_for,flash,redirect,request,abort,jsonify
from candyucab.forms import RegistrationJForm,LoginForm,PersonaContactoForm,TlfForm,RegistrationNForm,UpdateJForm,UpdateNForm,TiendaJForm,TiendaNForm
from candyucab.forms import  ProductoForm,TiendaForm,UpdateTiendaForm,AsistenciaForm,TarjetaDebito,TarjetaCredito,ChequeForm,DiarioDulce,DescuentoForm
from candyucab import app,bcrypt
from candyucab.user import User
import secrets
import os
import datetime
from datetime import date,timedelta
import pyexcel as p
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

@app.route("/ofertas/<int:dd_id>/<int:e_id>/registro",methods=['GET','POST'])
def create_oferta(dd_id,e_id):
    form = DiarioDulce()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        try:
            cur.execute("""INSERT INTO pro_diario (pd_descuento,dd_id,p_id)
                            VALUES (%s,%s,%s);""",(form.descuento.data/100,dd_id,form.producto.data))
        except:
            print("ERROR inserting into pro_diario")
            db.retroceder()
        db.actualizar()
        flash('Su oferta se ha creado exitosamente','success')
        return redirect(url_for('ofertas',e_id=e_id))
    return render_template('createOferta.html',form=form,e_id=e_id)

@app.route("/ofertas/update/<int:pd_id>/<int:e_id>",methods=['GET','POST'])
def update_oferta(pd_id,e_id):
    form = DescuentoForm()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        try:
            cur.execute("""UPDATE pro_diario SET pd_descuento = %s WHERE pd_id=%s;""",
                        (form.descuento.data/100,pd_id,))
        except:
            print("ERROR updating into pro_diario")
            db.retroceder()
        db.actualizar()
        return redirect(url_for('ofertas',e_id=e_id))
    return render_template('createOferta.html',form=form,pd_id=pd_id,e_id=e_id)


@app.route("/ofertas/delete/<int:pd_id>/<int:e_id>",methods=['GET','POST'])
def delete_oferta(pd_id,e_id):
    db = Database()
    cur = db.cursor_dict()
    try:
        cur.execute("""DELETE FROM pro_diario WHERE pd_id=%s;""",(pd_id,))
    except:
        print("ERROR deleting into pro_diario")
        db.retroceder()
    db.actualizar()
    return redirect(url_for('ofertas',e_id=e_id))

@app.route("/ofertas/<int:e_id>",methods=['GET','POST'])
def ofertas(e_id):
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT * FROM diariodulce WHERE dd_femision = CURRENT_DATE;")
    diario = cur.fetchone()
    if diario:
        cur.execute("SELECT P.p_nombre,P.p_precio, PD.* from pro_diario PD,producto P where PD.dd_id = %s AND P.p_id=PD.p_id;",(diario['dd_id'],))
        productos = cur.fetchall()
        return render_template('ofertas.html',productos=productos,dd_id=diario['dd_id'],e_id=e_id)
    else:
        end_date = datetime.datetime.strptime(date.today().strftime("%d-%m-%Y"), "%d-%m-%Y") + timedelta(days=20)
        cur = db.cursor()
        try:
            cur.execute("""INSERT INTO diariodulce (dd_ffinal,e_id)
                            VALUES (%s,%s) RETURNING dd_id;""",(end_date.date(),e_id))
        except:
            print("ERROR inserting into diariodulce")
            db.retroceder()
        diario = cur.fetchone()[0]
        db.actualizar()
        return render_template('ofertas.html',dd_id=diario,e_id=e_id)


@app.route("/asistencia",methods=['GET','POST'])
def asistencia():
    form = AsistenciaForm()
    db = Database()
    cur = db.cursor_dict()
    if form.validate_on_submit():
        records = p.iget_records(file_name=form.excel.data.filename)
        for record in records:
            if record['CEDULA'] != '':
                cur.execute("SELECT e_id from empleado WHERE e_ci=%s;",(int(float(record['CEDULA'])),))
                id = cur.fetchone()
                if record['FECHA_HORA_SALIDA'] != '' and record['FECHA_HORA_ENTRADA'] != '':
                    try:
                        cur.execute("""INSERT INTO asistencia (as_fecha_entrada,as_fecha_salida,e_id) VALUES
                            (to_timestamp(%s, 'DD-MM-YYYY HH24:MI'),to_timestamp(%s, 'DD-MM-YYYY HH24:MI'),%s);""",
                            (record['FECHA_HORA_ENTRADA'],record['FECHA_HORA_SALIDA'],id['e_id'],))
                    except:
                        print("ERROR inserting into asistencia")
                        db.retroceder()
                    db.actualizar()
        return redirect(url_for('home'))

    return render_template('asistencia.html',form=form)

@app.route("/tiendas/registro",methods=['GET','POST'])
def create_tienda():
    form = TiendaForm()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                    E.l_id = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                    P.l_nombre = %s AND P.fk_lugar = M.l_id;
                    """,(form.estados.data,form.municipios.data,form.parroquias.data,))
        direccion = cur.fetchone()
        if int(form.tipo.data) == 1:
            tipo = 'Candy Shop'
        else:
            tipo = 'Mini Candy Shop'
        try:
            cur.execute("""INSERT INTO tienda (ti_nombre,ti_tipo,l_id)
                        VALUES (%s, %s,%s);""",
                        (form.nombre.data,tipo,direccion['l_id'],))
        except:
            print("ERROR inserting into tienda")
            db.retroceder()
        db.actualizar()
        flash('Su tienda se ha creado exitosamente','success')
        return redirect(url_for('tiendas'))
    return render_template('createTienda.html',form=form)

@app.route("/tiendas/<int:ti_id>/delete",methods=['GET','POST'])
def delete_tienda(ti_id):
    db = Database()
    cur = db.cursor_dict()
    try:
        cur.execute("DELETE FROM tienda WHERE ti_id = %s;",(ti_id,))
    except:
        print("ERROR deleting into tienda")
        db.retroceder()
    db.actualizar()
    return redirect(url_for('tiendas'))

@app.route("/tiendas/<int:ti_id>/update",methods=['GET','POST'])
def update_tienda(ti_id):
    form = UpdateTiendaForm()
    db =Database()
    cur = db.cursor_dict()
    cur.execute("SELECT * FROM tienda WHERE ti_id =%s;",(ti_id,))
    tienda = cur.fetchone()
    if form.validate_on_submit():
        cur.execute("""SELECT P.l_id from lugar E, lugar M , lugar P where
                    E.l_id = %s AND E.l_tipo = 'E' AND M.l_nombre = %s AND M.fk_lugar= E.l_id AND
                    P.l_nombre = %s AND P.fk_lugar = M.l_id;
                    """,(form.estados.data,form.municipios.data,form.parroquias.data,))
        direccion = cur.fetchone()
        if direccion == None:
            direccion = tienda
        if int(form.tipo.data) == 1:
            tipo = 'Candy Shop'
        else:
            tipo = 'Mini Candy Shop'

        try:
            cur.execute("""UPDATE tienda SET ti_nombre=%s,ti_tipo=%s,l_id=%s WHERE ti_id=%s;""",
                        (form.nombre.data,tipo,direccion['l_id'],ti_id,))
        except:
            print("ERROR updating into tienda")
            db.retroceder()
        db.actualizar()
        flash('Su tienda se ha actualizado exitosamente','success')
        return redirect(url_for('tiendas'))
    elif request.method == 'GET':
        form.nombre.data = tienda['ti_nombre']
    return render_template('createTienda.html',form=form,ti_id = ti_id)

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
        if form.picture.data:
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
        else:
            flash('Su producto no se ha guardado porque no se suministro imagen','danger')
        return redirect(url_for('productos'))
    return render_template('createProducto.html',form=form)

@app.route("/clientes",methods=['GET','POST'])
def clientes():
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT C.*,L.l_nombre AS dir FROM clientenatural C,lugar L WHERE L.l_id=C.l_id;")
    cn = cur.fetchall()
    cur.execute("""SELECT C.*,fisica.l_nombre as fisica,fiscal.l_nombre as fiscal FROM clientejuridico C,jur_lug FL,jur_lug FA ,lugar as fiscal,lugar as fisica
                        WHERE (C.cj_id = FL.cj_id  OR C.cj_id = FA.cj_id)
                        AND (FL.l_id=fiscal.l_id AND FL.jl_tipo='fiscal')  AND (FA.l_id=fisica.l_id AND FA.jl_tipo='fisica') ;""")
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

@app.route("/metodo")
@login_required
def metodo():
   return render_template('metodo.html')

@app.route("/credito/<string:tipo>/<int:c_id>",methods=['GET','POST'])
@login_required
def credito(tipo,c_id):
    form = TarjetaCredito()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        if tipo == 'cj':
            try:
                cur.execute("""INSERT INTO tarjetacredito (tc_num,tc_fvenc,tc_codseg,tc_ncompl,cj_id)
                            VALUES (%s, %s,%s,%s,%s);""",
                (form.numero.data,form.fvenc.data,form.codigo.data,form.nombre.data,c_id,))
            except:
                print("ERROR inserting into tarjetacredito cj")
                db.retroceder()
            db.actualizar()
        elif tipo == 'cn':
            try:
                cur.execute("""INSERT INTO tarjetacredito (tc_num,tc_fvenc,tc_codseg,tc_ncompl,cn_id)
                            VALUES (%s, %s,%s,%s,%s);""",
                (form.numero.data,form.fvenc.data,form.codigo.data,form.nombre.data,c_id,))
            except:
                print("ERROR inserting into tarjetacredito cn")
                db.retroceder()
            db.actualizar()
        flash('Su tarjeta de credito se ha guardado exitosamente','success')
        return redirect(url_for('cliente_home'))

    return render_template('credito.html',title='Tarjeta Credito',form=form)

@app.route("/debito/<string:tipo>/<int:c_id>",methods=['GET','POST'])
@login_required
def debito(tipo,c_id):
    form = TarjetaDebito()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        if int(form.banco.data) == 1:
            banco = 'Mercantil'
        elif int(form.banco.data) == 2:
            banco = 'BOD'
        elif int(form.banco.data) == 3:
            banco = 'Banesco'
        elif int(form.banco.data) == 4:
            banco = 'Banco Plaza'
        elif int(form.banco.data) == 5:
            banco = 'Provincial'

        if tipo == 'cj':
            try:
                cur.execute("""INSERT INTO tarjetadebito (td_num,td_banco,td_fvenc,td_ncompl,cj_id)
                            VALUES (%s, %s,%s,%s,%s);""",
                (form.numero.data,banco,form.fvenc.data,form.nombre.data,c_id,))
            except:
                print("ERROR inserting into tarjetadebito cj")
                db.retroceder()
            db.actualizar()
        elif tipo == 'cn':
            try:
                cur.execute("""INSERT INTO tarjetadebito (td_num,td_banco,td_fvenc,td_ncompl,cn_id)
                        VALUES (%s, %s,%s,%s,%s);""",
                        (form.numero.data,banco,form.fvenc.data,form.nombre.data,c_id,))
            except:
                print("ERROR inserting into tarjetadebito cn")
                db.retroceder()
            db.actualizar()
            flash('Su tarjeta de debito se ha guardado exitosamente','success')
        return redirect(url_for('cliente_home'))
    return render_template('debito.html',title='Tarjeta Debito',form=form)

@app.route("/cheque/<string:tipo>/<int:c_id>",methods=['GET','POST'])
@login_required
def cheque(tipo,c_id):
    form = ChequeForm()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        if tipo == 'cj':
            try:
                cur.execute("""INSERT INTO cheque (ch_num,ch_faplicar,ch_ncompl,cj_id)
                            VALUES (%s, %s,%s,%s);""",
                (form.numero.data,form.faplicar.data,form.nombre.data,c_id,))
            except:
                print("ERROR inserting into cheque cj")
                db.retroceder()
            db.actualizar()
        elif tipo == 'cn':
            try:
                cur.execute("""INSERT INTO cheque (ch_num,ch_faplicar,ch_ncompl,cn_id)
                            VALUES (%s, %s,%s,%s);""",
                (form.numero.data,form.faplicar.data,form.nombre.data,c_id,))
            except:
                print("ERROR inserting into cheque cn")
                db.retroceder()
            db.actualizar()
        flash('Su cheque se ha guardado exitosamente','success')
        return redirect(url_for('cliente_home'))

    return render_template('cheque.html',title='Cheque',form=form)

@app.route("/new_tlf/<string:tipo>/<int:c_id>",methods=['GET','POST'])
@login_required
def new_tlf(tipo,c_id):
    form = TlfForm()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        if tipo == 'cj':
            try:
                cur.execute("""INSERT INTO telefono (t_num,cj_id)
                            VALUES (%s, %s);""",
                (form.numero.data,c_id,))
            except:
                print("ERROR inserting into telefono")
                db.retroceder()
            db.actualizar()
        else:
            try:
                cur.execute("""INSERT INTO telefono (t_num,cn_id)
                            VALUES (%s, %s);""",
                (form.numero.data,c_id,))
            except:
                print("ERROR inserting into telefono")
                db.retroceder()
            db.actualizar()
        flash('Su telefono se ha guardado exitosamente','success')
        return redirect(url_for('home'))

    return render_template('new_tlf.html',title='Nuevo Telefono',form=form)

@app.route("/new_persona/<int:c_id>",methods=['GET','POST'])
@login_required
def new_persona(c_id):
    form = PersonaContactoForm()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        try:
            cur.execute("""INSERT INTO personadecontacto (pc_nombre,pc_apellido,cj_id)
            VALUES (%s, %s,%s);""",
            (form.nombre.data,form.apellido.data,c_id,))
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
        print(dirFisica['l_id'])
        try:
            cur.execute("""INSERT INTO clientejuridico (cj_rif, cj_email,cj_demcom,cj_razsoc,cj_capdis,cj_pagweb)
            VALUES (%s, %s,%s,%s,%s,%s) RETURNING cj_id;""",
            (form.rif.data,form.email.data,form.demcom.data,form.razsoc.data,form.capdis.data,form.pagweb.data,))
        except:
            print("ERROR inserting into clientejuridico")
            db.retroceder()
        cj = cur.fetchone()[0]
        db.actualizar()
        #cur.execute("SELECT cj_id FROM clientejuridico WHERE cj_email = %s;",(form.email.data,))
        #cj = cur.fetchone()
        #dirFiscal
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
            (form.username.data,form.password.data,cj))
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
            (form.username.data,form.password.data,cn))
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
            if user and user.u_password == form.password.data:
                login_user(user,remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(url_for('home'))
            else:
                flash('Contraseña Incorrecta','danger')
        else:
            flash('Usuario no encontrado','danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/nombre_tienda',methods=['GET','POST'])
def nombre_tienda():
    db = Database()
    cur = db.cursor_dict()
    cur.execute("SELECT ti_nombre, ti_tipo, l_nombre, ti_id from tienda, lugar WHERE tienda.l_id=lugar.l_id")
    nombre_tiendas = cur.fetchall()
    db.cerrar()
    nomArray = []
    for nombre in nombre_tiendas:
        nomArray.append(nombre)

    return jsonify({'nombre_tiendas': nomArray})

@app.route("/cliente_home",methods=['GET','POST'])
def cliente_home():
    return render_template('cliente_home.html')

@app.route("/inventario", methods=['GET', 'POST'])
def inventario():
    return render_template('inventario.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
