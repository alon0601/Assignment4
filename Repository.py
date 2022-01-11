import os
import sqlite3
import imp
import atexit
import sys

from Persistence import *
from DAO import Dao


class Repository(object):
    def __init__(self, args):
        self._conn = sqlite3.connect(args[4])
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

