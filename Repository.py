import os
import sqlite3
import imp
import atexit

from Persistence import *
from DAO import Dao


class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
#        self._conn.text_factory = bytes
        self.hats = Dao(Hat, self._conn)
        self.suppliers = Dao(Supplier, self._conn)
        self.orders = Dao(Order, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
                CREATE TABLE hats (
                    id INT PRIMARY KEY,
                    topping STRING NOT NULL,
                    supplier INT REFERENCES Suppliers(id), 
                    quantity INT NOT NULL
                );

                CREATE TABLE suppliers (
                    id INT PRIMARY KEY,
                    name STRING NOT NULL
                );

                CREATE TABLE orders (
                    id INT PRIMARY KEY,
                    location STRING NOT NULL,
                    hat INT NOT NULL REFERENCES hats(id)
                );
            """)


# singleton
repo = Repository()
atexit.register(repo._close)