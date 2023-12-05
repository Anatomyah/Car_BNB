import sqlite3
from datetime import datetime as dt
from config import DATABASE, LOGGER
import logging


def query_db(query, db=DATABASE, result=False):
    """
    Executes a SQL query on the specified database.

    Args:
        query (str): The SQL query to be executed.
        db (str, optional): The database file path. Defaults to DATABASE.
        result (bool, optional): If True, fetches and returns the query results.

    Returns:
        list: The result of the query if result is True; otherwise, None.
    """
    res = None

    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute(query)

        if result:
            res = c.fetchall()

        conn.commit()

    return res


def auto_log(msg, object_id):
    """
    Logs a message with an associated object ID.

    Args:
        msg (str): The message to be logged.
        object_id (int): The ID of the object related to the log message.
    """
    logging.basicConfig(filename=LOGGER, level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s')
    logging.info(f"{msg}: ID: {object_id}")


def is_available(car_id, pickup_t, return_t):
    """
    Checks if a car is available for rent between specified pickup and return times.

    Args:
        car_id (int): The ID of the car to check.
        pickup_t (datetime): The pickup time.
        return_t (datetime): The return time.

    Returns:
        bool: True if the car is available; otherwise, False.
    """
    query = f"SELECT * FROM rent WHERE car = {car_id}"
    orders = query_db(query, result=True)
    flag = False

    for order in orders:
        pickup_time = dt.strptime(order[1], '%Y-%m-%d %H:%M:%S')
        return_time = dt.strptime(order[2], '%Y-%m-%d %H:%M:%S')

        if return_time >= pickup_t >= pickup_time or pickup_time <= return_t <= return_time:
            flag = True
            break

    return flag


def get_by_id(object_id, table):
    """
    Retrieves a record from the database by its ID.

    Args:
        object_id (int): The ID of the object to retrieve.
        table (str): The name of the table to query.

    Returns:
        list: The data row corresponding to the object ID.

    Raises:
        AssertionError: If no record is found with the specified ID.
    """
    query = f"SELECT * FROM {table} WHERE id = {object_id}"

    res = query_db(query, result=True)

    assert len(res) != 0

    return res


def get_cars(self):
    """
    Retrieves car data for a given owner.

    Returns:
        list: A list of car data rows owned by the person instance.
    """
    query = f"SELECT c.id, c.brand, c.model, c.year, c.engine, c.day_cost, c.km FROM cars c " \
            f"JOIN person p ON c.owner = p.id WHERE p.id = {self.id};"
    data_output = query_db(query)

    return data_output


def get_orders(self, second_obj=None, future_orders=False):
    """
    Retrieves orders related to the current object, optionally filtering by a second object or future orders.

    Args:
        second_obj (Person or Car, optional): A second object to filter the orders.
        future_orders (bool, optional): If True, returns only future orders.

    Returns:
        list: A list of order data rows related to the object.
    """
    query = None

    if self.__class__.__name__ == 'Person':
        if second_obj:
            query = f"SELECT r.id, r.pickup, r.return, r.client, r.car FROM rent r " \
                    f"JOIN person p ON r.client = p.id" \
                    f"JOIN cars c ON r.car = c.id " \
                    f"WHERE p.id = {self.id} AND c.id = {second_obj.id};"
        else:
            query = f"SELECT r.id, r.pickup, r.return, r.client, r.car FROM rent r " \
                    f"JOIN person p ON r.client = p.id WHERE p.id = {self.id};"

    elif self.__class__.__name__ == 'Car':
        if second_obj:
            query = f"SELECT r.id, r.pickup, r.return, r.client, r.car FROM rent r " \
                    f"JOIN cars c ON r.car = c.id" \
                    f"JOIN person p ON r.client = p.id " \
                    f"WHERE c.id = {self.id} AND p.id = {second_obj.id};"
        else:
            query = f"SELECT r.id, r.pickup, r.return, r.client, r.car FROM rent r " \
                    f"JOIN cars c ON r.car = c.id WHERE c.id = {self.id};"

    if future_orders:
        final_output = []
        # Fetch the data from the database based on the constructed query
        data_output = query_db(query, result=True)

        for order in data_output:
            # Convert the pickup time string from the order to a datetime object
            pickup = dt.strptime(order[1], '%Y-%m-%d %H:%M:%S')

            # Check if the pickup time is in the future compared to the current time
            if pickup > dt.now():
                final_output.append(order)
    else:
        # If not filtering for future orders, fetch all data based on the query
        final_output = query_db(query, result=True)

    return final_output


def rent_cost_general(days, car):
    """
      Calculates the total cost of renting a car for a given number of days.

      Args:
          days (timedelta): The number of days the car is rented.
          car (Car): The car object being rented.

      Returns:
          int: The total cost of the rental.
      """
    return days.days * car.day_cost
