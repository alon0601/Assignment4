import sqlite3
import atexit


class Hat(object):
    def __init__(self, id, topping, supplier, quantity):
        self.id = id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity


class Supplier(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Order(object):
    def __init__(self, id, location, hat):
        self.id = id
        self.location = location
        self.hat = hat



