"""
This file contains a connection class that creates a usable connection and cursor object
"""

import sqlite3

class DatabaseConnection:
    def __init__(self, host):
        self.connection = None
        self.host=host

    def __enter__(self):
        self.connection = sqlite3.connect(self.host)
        self.cursor = self.connection.cursor()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()


