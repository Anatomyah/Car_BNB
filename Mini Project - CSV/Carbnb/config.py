# Configuration settings for the Car Rental Management System

# File paths for various CSV files used in the system.
# These paths are utilized by other modules to access and manage data.

CARS_PATH = r'C:\Users\User\PycharmProjects\class2\Mini Project\Package\System files\cars.csv'
# Path to the CSV file containing car data

PERSON_PATH = r'C:\Users\User\PycharmProjects\class2\Mini Project\Package\System files\person.csv'
# Path to the CSV file containing person data

RENT_PATH = r'C:\Users\User\PycharmProjects\class2\Mini Project\Package\System files\rent.csv'
# Path to the CSV file containing rental transaction data

RENT_ID_COUNTER = r'C:\Users\User\PycharmProjects\class2\Mini Project\Package\System files\id_counter.txt'
# Path to the file used for tracking the next available rental ID

LOGGER = r'C:\Users\User\PycharmProjects\class2\Mini Project\Package\System files\carbnb.log'
# Path to the log file for the application

# Field names for the CSV files. These are used by the FileHandler class
# to read and write data to the CSV files in a structured format.

RENT_FIELDNAMES = ['ID','Pickup Time','Return Time','Client','Car']
# Field names for the rent.csv file

CARS_FIELDNAMES = ['Serial','Brand','Model','Year','Engine','Day Cost','KM','Owner']
# Field names for the cars.csv file

PERSON_FIELDNAMES = ['ID','First Name','Last Name','Age','Email','Phone']
# Field names for the person.csv file
