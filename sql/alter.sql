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
