from config import CARS_FIELDNAMES
from filehandler import FileHandler
from helpers import get_by_id
from person import Person


class Car(FileHandler):
    """
    A subclass of FileHandler that represents a car and its associated operations.

    This class encapsulates the properties of a car and provides methods to handle
    car-related data, including displaying details, converting to string for database
    purposes, and loading car objects from the database.

    Attributes:
        id (int): Identification number of the car.
        brand (str): Brand of the car.
        model (str): Model of the car.
        year (int): Year of manufacture of the car.
        engine (int): Engine size of the car.
        day_cost (int): Daily cost for renting the car.
        km (int): Total kilometers driven by the car.
        owner (Person): The owner of the car.
    """

    def __init__(self, id_, brand, model, year, engine, day_cost, km, owner):
        """
        Initializes a new instance of the Car class.

        Args:
            id_ (int): Identification number of the car.
            brand (str): Brand of the car.
            model (str): Model of the car.
            year (int): Year of manufacture of the car.
            engine (int): Engine size of the car.
            day_cost (int): Daily cost for renting the car.
            km (int): Total kilometers driven by the car.
            owner (int): ID of the owner of the car.
        """
        self.id = id_
        self.brand = brand
        self.model = model
        self.year = year
        self.engine = engine
        self.day_cost = day_cost
        self.km = km
        self.owner = owner

    def show(self):
        """
        Displays the details of the car.
        """
        print(f"\n*** Car Details ***\n"
              f"ID: {self._id}\n"
              f"Brand: {self._brand}\n"
              f"Model: {self._model}\n"
              f"Year: {self._year}\n"
              f"Engine: {self._engine}\n"
              f"Day Cost: {self._day_cost}\n"
              f"KM: {self._km}\n"
              f"Owner ID: {self._owner.id}")

    def obj_to_str(self):
        """
              Converts the car object's properties to a string suitable for database storage.

              Returns:
                  str: A string representation of the car object's properties.
              """
        return f"'{self._id}', '{self._brand}', '{self._model}', {self._year}, {self._engine}, " \
               f"{self._day_cost}, '{self._km}', '{self._owner.id}'"

    def get_table(self):
        """
              Returns the table name associated with Car objects for database operations.

              Returns:
                  str: The table name.
              """
        return 'cars'

    def get_fieldnames(self, fieldnames=False):
        """
               Returns the fieldnames for car attributes.

               Args:
                   fieldnames (bool): Unused parameter in the current implementation.

               Returns:
                   list: A list of field names for the Car object.
               """
        return CARS_FIELDNAMES

    def get_id(self):
        """
               Retrieves the identification number of the car.

               Returns:
                   int: The ID of the car.
               """
        return self.id

    # Property methods (id, brand, model, year, engine, day_cost, km, owner)
    # with their respective setters are included here.
    # Each setter contains validation logic to ensure that the input values meet specific criteria.

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_val):
        assert len(str(new_val)) > 6 and not any(x.isalpha() for x in str(new_val)), f"Invalid ID number. " \
                                                                                     f"Number cannot contain letters " \
                                                                                     f"or be under 6 characters"

        self._id = new_val

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, new_val):
        assert len(new_val) > 2 and not any(x.isnumeric() for x in new_val), f"Invalid Brand. Name cannot contain" \
                                                                             f" numbers or be under 3 characters"

        new_val = new_val.capitalize()
        self._brand = new_val

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, new_val):
        assert len(new_val) > 2 , f"Invalid Model name. Name must be over 3 characters"
        new_val = new_val.capitalize()
        self._model = new_val

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, new_val):
        assert len(str(new_val)) == 4 and not any(x.isalpha() for x in str(new_val)), f"Invalid year. " \
                                                                                      f"Number cannot contain letters "\
                                                                                      f"and must be 4 characters long"

        self._year = new_val

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, new_val):
        assert 2 < len(str(new_val)) < 5 and not any(x.isalpha() for x in str(new_val)), f"Invalid engine size. " \
                                                                                         f"Number cannot contain " \
                                                                                         f"letters and must be " \
                                                                                         f"between 3-4 characters"

        self._engine = new_val

    @property
    def day_cost(self):
        return self._day_cost

    @day_cost.setter
    def day_cost(self, new_val):
        assert len(str(new_val)) < 6 and not any(x.isalpha() for x in str(new_val)), f"Invalid price. " \
                                                                                     f"Number cannot contain letters " \
                                                                                     f"and must be under 6 characters"

        self._day_cost = new_val

    @property
    def km(self):
        return self._km

    @km.setter
    def km(self, new_val):
        assert not any(x.isalpha() for x in str(new_val)), f"Invalid Kilometer amount. " \
                                                           f"Number cannot contain letters."

        self._km = new_val

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, new_value):
        owner_data = get_by_id(new_value, table='person')[0]
        assert new_value is not None, f"This owner ID does not exists in our database"

        self._owner = Person(owner_data[0], owner_data[1], owner_data[2], owner_data[3], owner_data[4],
                             owner_data[5])

    def load_from_db(cls):
        """
        Class method to load car data from the database and create Car objects.

        Returns:
            list: A list of Car objects loaded from the database.
        """
        cars_data = cls.load(table='cars')

        objects = []
        for row in cars_data:
            # Creates Car object for each row in the database and adds it to the list
            objects.append(cls(id_=int(row[0]),
                               brand=row[1],
                               model=row[2],
                               year=int(row[3]),
                               engine=int(row[4]),
                               day_cost=int(row[5]),
                               km=int(row[6]),
                               owner=int(row[7])))

        return objects
