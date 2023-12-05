import csv
from abc import abstractmethod, ABCMeta
import helpers
from config import *


class FileHandler(metaclass=ABCMeta):
    """
    Abstract base class that defines the template for handling file operations.
    Classes that inherit from FileHandler must implement specific methods to
    interact with CSV files for different data models.

    The class provides generic methods for loading, saving, deleting, and checking
    the existence of data in CSV files, which are overridden in child classes as needed.
    """

    @abstractmethod
    def obj_to_str(self):
        """
        Abstract method that should be implemented in child classes.
        Converts an object to a string representation.
        """
        pass

    @abstractmethod
    def obj_to_dict(self):
        """
        Abstract method that should be implemented in child classes.
        Converts an object to a dictionary representation.
        """
        pass

    @abstractmethod
    def get_file_path(self, fieldnames=False):
        """
        Abstract method that should be implemented in child classes.
        Returns the file path for the CSV file associated with the object.
        """
        pass

    @abstractmethod
    def get_id(self):
        """
        Abstract method that should be implemented in child classes.
        Returns the unique identifier of the object.
        """
        pass

    def load(self=None, file_path=None):
        """
        Load data from a CSV file.

        Parameters:
            self (optional): Instance of the class calling the method.
            file_path (str, optional): Path of the CSV file to load.

        Returns:
            list of dict: Rows from the CSV file as dictionaries.
        """
        if self:
            file_path = self.get_file_path()
        else:
            file_path = file_path

        with open(file=file_path, mode='r') as fh:
            reader = csv.DictReader(fh)
            rows = [x for x in reader]

            return rows

    def check_id(self=None, object_id=None, check_rent=None):
        """
             Check if an ID exists in the corresponding CSV file.

             Parameters:
                 self (optional): Instance of the class calling the method.
                 object_id (optional): ID to check in the CSV file.
                 check_rent (bool, optional): Flag to check in the rent file.

             Returns:
                 dict or None: Dictionary containing the rows and reader if the ID is found; None otherwise.
             """
        res = None

        # Determine the appropriate file path based on the context (rental or other).
        if object_id or check_rent:
            file_path = RENT_PATH
        else:
            file_path = self.get_file_path()
            object_id = self.get_id()

        # Open the file and read the data to check for the existence of the given ID.
        with open(file=file_path, mode='r') as fh:
            reader = csv.DictReader(fh)
            rows = [x for x in reader]

            # Loop through the rows to find a matching ID.
            for row in rows:
                # Special handling for cars, checking 'Serial' instead of 'ID'.
                if file_path == CARS_PATH:
                    if row['Serial'] == str(object_id):
                        new_rows = [x for x in rows if x['Serial'] != str(object_id)]
                        res = {"rows": new_rows, "reader": reader}
                        break
                # Standard handling for other types of objects.
                else:
                    if row['ID'] == str(object_id):
                        new_rows = [x for x in rows if x['ID'] != str(object_id)]
                        res = {"rows": new_rows, "reader": reader}
                        break

        return res

    def delete(self=None, object_d: dict = None):
        """
                Delete an object from its corresponding CSV file.

                Parameters:
                    self (optional): Instance of the class calling the method.
                    object_d (dict, optional): Dictionary representing the object to be deleted.
                """
        # Determine the context and prepare for deletion.
        if object_d:
            file_path = RENT_PATH
            reader_d = FileHandler.check_id(object_id=object_d['ID'])
        else:
            file_path = self.get_file_path()

            # Special handling for clients and cars, checking for open orders.
            if file_path == PERSON_PATH or CARS_PATH:
                open_orders = helpers.get_orders(self, future_orders=True)
                assert len(open_orders) == 0, "Unable to delete client."

            reader_d = self.check_id()

        # If the object to be deleted is found, proceed with deletion.
        if reader_d:
            with open(file=file_path, mode='w', newline='') as new_file:
                writer = csv.DictWriter(new_file, fieldnames=reader_d['reader'].fieldnames)
                writer.writeheader()
                writer.writerows(reader_d['rows'])

    def save(self=None, object_d: dict = None):
        """
               Save an object to its corresponding CSV file.

               Parameters:
                   self (optional): Instance of the class calling the method.
                   object_d (dict, optional): Dictionary representing the object to be saved.
               """
        # Determine the context and prepare for saving.
        if self:
            file_path = self.get_file_path(fieldnames=True)
            reader_d = self.check_id()
        else:
            file_path = RENT_PATH
            reader_d = FileHandler.check_id(object_id=object_d['ID'])
            reader_d['rows'].append(object_d)
            sorted_rows = sorted(reader_d['rows'], key=lambda d: d['ID'])
            reader_d['rows'] = sorted_rows

        # If the object is not present in the file, append it.
        if reader_d:
            if self:
                reader_d['rows'].append(self.obj_to_dict())
            with open(file=file_path['file_path'], mode='w', newline='') as new_file:
                writer = csv.DictWriter(new_file, fieldnames=reader_d['reader'].fieldnames)
                writer.writeheader()
                writer.writerows(reader_d['rows'])

        # Additional code to append the object to the file.
        with open(file=file_path['file_path'], mode='a', newline='') as fh:
            writer = csv.DictWriter(fh, fieldnames=file_path['fieldnames'])
            row = self.obj_to_dict()
            writer.writerow(row)
