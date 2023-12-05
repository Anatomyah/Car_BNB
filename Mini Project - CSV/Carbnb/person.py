from config import *
from filehandler import FileHandler
import re


class Person(FileHandler):
    def __init__(self, id_, f_name, l_name, age, email, phone):
        """
           Initializes a new Person object.

           Parameters:
               id_ (str): Unique identifier for the person.
               f_name (str): First name of the person.
               l_name (str): Last name of the person.
               age (int): Age of the person.
               email (str): Email address of the person.
               phone (str): Phone number of the person.
           """
        self.id = id_
        self.f_name = f_name
        self.l_name = l_name
        self.age = age
        self.email = email
        self.phone = phone

    def show(self):
        """
          Displays the details of the person.
          """
        print(f"ID: {self._id}\n" 
               f"First Name: {self._f_name}\n" 
               f"Last Name: {self._l_name}\n" 
               f"Age: {self._age}\n" 
               f"Email: {self._email}\n" 
               f"Phone: {self._phone}")

    def obj_to_str(self):
        """
          Converts the person object to a string representation for storage.

          Returns:
              str: A string representation of the person object.
          """
        return f"{self._id},{self._f_name},{self._l_name},{self._age},{self._email},{self._phone}"

    def obj_to_dict(self):
        """
           Converts the person object to a dictionary representation.

           Returns:
               dict: A dictionary representation of the person object.
           """
        return {'ID': self._id, 'First Name': self._f_name, 'Last Name': self._l_name, 'Age': self._age,
                'Email': self._email, 'Phone': self._phone}

    def get_file_path(self, fieldnames=False):
        """
         Provides the file path for storing person data.

         Parameters:
             fieldnames (bool): If True, returns file path and field names.

         Returns:
             str or dict: File path or dictionary with file path and field names.
         """
        res = PERSON_PATH

        if fieldnames:
            res = {'file_path': PERSON_PATH, 'fieldnames': PERSON_FIELDNAMES}

        return res

    def get_id(self):
        """
        Returns the ID of the person.

        Returns:
            str: The ID of the person.
        """
        return self.id

    # Properties and setters for various attributes follow, ensuring data integrity and validation
    @property
    def id(self):
        # Getter for id ...
        return self._id

    @id.setter
    def id(self, new_val):
        # Setter for id with validation ...
        assert len(str(new_val)) > 6 and not any(x.isalpha() for x in str(new_val)), f"Invalid ID number. " \
            f"Number cannot contain letters or be under 6 characters"

        self._id = new_val

    # Similar property and setter definitions for f_name, l_name, age, email, phone
    @property
    def f_name(self):
        return self._f_name

    @f_name.setter
    def f_name(self, new_val):
        assert len(str(new_val)) > 2 and not any(x.isnumeric() for x in str(new_val)), f"Invalid Name. Name cannot contain numbers" \
                                                                        f"or be under 3 characters"
        new_val = new_val.capitalize()
        self._f_name = new_val

    @property
    def l_name(self):
        return self._l_name

    @l_name.setter
    def l_name(self, new_val):
        assert len(str(new_val) )> 2 and not any(x.isnumeric() for x in str(new_val)), f"Invalid Name. Name cannot contain numbers" \
                                                                        f" or be under 3 characters"

        new_val = new_val.capitalize()
        self._l_name = new_val

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_val):
        assert not any(x.isalpha() for x in str(new_val)) or 17 < int(new_val) < 120, f"Invalid age. " \
            f"Must be between 17-120 and cannot contain letters"

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
        assert len(str(new_val)) == 10 and not any(x.isalpha() for x in str(new_val)) ,f"Invalid phone number. " \
            f"Number cannot contain letters and be 10 characters long"

        self._phone = new_val

    @classmethod
    def load_from_csv(cls):
        """
            Loads person objects from a CSV file.

            Returns:
                list of Person: A list of person objects loaded from the file.
        """
        reader = FileHandler.load(file_path=PERSON_PATH)

        objects = []
        for row in reader:
            objects.append(cls(id_=row['ID'],
                               f_name=row['First Name'],
                               l_name=row['Last Name'],
                               age=row['Age'],
                               email=int(row['Email']),
                               phone=int(row['Phone'])))

        return objects
