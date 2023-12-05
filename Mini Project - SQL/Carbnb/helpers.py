import sqlite3
from datetime import datetime as dt
from config import DATABASE, LOGGER
import logging


def query_db(query, db=DATABASE, result=False):
    res = None

    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute(query)

        if result:
            res = c.fetchall()

        conn.commit()

    return res


def auto_log(msg, object_id):
    logging.basicConfig(filename=LOGGER, level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s')
    logging.info(f"{msg}: ID: {object_id}")


def is_available(car_id, pickup_t, return_t):
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
    query = f"SELECT * FROM {table} WHERE id = {object_id}"

    res = query_db(query, result=True)

    assert len(res) != 0

    return res


def get_cars(self):
    query = f"SELECT c.id, c.brand, c.model, c.year, c.engine, c.day_cost, c.km FROM cars c " \
            f"JOIN person p ON c.owner = p.id WHERE p.id = {self.id};"
    data_output = query_db(query)

    return data_output


def get_orders(self, second_obj=None, future_orders=False):
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
        data_output = query_db(query, result=True)

        for order in data_output:
            pickup = dt.strptime(order[1], '%Y-%m-%d %H:%M:%S')
            if pickup > dt.now():
                final_output.append(order)
    else:
        final_output = query_db(query, result=True)

    return final_output


def rent_cost_general(days, car):
    return days.days * car.day_cost
