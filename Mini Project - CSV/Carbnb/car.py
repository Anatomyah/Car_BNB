from config import *
from filehandler import FileHandler
from helpers import get_by_id
from person import Person


class Car(FileHandler):
    """
     Represents a car in the system, encapsulating various attributes of a car
     and providing methods to handle car-related operations.

     Attributes:
         serial (int): Unique identifier for the car.
         brand (str): Brand of the car.
         model (str): Model of the car.
         year (int): Manufacturing year of the car.
         engine (int): Engine capacity of the car.
         day_cost (int): Daily rental cost of the car.
         km (int): Total kilometers driven by the car.
         owner (Person): Owner of the car, represented by a Person object.
     """

    def __init__(self, serial, brand, model, year, engine, day_cost, km, owner):
        # Initialize the car with specified attributes
        self.serial = serial
        self.brand = brand
        self.model = model
        self.year = year
        self.engine = engine
        self.day_cost = day_cost
        self.km = km
        self.owner = owner

    def show(self):
        # Display the details of the car
        print(f"\n*** Car Details ***\n"
              f"ID: {self._serial}\n"
              f"Brand: {self._brand}\n"
              f"Model: {self._model}\n"
              f"Year: {self._year}\n"
              f"Engine: {self._engine}\n"
              f"Day Cost: {self._day_cost}\n"
              f"KM: {self._km}\n"
              f"Owner ID: {self._owner}")

    def obj_to_str(self):
        # Convert car object to a string representation suitable for CSV files
        return f"{self._serial},{self._brand},{self._model},{self._year},{self._engine}," \
               f"{self._day_cost},{self._km},{self._owner.id}"

    def obj_to_dict(self):
        # Convert car object to a dictionary representation
        return {'Serial': self._serial, 'Brand': self._brand, 'Model': self._model, 'Year': self._year,
                'Engine': self._engine, 'Day Cost': self._day_cost, 'KM': self._km, 'Owner': self._owner.id}

    def get_file_path(self, fieldnames=False):
        # Get the file path for car data, with an option to include fieldnames
        res = CARS_PATH
        if fieldnames:
            res = {'file_path': CARS_PATH, 'fieldnames': CARS_FIELDNAMES}
        return res

    def get_id(self):
        # Get the unique serial number of the car
        return self.serial

    # Properties and setters for various attributes follow, ensuring data integrity and validation

    @property
    def serial(self):
        # Return the car's serial number
        return self._serial

    @serial.setter
    def serial(self, new_val):
        # Set a new serial number for the car after validation
        assert len(str(new_val)) > 6 and not any(x.isalpha() for x in str(new_val)), "Invalid ID number."
        self._serial = new_val

    # Similar property and setter definitions for brand, model, year, engine, day_cost, km, owner

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
        assert len(new_val) > 2 and not any(x.isnumeric() for x in new_val), f"Invalid Model. Name cannot contain" \
                                                                             f" numbers or be under 3 characters"
        new_val = new_val.capitalize()
        self._model = new_val

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, new_val):
        assert len(str(new_val)) == 4 and not any(x.isalpha() for x in str(new_val)), f"Invalid year. " \
                                                                                      f"Number cannot contain letters and must be 4 characters long"

        self._year = new_val

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, new_val):
        assert 2 < len(str(new_val)) < 5 and not any(x.isalpha() for x in str(new_val)), f"Invalid engine size. " \
                                                                                         f"Number cannot contain letters and must be between 3-4 characters"

        self._engine = new_val

    @property
    def day_cost(self):
        return self._day_cost

    @day_cost.setter
    def day_cost(self, new_val):
        assert len(str(new_val)) < 6 and not any(x.isalpha() for x in str(new_val)), f"Invalid price. " \
                                                                                     f"Number cannot contain letters and must be under 6 characters"

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

        row = get_by_id(new_value, PERSON_PATH)
        assert new_value is not None, f"This owner ID does not exists in our database"

        self._owner = Person(row['ID'], row['First Name'], row['Last Name'], row['Age'], row['Email'],
                             row['Phone'])

    @classmethod
    def load_from_csv(cls):
        # Load car objects from a CSV file
        reader = FileHandler.load(file_path=CARS_PATH)
        objects = []

        for row in reader:
            objects.append(cls(serial=int(row['Serial']),
                               brand=row['Brand'],
                               model=row['Model'],
                               year=int(row['Year']),
                               engine=int(row['Engine']),
                               day_cost=int(row['Day Cost']),
                               km=int(row['KM']),
                               owner=int(row['Owner'])))

        return objects
