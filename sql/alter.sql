ALTER TABLE lugar
  ADD CONSTRAINT fk_lugar_lugar FOREIGN KEY (fk_lugar) references lugar(l_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE clientenatural ADD CONSTRAINT fk_cn_tienda FOREIGN KEY (ti_cod) references tienda(ti_id) ON DELETE CASCADE;
ALTER TABLE clientenatural ADD CONSTRAINT fk_cn_lugar FOREIGN KEY (l_id) references lugar(l_id) ON DELETE CASCADE;
ALTER TABLE clientejuridico ADD CONSTRAINT fk_cj_tienda FOREIGN KEY (ti_cod) references tienda(ti_id) ON DELETE CASCADE;
ALTER TABLE telefono ADD CONSTRAINT fk_cn_tlf FOREIGN KEY (cn_id) references clientenatural(cn_id) ON DELETE CASCADE;
ALTER TABLE telefono ADD CONSTRAINT fk_cj_tlf FOREIGN KEY (cj_id) references clientejuridico(cj_id)ON DELETE CASCADE ;
ALTER TABLE personadecontacto ADD CONSTRAINT fk_cj_pc FOREIGN KEY (cj_id) references clientejuridico(cj_id) ON DELETE CASCADE;
ALTER TABLE usuario ADD CONSTRAINT fk_cn_user FOREIGN KEY (cn_id) references clientenatural(cn_id) ON DELETE CASCADE;
ALTER TABLE usuario ADD CONSTRAINT fk_cj_user FOREIGN KEY (cj_id) references clientejuridico(cj_id) ON DELETE CASCADE;
ALTER TABLE usuario ADD CONSTRAINT fk_e_user FOREIGN KEY (e_id) references empleado(e_id) ON DELETE CASCADE;
ALTER TABLE jur_lug ADD CONSTRAINT fk_cj_jur_lug FOREIGN KEY (cj_id) references clientejuridico(cj_id) ON DELETE CASCADE;
ALTER TABLE jur_lug ADD CONSTRAINT fk_lugar_jur_lug FOREIGN KEY (l_id) references lugar(l_id) ON DELETE CASCADE;
ALTER TABLE fabrica ADD CONSTRAINT fk_fabrica_lugar FOREIGN KEY (l_id) references lugar(l_id) ON DELETE CASCADE;
ALTER TABLE tienda ADD CONSTRAINT fk_tienda_lugar FOREIGN KEY (l_id) references lugar(l_id) ON DELETE CASCADE;
ALTER TABLE usuario ADD CONSTRAINT fk_user_rol FOREIGN KEY (r_id) references rol(r_id) ON DELETE CASCADE;
ALTER TABLE rol_per ADD CONSTRAINT fk_rp_rol FOREIGN KEY (r_id) references rol(r_id) ON DELETE CASCADE;
ALTER TABLE rol_per ADD CONSTRAINT fk_rp_permiso FOREIGN KEY (per_id) references permiso(per_id) ON DELETE CASCADE;
ALTER TABLE asistencia ADD CONSTRAINT fk_a_empleado FOREIGN KEY (e_id) references empleado(e_id) ON DELETE CASCADE;
ALTER TABLE beneficio ADD CONSTRAINT fk_ben_empleado FOREIGN KEY (e_id) references empleado(e_id) ON DELETE CASCADE;
ALTER TABLE horario ADD CONSTRAINT fk_hor_empleado FOREIGN KEY (e_id) references empleado(e_id) ON DELETE CASCADE;
ALTER TABLE diariodulce ADD CONSTRAINT fk_diario_empleado FOREIGN KEY (e_id) references empleado(e_id) ON DELETE CASCADE;
ALTER TABLE pasillo ADD CONSTRAINT fk_pas_tienda FOREIGN KEY (ti_id) references tienda(ti_id) ON DELETE CASCADE;
ALTER TABLE anaquel ADD CONSTRAINT fk_an_pasillo FOREIGN KEY (pas_id) references pasillo(pas_id) ON DELETE CASCADE;
ALTER TABLE inventario ADD CONSTRAINT fk_i_anaquel FOREIGN KEY (an_id) references anaquel(an_id) ON DELETE CASCADE;
ALTER TABLE inventario ADD CONSTRAINT fk_i_producto FOREIGN KEY (p_id) references producto(p_id) ON DELETE CASCADE;
ALTER TABLE inventario ADD CONSTRAINT fk_i_tienda FOREIGN KEY (ti_id) references tienda(ti_id) ON DELETE CASCADE;
ALTER TABLE pro_diario ADD CONSTRAINT fk_pd_dd FOREIGN KEY (dd_id) references diariodulce(dd_id) ON DELETE CASCADE;
ALTER TABLE pro_diario ADD CONSTRAINT fk_pd_producto FOREIGN KEY (p_id) references producto(p_id) ON DELETE CASCADE;
ALTER TABLE tarjetacredito ADD CONSTRAINT fk_tc_cj FOREIGN KEY (cj_id) references clientejuridico(cj_id) ON DELETE CASCADE;
ALTER TABLE tarjetacredito ADD CONSTRAINT fk_tc_cn FOREIGN KEY (cn_id) references clientenatural(cn_id) ON DELETE CASCADE;
ALTER TABLE tarjetadebito ADD CONSTRAINT fk_td_cj FOREIGN KEY (cj_id) references clientejuridico(cj_id) ON DELETE CASCADE;
ALTER TABLE tarjetadebito ADD CONSTRAINT fk_td_cn FOREIGN KEY (cn_id) references clientenatural(cn_id) ON DELETE CASCADE;
ALTER TABLE cheque ADD CONSTRAINT fk_ch_cj FOREIGN KEY (cj_id) references clientejuridico(cj_id) ON DELETE CASCADE;
ALTER TABLE cheque ADD CONSTRAINT fk_ch_cn FOREIGN KEY (cn_id) references clientenatural(cn_id) ON DELETE CASCADE;
ALTER TABLE producto ADD CONSTRAINT fk_p_tp FOREIGN KEY (tp_id) references tipo_producto(tp_id) ON DELETE CASCADE;
ALTER TABLE comprafisica ADD CONSTRAINT fk_cf_inventario FOREIGN KEY (i_id) references inventario(i_id) ON DELETE CASCADE;
ALTER TABLE comprafisica ADD CONSTRAINT fk_cf_cj FOREIGN KEY (cj_id) references clientejuridico(cj_id) ON DELETE CASCADE;
ALTER TABLE comprafisica ADD CONSTRAINT fk_cf_cn FOREIGN KEY (cn_id) references clientenatural(cn_id) ON DELETE CASCADE;
ALTER TABLE compravirtual ADD CONSTRAINT fk_cv_presupuesto FOREIGN KEY (pre_id) references presupuesto(pre_id) ON DELETE CASCADE;
ALTER TABLE compravirtual ADD CONSTRAINT fk_cv_presupuesto2 FOREIGN KEY (pre2_id) references presupuesto(pre_id) ON DELETE CASCADE;
ALTER TABLE compravirtual ADD CONSTRAINT fk_cv_usuario FOREIGN KEY (u_id) references usuario(u_id) ON DELETE CASCADE;
ALTER TABLE compravirtual ADD CONSTRAINT fk_cv_producto FOREIGN KEY (p_id) references producto(p_id) ON DELETE CASCADE;
ALTER TABLE pagovirtual ADD CONSTRAINT fk_pv_comprav FOREIGN KEY (cv_id) references compravirtual(cv_id) ON DELETE CASCADE;
ALTER TABLE pagovirtual ADD CONSTRAINT fk_pv_tarjetac FOREIGN KEY (tc_id) references tarjetacredito(tc_id) ON DELETE CASCADE;
ALTER TABLE pagovirtual ADD CONSTRAINT fk_pv_orden FOREIGN KEY (o_id) references orden(o_id) ON DELETE CASCADE;
ALTER TABLE factura ADD CONSTRAINT fk_f_pagov FOREIGN KEY (pv_id) references pagovirtual(pv_id) ON DELETE CASCADE;
ALTER TABLE carnet ADD CONSTRAINT fk_car_clientej FOREIGN KEY (cj_id) references clientejuridico(cj_id) ON DELETE CASCADE;
ALTER TABLE carnet ADD CONSTRAINT fk_car_clienten FOREIGN KEY (cn_id) references clientenatural(cn_id) ON DELETE CASCADE;
ALTER TABLE carnet ADD CONSTRAINT fk_car_departamento FOREIGN KEY (d_id) references departamento(d_id) ON DELETE CASCADE;
ALTER TABLE orden ADD CONSTRAINT fk_o_inventario FOREIGN KEY (i_id) references inventario(i_id) ON DELETE CASCADE;
ALTER TABLE orden ADD CONSTRAINT fk_o_departamento FOREIGN KEY (d_id) references departamento(d_id) ON DELETE CASCADE;
ALTER TABLE estatus ADD CONSTRAINT fk_es_orden FOREIGN KEY (o_id) references orden(o_id) ON DELETE CASCADE;
ALTER TABLE estatus ADD CONSTRAINT fk_es_pedido FOREIGN KEY (ped_id) references pedido(ped_id) ON DELETE CASCADE;
ALTER TABLE pedido ADD CONSTRAINT fk_ped_pagov FOREIGN KEY (pv_id) references pagovirtual(pv_id) ON DELETE CASCADE;
ALTER TABLE pedido ADD CONSTRAINT fk_ped_clientej FOREIGN KEY (cj_id) references clientejuridico(cj_id) ON DELETE CASCADE;
ALTER TABLE pedido ADD CONSTRAINT fk_ped_clienten FOREIGN KEY (cn_id) references clientenatural(cn_id) ON DELETE CASCADE;
ALTER TABLE pedido ADD CONSTRAINT fk_ped_departamento FOREIGN KEY (d_id) references departamento(d_id) ON DELETE CASCADE;
ALTER TABLE punto ADD CONSTRAINT fk_pu_pagof FOREIGN KEY (pf_id) references pagofisico(pf_id) ON DELETE CASCADE;
ALTER TABLE punto ADD CONSTRAINT fk_pu_carnet FOREIGN KEY (car_id) references carnet(car_id) ON DELETE CASCADE;
ALTER TABLE punto ADD CONSTRAINT fk_pu_historial FOREIGN KEY (h_id) references historial(h_id) ON DELETE CASCADE;
ALTER TABLE reposicion ADD CONSTRAINT fk_re_fabrica FOREIGN KEY (f_id) references fabrica(f_id) ON DELETE CASCADE;
ALTER TABLE reposicion ADD CONSTRAINT fk_re_inventario FOREIGN KEY (i_id) references inventario(i_id) ON DELETE CASCADE;
ALTER TABLE reposicion ADD CONSTRAINT fk_re_orden FOREIGN KEY (o_id) references orden(o_id) ON DELETE CASCADE;
