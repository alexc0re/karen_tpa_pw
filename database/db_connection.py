import psycopg2

class DataBaseConnection:
    def __init__(self, host, port, user, password, dbname):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )

    def execute(self, query, *args):
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            self.connection.commit()


    def fetchone(self, query, *args):
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            return cursor.fetchone()

    def close(self):
        self.connection.close()
