DROP DATABASE IF EXISTS proyecto;
CREATE DATABASE proyecto;
\c proyecto;

CREATE TABLE clientenatural (
  cn_id SERIAL,
  cn_rif varchar(15) NOT NULL UNIQUE,
  cn_email varchar(50) NOT NULL UNIQUE,
  cn_ci numeric(15) NOT NULL UNIQUE,
  cn_nom1 varchar(20) NOT NULL,
  cn_nom2 varchar(20) NOT NULL,
  cn_ap1 varchar(20) NOT NULL,
  cn_ap2 varchar(20) NOT NULL,
  l_id numeric(10) NOT NULL,
  t_cod numeric(8),
  CONSTRAINT pk_clienten PRIMARY KEY (cn_id)
);

CREATE TABLE clientejuridico (
  cj_id SERIAL,
  cj_rif varchar(15) NOT NULL UNIQUE,
  cj_email varchar(50) NOT NULL UNIQUE,
  cj_demcom varchar(50) NOT NULL,
  cj_razsoc varchar(50) NOT NULL,
  cj_pagweb varchar(30) NOT NULL,
  cj_capdis numeric(20) NOT NULL,
  t_cod numeric(8),
  CONSTRAINT pk_clientej PRIMARY KEY (cj_id)
);

CREATE TABLE telefono (
  t_id SERIAL,
  t_num numeric(10) NOT NULL,
  cj_id integer,
  cn_id integer,
  CONSTRAINT pk_telefono PRIMARY KEY (t_id)
);

CREATE TABLE personadecontacto (
  pc_id SERIAL,
  pc_nombre varchar(20) NOT NULL,
  pc_apellido varchar(20) NOT NULL,
  cj_id integer NOT NULL,
  CONSTRAINT pk_percontacto PRIMARY KEY (pc_id)
);

CREATE TABLE usuario (
  u_id SERIAL,
  u_username varchar(20) NOT NULL UNIQUE,
  u_password varchar(60) NOT NULL,
  cj_id integer,
  cn_id integer,
  e_id integer,
  CONSTRAINT pk_usuario PRIMARY KEY (u_id)
);

CREATE TABLE empleado (
  e_id SERIAL,
  e_nombre varchar(20) NOT NULL,
  e_apellido varchar(20) NOT NULL,
  e_ci numeric(15) NOT NULL UNIQUE,
  e_salario numeric(15) NOT NULL,
  CONSTRAINT pk_empleado PRIMARY KEY (e_id)
);

CREATE TABLE permiso(
  p_id numeric(8),
  p_tipo varchar(15) NOT NULL,
  CONSTRAINT pk_permiso PRIMARY KEY (p_id)
);

CREATE TABLE lugar (
  l_id numeric(10),
  l_tipo char(1) NOT NULL,
  l_nombre varchar(40) NOT NULL,
  fk_lugar numeric(10),
  CONSTRAINT pk_lugar PRIMARY KEY (l_id),
  CONSTRAINT check_tipo CHECK(l_tipo in ('M','P','E'))
);

CREATE TABLE jur_lug(
  jl_id SERIAL,
  l_id numeric(10) NOT NULL,
  cj_id integer NOT NULL,
  jl_tipo varchar(10) NOT NULL,
  CONSTRAINT pk_lugar_clientej PRIMARY KEY (jl_id),
  CONSTRAINT check_tipodir CHECK(jl_tipo in ('fisica','fiscal'))
);

CREATE TABLE departamento (
  d_id numeric(8),
  d_nombre varchar(20) NOT NULL,
  CONSTRAINT pk_departamento PRIMARY KEY (d_id)
);

CREATE TABLE fabrica (
  f_id numeric(8),
  f_nombre varchar(20) NOT NULL,
  l_id numeric(10) NOT NULL,
  CONSTRAINT pk_fabrica PRIMARY KEY (f_id)
);

CREATE TABLE tienda (
  ti_id numeric(8),
  ti_tipo varchar(20) NOT NULL,
  ti_nombre varchar(40) NOT NULL,
  l_id numeric(10) NOT NULL,
  CONSTRAINT pk_tienda PRIMARY KEY (ti_id)
);
