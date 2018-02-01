import psycopg2 as pg
from config import Config

class DB():
    def __init__(self):
        self._connection_parameters = {
        'host': Config.get_variable('db', 'host'),
        'database': Config.get_variable('db', 'database'),
        'user': Config.get_variable('db', 'user'),
        'password': Config.get_variable('db', 'password'),
        'port':  int(Config.get_variable('db', 'port')) }
        self._conn = pg.connect(**self._connection_parameters)
        self._cursor = self._conn.cursor()

    def execute(self, query):
        try:
            self._cursor.execute(query=query)
        except (AttributeError, pg.OperationalError):
            self.__reconnect__()
            self._cursor.execute(query=query)

    def fetchone(self):
        return self._cursor.fetchone()

    def commit(self):
        return self._conn.commit()

    def __reconnect__(self):
        self._conn = pg.connect(**self._connection_parameters)
        self._cursor = self._conn.cursor()
