#!/usr/bin/env python3

import psycopg2
import config

class DB(object):

        self._host = config.host
        self._user = config.user
        self._password = config.password
        self._port = config.port
        self._conn = psycopg2.connect(host=host, port=port,
                       user=user, passwd=password)
        self._cursor = self._conn.cursor()

    def execute(self, query):
        try:
            self._cursor.execute(query=query)
        except (AttributeError, pymysql.OperationalError):
            self.__reconnect__()
            self._cursor.execute(query=query)

    def fetchone(self):
        return self._cursor.fetchone()

    def commit(self):
        return self._conn.commit()

    def __reconnect__(self):
        self._conn = pymysql.connect(host=self._host, port=self._port, user=self._user, passwd=self._password)
        self._cursor = self._conn.cursor()

