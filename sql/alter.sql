ALTER TABLE lugar
  ADD CONSTRAINT fk_lugar_lugar FOREIGN KEY (fk_lugar) references lugar(l_id) ON DELETE CASCADE ON UPDATE CASCADE;
