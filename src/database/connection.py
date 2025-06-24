import mysql.connector
from src.config import Config

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = mysql.connector.connect(
                **Config.DB_CONFIG,
                auth_plugin='mysql_native_password'
            )
        return cls._instance

    def get_connection(self):
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self._instance = None