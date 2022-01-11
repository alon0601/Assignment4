# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from Repository import *
import sqlite3
from Repository import *
from DAO import *


def read_file(path):
    input_filename = path
    with open(input_filename) as input_file:
        return [line.split(',') for line in input_file]


def main(args):
    repo = Repository(args)
    atexit.register(repo._close)
    repo.create_tables()

    raws = read_file(args[1])

    n_toppings = int(raws[0][0])
    n_suppliers = int(raws[0][1])

    for i in range(n_toppings):
        hat = Hat(raws[i + 1][0], raws[i + 1][1], raws[i + 1][2], raws[i + 1][3].replace('\n', ''))
        repo.hats.insert(hat)

    for j in range(n_suppliers):
        supplier = Supplier(raws[j + n_toppings + 1][0], raws[j + n_toppings + 1][1].replace('\n', ''))
        repo.suppliers.insert(supplier)

    repo.hats.order_by('supplier')
    orders = read_file(args[2])
    with open(args[3], 'w') as f:
        order_id = 1
        for order in orders:
            output = order_pizza(order, order_id, repo)
            order_id += 1
            f.write(output)
            f.write('\n')


def order_pizza(order_com, id, repo):
    hat_id = repo.hats.find_order("supplier", topping=order_com[1].replace('\n', ''))
    new_order = Order(id, order_com[0], hat_id[0].id)
    repo.orders.insert(new_order)

    supplier = repo.suppliers.find(id=hat_id[0].supplier)

    output = str(hat_id[0].topping) + "," + str(supplier[0].name) + "," + str(order_com[0])
    quantity = hat_id[0].quantity - 1
    if quantity == 0:
        repo.hats.delete({'id': new_order.hat})
    else:
        repo.hats.update({'id': hat_id[0].id}, {'quantity': quantity})
    return output


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
