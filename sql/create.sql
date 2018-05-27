DROP DATABASE IF EXISTS proyecto;
CREATE DATABASE proyecto;
\c proyecto;

CREATE TABLE clientenatural (
  cn_id numeric(8),
  cn_rif numeric(15) NOT NULL UNIQUE,
  cn_email varchar(50) NOT NULL UNIQUE,
  cn_ci numeric(15) NOT NULL UNIQUE,
  cn_nom1 varchar(20) NOT NULL,
  cn_nom2 varchar(20) NOT NULL,
  cn_ap1 varchar(20) NOT NULL,
  cn_ap2 varchar(20) NOT NULL,
  l_id numeric(8) NOT NULL,
  t_cod numeric(8),
  CONSTRAINT pk_cn PRIMARY KEY (cn_id)
);

CREATE TABLE clientejuridico (
  cj_id numeric(8),
  cj_rif numeric(15) NOT NULL UNIQUE,
  cj_email varchar(50) NOT NULL UNIQUE,
  cj_demcom varchar(50) NOT NULL,
  cj_razsoc varchar(50) NOT NULL,
  cj_pagweb varchar(30) NOT NULL,
  cj_capdis numeric(20) NOT NULL,
  l_id numeric(8) NOT NULL,
  l_id2 numeric(8) NOT NULL,
  t_cod numeric(8),
  CONSTRAINT pk_cj PRIMARY KEY (cj_id)
);

CREATE TABLE telefono (
  t_id numeric(8),
  t_num numeric(10) NOT NULL,
  cj_id numeric(8),
  cn_id numeric(8),
  CONSTRAINT pk_t PRIMARY KEY (t_id)
);

CREATE TABLE personadecontacto (
  pc_id numeric(8),
  pc_nombre varchar(20) NOT NULL,
  pc_apellido varchar(20) NOT NULL,
  cj_id numeric(8) NOT NULL,
  CONSTRAINT pk_pc PRIMARY KEY (pc_id)
);
