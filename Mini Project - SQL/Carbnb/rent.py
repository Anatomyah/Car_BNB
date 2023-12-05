from datetime import datetime
from config import RENT_ID_COUNTER, RENT_FIELDNAMES
from filehandler import FileHandler
from helpers import get_by_id, is_available
from car import Car
from person import Person


class Rent(FileHandler):
    """
    A subclass of FileHandler that represents a rental transaction.

    This class manages rental details and provides methods for displaying rental orders,
    converting to a string format for database interaction, and loading rental objects
    from the database.

    Attributes:
        id (int): Unique identifier for the rental order.
        car (Car): The car being rented.
        pickup_time (datetime): The pickup time for the rental.
        return_time (datetime): The return time for the rental.
        client (Person): The client who is renting the car.
    """

    __ID_COUNTER = 0  # A class variable to track the next available ID

    def __init__(self, pickup_time, return_time, client, car, id_=0, override=False):
        """
        Initializes a new instance of the Rent class.

        Args:
            pickup_time (str): The pickup time for the rental in 'YYYY-MM-DD HH:MM:SS' format.
            return_time (str): The return time for the rental in 'YYYY-MM-DD HH:MM:SS' format.
            client (int): The ID of the client who is renting the car.
            car (int): The ID of the car being rented.
            id_ (int, optional): The ID of the rental order. Default is 0.
            override (bool, optional): If True, the id_ parameter is used as the ID.
        """
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
        """
        Reads the current ID counter from a file and updates the class variable.
        """
        with open(RENT_ID_COUNTER, 'r') as fh:
            Rent.__ID_COUNTER = int(fh.read())

    @staticmethod
    def save_id_counter():
        """
        Saves the current ID counter to a file.
        """
        with open(RENT_ID_COUNTER, 'w') as fh:
            fh.write(str(Rent.__ID_COUNTER))

    # Method definitions for obj_to_str, get_table, show, get_fieldnames, get_id
    # and property methods for pickup_time, return_time, car, client are included here.
    # Each property setter includes validation logic to ensure input values meet specific criteria.

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
        """
        Calculates the cost of the rental based on the number of days and the car's daily rate.

        Returns:
            int: The total rental cost.
        """
        days = self._return_time - self._pickup_time
        return days.days * self.car.day_cost

    @classmethod
    def load_from_db(cls):
        """
        Class method to load rental data from the database and create Rent objects.

        Returns:
            list: A list of Rent objects loaded from the database.
        """
        order_data = cls.load(table='rent')

        objects = []
        for row in order_data:
            # Creates Rent object for each row in the database and adds it to the list
            objects.append(cls(pickup_time=row[1],
                               return_time=row[2],
                               client=row[3],
                               car=row[4],
                               id_=row[0], override=True))

        return objects
