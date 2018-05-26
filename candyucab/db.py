import psycopg2,psycopg2.extras

class Database (object):
    def __init__(self):
        self.connectionString = 'dbname=Aprendiendo user=postgres password=angel123 host=localhost'
        print (self.connectionString)
        try:
            self.conn = psycopg2.connect(self.connectionString)
        except:
            print("Can't connect to database")

    def cursor_dict(self):
        return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def cursor(self):
        return self.conn.cursor()

    def actualizar(self):
        self.conn.commit()

    def retroceder(self):
        self.conn.rollback()