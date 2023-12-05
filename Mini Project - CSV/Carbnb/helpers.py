import csv
from datetime import datetime as dt
from config import *
import logging


def auto_log(msg, object_id):
    """
       Log a message with the associated object ID.

       Parameters:
           msg (str): The message to log.
           object_id: The ID of the object related to the log message.
       """
    # Configure logging settings
    logging.basicConfig(filename=LOGGER, level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s')
    # Log the message
    logging.info(f"{msg}: ID: {object_id}")


def is_available(order):
    """
       Check if a car is available for rental within the specified time frame.

       Parameters:
           order: The rental order to check availability for.

       Returns:
           bool: True if available, False otherwise.
       """
    # Load existing rental orders
    reader = order.load()
    flag = True

    # Check each order for time overlap
    for row in reader:
        pickup_time = dt.strptime(row['Pickup Time'], '%Y-%m-%d %H:%M:%S')
        return_time = dt.strptime(row['Return Time'], '%Y-%m-%d %H:%M:%S')

        # Determine if the requested times conflict with existing orders
        if return_time >= order._pickup_time >= pickup_time or pickup_time <= order._return_time <= return_time:
            flag = False
            break

    return flag


def get_by_id(id_, file):
    """
       Retrieve a record by its ID from a specified CSV file.

       Parameters:
           id_ (int): The ID to look for.
           file (str): The path of the CSV file to search.

       Returns:
           dict or None: The found record as a dictionary, or None if not found.
       """
    # Read data from the specified file
    with open(file=file, mode='r') as fh:
        reader = csv.DictReader(fh)
        rows = [x for x in reader]

    res = None

    # Search for the ID in the appropriate column based on the file type
    if file == CARS_PATH:
        for row in rows:
            if row['Serial'] == str(id_):
                res = row
                break
    else:
        for row in rows:
            if row['ID'] == str(id_):
                res = row
                break

    return res


def get_cars(self):
    """
       Retrieve all cars associated with a person's ID.

       Parameters:
           self: The person object calling the method.

       Returns:
           list of dict: A list of car records.
       """
    res = []
    # Read car data from the file
    with open(file=CARS_PATH, mode='r') as fh:
        reader = csv.DictReader(fh)
        rows = [x for x in reader]

        # Find cars that match the person's ID
        for row in rows:
            if row['ID'] == self.id:
                res.append(row)

    return res


def get_orders(self, future_orders=False):
    """
        Retrieve all orders associated with a person or car.

        Parameters:
            self: The object (person or car) calling the method.
            future_orders (bool): If True, only retrieves future orders.

        Returns:
            list of dict: A list of order records.
        """
    res = []
    # Read rental data from the file
    with open(file=RENT_PATH, mode='r') as fh:
        reader = csv.DictReader(fh)
        rows = [x for x in reader]

        # Check for orders based on the object type and condition
        for row in rows:
            pickup_time = dt.strptime(row['Pickup Time'], '%Y-%m-%d %H:%M:%S')
            if self.__class__.__name__ == 'Person':
                # Retrieve orders for a person
                if int(row['Client']) == int(self.id) and (
                        future_orders and pickup_time > dt.now() or not future_orders):
                    res.append(row)
            elif self.__class__.__name__ == 'Car':
                # Retrieve orders for a car
                if int(row['Car']) == int(self.id) and (future_orders and pickup_time > dt.now() or not future_orders):
                    res.append(row)

    return res


def rent_cost_general(days, car):
    """
       Calculate the total rental cost for a specified number of days.

       Parameters:
           days (datetime.timedelta): The number of days for the rental.
           car: The car being rented.

       Returns:
           int: The total cost of the rental.
       """
    # Calculate cost based on the number of days and the daily
    return days.days * car.day_cost


