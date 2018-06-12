from faker import Faker
import random
fake = Faker('es_ES')

#hs.write("\n")

myfile = open("clientes.txt","a")
for _ in range(41):
    #clientes naturales
    insert_n = "INSERT INTO clientenatural (cn_rif, cn_email,cn_nom1,cn_nom2,cn_ap1,cn_ap2,l_id,cn_ci,ti_cod) VALUES ('{}','{}','{}','{}','{}','{}',{},{},{})"
    rif1 = "V-{}-{}"
    myfile.write(insert_n.format(rif1.format(str(random.randint(1000000,99999999)),str(random.randint(0,9))),
                    fake.simple_profile(sex=None)['mail'],fake.first_name(),fake.first_name(),fake.last_name(),
                    fake.last_name(),str(random.randint(463,1600)),str(random.randint(1000000,25999999)),str(_+1)))
    myfile.write("\n")
    myfile.write("\n")

    myfile.write(insert_n.format(rif1.format(str(random.randint(1000000,99999999)),random.randint(0,9)),
                    fake.simple_profile(sex=None)['mail'],fake.first_name(),fake.first_name(),fake.last_name(),
                    fake.last_name(),str(random.randint(463,1600)),str(random.randint(1000000,25999999)),str(_+1)))
    myfile.write("\n")
    myfile.write("\n")
    #clientes Juridicos


for _ in range(41):
    insert_j = "INSERT INTO clientejuridico (cj_rif, cj_email,cj_razsoc,cj_demcom,cj_pagweb,cj_capdis,ti_cod) VALUES ('{}','{}','{}','{}','{}',{},{})"
    rif2 = "J-{}-{}"
    profile = fake.profile()
    myfile.write(insert_j.format(rif2.format(str(random.randint(1000000,99999999)),str(random.randint(0,9))),
                    profile['mail'],profile['company'],fake.company_suffix()+fake.company(),profile['website'][0],
                    str(random.randint(100000,1000000)),str(_+1)))
    myfile.write("\n")
    myfile.write("\n")
    profile1 = fake.profile()
    myfile.write(insert_j.format(rif2.format(str(random.randint(1000000,99999999)),str(random.randint(0,9))),
                    profile1['mail'],profile1['company'],fake.company_suffix()+fake.company(),profile1['website'][0],
                    str(random.randint(100000,1000000)),str(_+1)))
    myfile.write("\n")
    myfile.write("\n")


myfile.close()
