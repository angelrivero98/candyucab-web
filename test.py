import pyexcel as p

records = p.iget_records(file_name="asistencia.xlsx")
for record in records:
    print(isinstance(record['CEDULA'],str))
