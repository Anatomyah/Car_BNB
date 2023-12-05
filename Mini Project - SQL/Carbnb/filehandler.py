from abc import abstractmethod, ABCMeta
import helpers


class FileHandler(metaclass=ABCMeta):
    """
    An abstract base class representing a file handler.

    This class provides an abstract interface for file handling operations
    including loading, checking IDs, deleting, editing, and saving data to a database.
    Subclasses are expected to implement the abstract methods defined here.

    Methods:
        obj_to_str: Abstract method to convert object to string format for database.
        get_table: Abstract method to get the database table name.
        get_fieldnames: Abstract method to get fieldnames for database operations.
        get_id: Abstract method to get the object's ID.
        load: Loads data from the database.
        check_id: Checks if an ID exists in the database.
        delete: Deletes an object from the database.
        edit: Edits an object in the database.
        save: Saves an object to the database.
    """

    @abstractmethod
    def obj_to_str(self):
        """
        Converts the object to a string format suitable for database storage.
        This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_table(self):
        """
        Retrieves the database table name associated with the object.
        This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_fieldnames(self):
        """
        Retrieves the field names for database operations for the object.
        This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_id(self):
        """
        Retrieves the ID of the object.
        This method must be implemented by subclasses.
        """
        pass

    def load(self=None, table=None, condition=None):
        """
        Loads data from a specified table in the database based on a condition.

        Args:
            table (str): The name of the table to load data from.
            condition (str, optional): The condition for data selection.

        Returns:
            list: A list of data rows that match the condition from the specified table.
        """
        if condition:
            query = f'SELECT * FROM {table} WHERE {condition};'
        else:
            query = f'SELECT * FROM {table};'

        data_output = helpers.query_db(query, result=True)

        return data_output

    def check_id(self=None, table=None, object_id=None):
        """
        Checks if an ID exists in the specified table in the database.

        Args:
            table (str): The name of the table to check the ID in.
            object_id (int): The ID to check in the table.

        Returns:
            list: The data row corresponding to the ID, if it exists.
        """
        if self:
            object_id = self.get_id()
            table = self.get_table()

        query = f"SELECT * FROM {table} WHERE id = {object_id};"
        data_output = helpers.query_db(query, result=True)

        return data_output

    def delete(self):
        """
        Deletes the object from its respective table in the database.

        Raises:
            AssertionError: If the object cannot be deleted due to related open orders.
        """
        object_id = self.get_id()
        table = self.get_table()

        # Additional logic for specific table conditions
        if table == 'person':
            open_orders = helpers.get_orders(self, future_orders=True)
            assert len(open_orders) == 0, "Unable to delete client. This client has open orders related to it."
        if table == 'cars':
            open_orders = helpers.get_orders(self, future_orders=True)
            assert len(open_orders) == 0, "Unable to delete car. This car has open orders related to it."

        query = f"DELETE FROM {table} WHERE id = {object_id};"
        helpers.query_db(query)

    def edit(self, set_clauses: list):
        """
        Edits the object's attributes in the database.

        Args:
            set_clauses (list): A list of strings specifying the attributes to be updated.

        Returns:
            bool: True if the operation is successful.
        """
        object_id = self.get_id()
        table = self.get_table()
        clauses_str = ", ".join(set_clauses)

        query = f"UPDATE {table} SET {clauses_str} WHERE id = '{object_id}';"
        helpers.query_db(query)

        return True

    def save(self):
        """
        Saves the object to its respective table in the database.

        Returns:
            bool: True if the operation is successful.
        """
        table = self.get_table()
        columns = self.get_fieldnames()
        values = self.obj_to_str()

        query = f"INSERT INTO {table} ({columns}) VALUES ({values});"

        helpers.query_db(query)

        return True
