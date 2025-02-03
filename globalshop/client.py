from pyodbc import Cursor, Connection
import pyodbc

from baseintegration.datamigration import logger


class GlobalShopClient:
    _instance = None

    def __new__(cls, **kwargs):
        """
        Create or return the GlobalShopClient Singleton.
        """
        if GlobalShopClient._instance is None:
            logger.info("GlobalShopInstance is none, setting")
            GlobalShopClient._instance = object.__new__(cls)
        instance = GlobalShopClient._instance

        logger.info("Get secrets")
        instance.server_name = kwargs.get('server_name', None)
        logger.info('new func servername:' + instance.server_name)
        instance.database = kwargs.get('database', None)
        instance.username = kwargs.get('username', None)
        instance.password = kwargs.get('password', None)

        return instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __init__(self, server_name: str, database: str, username, password):
        logger.info("init function server_name: " + server_name)
        self.server_name = server_name
        self.database = database
        self.username = username
        self.password = password
        self._sql_cache = []

    def connect(self) -> Connection:
        """
        Establish a connection to return a pyodbc Connection object. Assumes
        the caller will close the connection. Recommended usage is: with
        client.connect() as conn: conn.cursor
        """
        logger.info("Connect to server name: " + self.server_name)
        conn = pyodbc.connect(
            f'Driver={{Pervasive ODBC Interface}};'
            f'ServerName={self.server_name};dbq={self.database};'
            f'UID={self.username};PWD={self.password}')
        return conn

    def cursor(self) -> Cursor:
        """
        Establish a connection to return a pyodbc cursor object. Assumes the
        caller will close the cursor. Recommended usage is: with
        client.cursor() as cur: cur.execute()
        """
        return self.connect().cursor()

    def cache(self, sql_cmd: str) -> None:
        """
        Some sql commands need to be written out in a batch sequence, BOM &
        Router being the two main examples. This caching allows the a sql
        command to be cached until the caller is ready to execute all of
        them in sequence. It is the responsibility of the caller to run
        ,execute_cache() and then either
        """
        self._sql_cache.append(sql_cmd)

    def execute_cache(self, commit=False) -> Cursor:
        """
        Execute the sql commands in the cache in order. This does NOT handle
        ODBC errors. If the cache is corrupt then the caller will need to
        rebuild it correctly.
        :param commit: set to True if you want to do a cursor.commit() to
        commit the transaction to the DB after the last sql command in the
        cache is executed.
        :return cursor: Return the cursor used to execute the commands. If
        commit param is False, the caller can call .commit() on the cursor
        themselves.
        """
        cursor = self.cursor()
        for cmd in self._sql_cache:
            cursor.execute(cmd)

        if commit:
            cursor.commit()

        # Clear the cache now that we successfully wrote it out
        self._sql_cache.clear()

        return cursor
