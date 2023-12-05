from abc import abstractmethod, ABCMeta
import helpers


class FileHandler(metaclass=ABCMeta):

    @abstractmethod
    def obj_to_str(self):
        pass

    @abstractmethod
    def get_table(self):
        pass

    @abstractmethod
    def get_fieldnames(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

    def load(self=None, table=None, condition=None):
        if condition:
            query = f'SELECT * FROM {table} WHERE {condition};'
        else:
            query = f'SELECT * FROM {table};'

        data_output = helpers.query_db(query, result=True)

        return data_output

    def check_id(self=None, table=None, object_id=None):
        if self:
            object_id = self.get_id()
            table = self.get_table()

        query = f"SELECT * FROM {table} WHERE id = {object_id};"
        data_output = helpers.query_db(query, result=True)

        return data_output

    def delete(self):
        object_id = self.get_id()
        table = self.get_table()

        if table == 'person':
            open_orders = helpers.get_orders(self, future_orders=True)
            assert len(open_orders) == 0, "Unable to delete client. " \
                                          "This client has open orders related to it."
        query = f"DELETE FROM {table} WHERE id = {object_id};"

        if table == 'cars':
            open_orders = helpers.get_orders(self, future_orders=True)
            assert len(open_orders) == 0, "Unable to delete car. " \
                                          "This car has open orders related to it."
        query = f"DELETE FROM {table} WHERE id = {object_id};"

        helpers.query_db(query)

    def edit(self, set_clauses: list):
        object_id = self.get_id()
        table = self.get_table()
        clauses_str = ""

        for i in range(len(set_clauses)):
            if (i + 1) == len(set_clauses):
                clauses_str += f"{set_clauses[i]}"
            else:
                clauses_str += f"{set_clauses[i]}, "

        query = f"UPDATE {table} SET {clauses_str} WHERE id = '{object_id}';"
        helpers.query_db(query)

        return True

    def save(self):
        table = self.get_table()
        columns = self.get_fieldnames()
        values = self.obj_to_str()

        query = f"INSERT INTO {table} ({columns}) VALUES ({values});"

        helpers.query_db(query)

        return True
