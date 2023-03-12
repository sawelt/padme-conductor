import atexit

import psycopg2

from padme_conductor.Plugins.DatabasePlugin import DatabasePlugin

class SqlPlugin(DatabasePlugin):
    def __init__(self, db_name, user, password, host, port) -> None:
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = self.connect()
        atexit.register(self.conn.close)

    def connect(self):
        # TODO: maybe move to init with automatic cleanup?
        return psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    def _query(self, query):
        # TODO: the connection needs to be streamlined
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
