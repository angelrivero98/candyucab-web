import psycopg2,psycopg2.extras

class Database ():
    def cursor_dict(self):
        connectionString = 'dbname=Aprendiendo user=postgres password=angel123 host=localhost'
        print (connectionString)
        try:
            self.conn = psycopg2.connect(connectionString)
        except:
            print("Can't connect to database")

        return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def cursor(self):
        connectionString = 'dbname=Aprendiendo user=postgres password=angel123 host=localhost'
        print (connectionString)
        try:
            self.conn = psycopg2.connect(connectionString)
        except:
            print("Can't connect to database")
        return self.conn.cursor()

    def actualizar(self):
        self.conn.commit()

    def retroceder(self):
        self.conn.rollback()
