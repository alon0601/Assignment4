
import inspect


def orm(cursor, dto_type):

    # the following line retrieve the argument names of the constructor
    args = inspect.getargspec(dto_type.__init__).args

    # the first argument of the constructor will be 'self', it does not correspond
    # to any database field, so we can ignore it.
    args = args[1:]

    # gets the names of the columns returned in the cursor
    col_names = [column[0] for column in cursor.description]

    # map them into the position of the corresponding constructor argument
    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]


def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)


class Dao(object):
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type

        # dto_type is a class, its __name__ field contains a string representing the name of the class.
        self._table_name = dto_type.__name__.lower() + 's'

    def order_by(self, order_param):
        stmt = 'SELECT * FROM {} ORDER BY {}'.format(self._table_name, order_param)
        c = self._conn.cursor()
        c.execute(stmt)

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)

        column_names = ','.join(ins_dict.keys())
        params = ins_dict.values()
        qmarks = ','.join(['?'] * len(ins_dict))

        stmt = 'INSERT INTO {} ({}) VALUES ({})' \
            .format(self._table_name, column_names, qmarks)

        self._conn.execute(stmt, list(params))

    def update(self, cond, values_set):
        cond_keys = cond.keys()
        cond_values = cond.values()

        key_set = values_set.keys()
        values = values_set.values()

        state = 'UPDATE {} SET {} WHERE {}'.format(self._table_name,
                                                   ', '.join(key + '=?' for key in key_set),
                                                   ' AND '.join(cond_key + '=?' for cond_key in cond_keys))

        self._conn.execute(state, list(values) + list(cond_values))

    def delete(self, cond):
        cond_keys = cond.keys()
        cond_values = cond.values()

        state = 'DELETE FROM {} WHERE {}'.format(self._table_name,
                                                 ' AND '.join(cond_key + '=?' for cond_key in cond_keys))

        self._conn.execute(state, list(cond_values))

    def find_all(self):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {}'.format(self._table_name))
        return orm(c, self._dto_type)

    def find(self, **keyvals):
        column_names = keyvals.keys()
        params = keyvals.values()

        stmt = 'SELECT * FROM {} WHERE {}' \
            .format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))

        c = self._conn.cursor()
        c.execute(stmt, list(params))
        return orm(c, self._dto_type)

    def find_order(self, order_by, **keyvals):
        column_names = keyvals.keys()
        params = keyvals.values()

        stmt = 'SELECT * FROM {} WHERE {} ORDER BY {}' \
            .format(self._table_name, ' AND '.join([col + '=?' for col in column_names]), order_by)

        c = self._conn.cursor()
        c.execute(stmt, list(params))
        return orm(c, self._dto_type)