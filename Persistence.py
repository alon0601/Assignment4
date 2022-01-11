import sqlite3
import atexit


class Hat(object):
    def __init__(self, id, topping, supplier_id, quantity):
        self.id = id
        self.topping = topping
        self.supplier_id = supplier_id
        self.quantity = quantity


class Supplier(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Order(object):
    def __init__(self, id, location, hat_id):
        self.id = id
        self.location = location
        self.hats_id = hat_id



