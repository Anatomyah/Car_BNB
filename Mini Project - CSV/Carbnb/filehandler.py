import csv
from abc import abstractmethod, ABCMeta
import helpers
from config import *


class FileHandler(metaclass=ABCMeta):

    @abstractmethod
    def obj_to_str(self):
        pass

    @abstractmethod
    def obj_to_dict(self):
        pass

    @abstractmethod
    def get_file_path(self, fieldnames=False):
        pass

    @abstractmethod
    def get_id(self):
        pass

    def load(self=None, file_path=None):
        if self:
            file_path = self.get_file_path()
        else:
            file_path = file_path

        with open(file=file_path, mode='r') as fh:
            reader = csv.DictReader(fh)
            rows = [x for x in reader]

            return rows

    def check_id(self=None, object_id=None, check_rent=None):
        res = None

        if object_id or check_rent:
            file_path = RENT_PATH
        else:
            file_path = self.get_file_path()
            object_id = self.get_id()

        with open(file=file_path, mode='r') as fh:
            reader = csv.DictReader(fh)
            rows = [x for x in reader]

            for row in rows:
                if file_path == CARS_PATH:
                    if row['Serial'] == str(object_id):
                        new_rows = [x for x in rows if x['Serial'] != str(object_id)]
                        res = {"rows": new_rows, "reader": reader}
                        break

                else:
                    if row['ID'] == str(object_id):
                        new_rows = [x for x in rows if x['ID'] != str(object_id)]
                        res = {"rows": new_rows, "reader": reader}
                        break

        return res

    def delete(self=None, object_d: dict = None):
        if object_d:
            file_path = RENT_PATH
            reader_d = FileHandler.check_id(object_id=object_d['ID'])
        else:
            file_path = self.get_file_path()

            if file_path == PERSON_PATH or CARS_PATH:
                open_orders = helpers.get_orders(self, future_orders=True)
                i
                assert len(open_orders) == 0, "Unable to delete client. " \
                                             "The Client you are trying to delete has open orders in our system."

            reader_d = self.check_id()

        if reader_d:
            with open(file=file_path, mode='w', newline='') as new_file:
                writer = csv.DictWriter(new_file, fieldnames=reader_d['reader'].fieldnames)

                writer.writeheader()
                writer.writerows(reader_d['rows'])

    def save(self=None, object_d: dict = None):
        if self:
            file_path = self.get_file_path(fieldnames=True)
            reader_d = self.check_id()

        else:
            file_path = RENT_PATH
            reader_d = FileHandler.check_id(object_id=object_d['ID'])
            reader_d['rows'].append(object_d)
            sorted_rows = sorted(reader_d['rows'], key=lambda d: d['ID'])
            reader_d['rows'] = sorted_rows

        if reader_d:
            if self:
                reader_d['rows'].append(self.obj_to_dict())
            with open(file=file_path['file_path'], mode='w', newline='') as new_file:
                writer = csv.DictWriter(new_file, fieldnames=reader_d['reader'].fieldnames)

                writer.writeheader()
                writer.writerows(reader_d['rows'])

        with open(file=file_path['file_path'], mode='a', newline='') as fh:
            writer = csv.DictWriter(fh, fieldnames=file_path['fieldnames'])
            row = self.obj_to_dict()
            writer.writerow(row)
