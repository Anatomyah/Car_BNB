from datetime import datetime
from config import RENT_ID_COUNTER, RENT_FIELDNAMES
from filehandler import FileHandler
from helpers import get_by_id, is_available
from car import Car
from person import Person


class Rent(FileHandler):
    __ID_COUNTER = 0

    def __init__(self, pickup_time, return_time, client, car, id_=0, override=False):
        if override:
            self.id = id_
        else:
            Rent.get_id_counter()
            self.id = Rent.__ID_COUNTER
            Rent.__ID_COUNTER += 1
            Rent.save_id_counter()

        self.car = car
        self.pickup_time = pickup_time
        self.return_time = return_time
        self.client = client

    @staticmethod
    def get_id_counter():
        with open(RENT_ID_COUNTER, 'r') as fh:
            Rent.__ID_COUNTER = int(fh.read())

    @staticmethod
    def save_id_counter():
        with open(RENT_ID_COUNTER, 'w') as fh:
            fh.write(str(Rent.__ID_COUNTER))

    def obj_to_str(self):
        return f"'{self.id}', '{self._pickup_time}', '{self._return_time}', '{self._client.id}', '{self._car.id}'"

    def get_table(self):
        return 'rent'

    def show(self):
        print(f"\n*** Order Details ***\n"
              f"Order ID: {self.id}\n"
              f"Pickup Time: {self._pickup_time}\n"
              f"Return Time: {self._return_time}\n"
              f"Client: {self._client.id}\n"
              f"Car: {self._car.id}")

    def get_fieldnames(self, fieldnames=False):
        return RENT_FIELDNAMES

    def get_id(self):
        return self.id

    @property
    def pickup_time(self):
        return self._pickup_time

    @pickup_time.setter
    def pickup_time(self, new_val):
        assert not any(x.isalpha() for x in new_val), f"Invalid date. " \
                                                      f"Date ust be in the YYYY-MM-DD format " \
                                                      f"cannot contain letters or be under 6 " \
                                                      f"characters"

        date_object = datetime.strptime(new_val, '%Y-%m-%d %H:%M:%S')

        self._pickup_time = date_object

    @property
    def return_time(self):
        return self._return_time

    @return_time.setter
    def return_time(self, new_val):
        assert not any(x.isalpha() for x in new_val), f"Invalid date. " \
                                                      f"Date ust be in the YYYY-MM-DD format " \
                                                      f"cannot contain letters or be under 6 " \
                                                      f"characters"

        date_object = datetime.strptime(new_val, '%Y-%m-%d %H:%M:%S')

        self._return_time = date_object
        assert is_available(self.car.id, self._pickup_time, self._return_time) is False, "Chosen vehicle is already " \
                                                                                      "booked within the desired time" \
                                                                                      " frame"

    @property
    def car(self):
        return self._car

    @car.setter
    def car(self, new_val):
        assert len(new_val) > 6 and not any(x.isalpha() for x in new_val), f"Invalid ID number. " \
                                                                           f"Number cannot contain letters or be " \
                                                                           f"under 6 characters"

        row = get_by_id(new_val, table='cars')[0]
        assert row is not None, f"This car Serial Number does not exists in our database"

        self._car = Car(row[0], row[1], row[2], row[3],
                        row[4], row[5], row[6], row[7])

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, new_val):
        assert len(new_val) > 6 and not any(x.isalpha() for x in new_val), f"Invalid ID number. " \
                                                                           f"Number cannot contain letters or be " \
                                                                           f"under 6 characters"
        row = get_by_id(new_val, table='person')[0]
        assert row is not None, f"This client ID does not exists in our database"

        self._client = Person(row[0], row[1], row[2], row[3], row[4],
                              row[5])

    def rent_cost(self):
        days = self._return_time - self._pickup_time

        return days.days * self.car.day_cost

    @classmethod
    def load_from_db(cls):
        order_data = cls.load(table='rent')

        objects = []
        for row in order_data:
            objects.append(cls(pickup_time=row[1],
                               return_time=row[2],
                               client=row[3],
                               car=row[4],
                               id_=row[0], override=True))

        return objects
