from config import PERSON_FIELDNAMES
from filehandler import FileHandler
import re


class Person(FileHandler):
    """
    A subclass of FileHandler that represents a person.

    This class manages a person's details and provides methods for displaying,
    converting to a string format for database interaction, and loading person
    objects from the database.

    Attributes:
        id (int): Identification number of the person.
        f_name (str): First name of the person.
        l_name (str): Last name of the person.
        age (int): Age of the person.
        email (str): Email address of the person.
        phone (str): Phone number of the person.
    """

    def __init__(self, id_, p_name, l_name, age, email, phone):
        """
        Initializes a new instance of the Person class.

        Args:
            id_ (int): Identification number of the person.
            p_name (str): First name of the person.
            l_name (str): Last name of the person.
            age (int): Age of the person.
            email (str): Email address of the person.
            phone (str): Phone number of the person.
        """
        self.id = id_
        self.f_name = p_name
        self.l_name = l_name
        self.age = age
        self.email = email
        self.phone = phone

    def show(self):
        """
        Displays the details of the person.
        """
        print(f"\n*** Client Details ***\n"
              f"ID: {self._id}\n"
              f"First Name: {self._f_name}\n"
              f"Last Name: {self._l_name}\n"
              f"Age: {self._age}\n"
              f"Email: {self._email}\n"
              f"Phone: {self._phone}")

    def obj_to_str(self):
        """
        Converts the person object's properties to a string format suitable for database storage.

        Returns:
            str: A string representation of the person object's properties.
        """
        return f"'{self._id}', '{self._f_name}', '{self._l_name}', {self._age}, " \
               f"'{self._email}', '{self._phone}'"

    def get_table(self):
        """
        Retrieves the database table name associated with the Person objects.

        Returns:
            str: The table name.
        """
        return 'person'

    def get_fieldnames(self, fieldnames=False):
        """
        Retrieves the field names for database operations for the Person object.

        Returns:
            str: The field names for the Person object.
        """
        return PERSON_FIELDNAMES

    def get_id(self):
        """
        Retrieves the identification number of the person.

        Returns:
            int: The ID of the person.
        """
        return self.id

    # Property methods (id, f_name, l_name, age, email, phone)
    # with their respective setters are included here.
    # Each setter includes validation logic to ensure the input values meet specific criteria.

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
    def f_name(self):
        return self._f_name

    @f_name.setter
    def f_name(self, new_val):
        assert len(str(new_val)) > 2 and not any(
            x.isnumeric() for x in str(new_val)), f"Invalid Name. Name cannot contain numbers" \
                                                  f"or be under 3 characters"
        new_val = new_val.capitalize()
        self._f_name = new_val

    @property
    def l_name(self):
        return self._l_name

    @l_name.setter
    def l_name(self, new_val):
        assert len(str(new_val)) > 2 and not any(
            x.isnumeric() for x in str(new_val)), f"Invalid Name. Name cannot contain numbers" \
                                                  f" or be under 3 characters"

        new_val = new_val.capitalize()
        self._l_name = new_val

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_val):
        assert not any(x.isalpha() for x in str(new_val)) or 17 < int(new_val) < 120, f"Invalid age. " \
                                                                                      f"Must be between 17-120 and " \
                                                                                      f"cannot contain letters"

        self._age = new_val

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_val):
        assert re.match(r"[^@]+@[^@]+\.[^@]+", new_val), f"Email address not in the correct format"

        self._email = new_val

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, new_val):
        assert len(str(new_val)) == 10 and not any(x.isalpha() for x in str(new_val)), f"Invalid phone number. " \
                                                                                       f"Number cannot contain " \
                                                                                       f"letters and be 10 characters "\
                                                                                       f"long"

        self._phone = new_val

    @classmethod
    def load_from_db(cls):
        """
        Class method to load person data from the database and create Person objects.

        Returns:
            list: A list of Person objects loaded from the database.
        """
        client_data = cls.load(table='person')

        objects = []
        for row in client_data:
            # Creates Person object for each row in the database and adds it to the list
            objects.append(cls(id_=row[0],
                               p_name=row[1],
                               l_name=row[2],
                               age=row[3],
                               email=int(row[4]),
                               phone=int(row[5])))

        return objects
