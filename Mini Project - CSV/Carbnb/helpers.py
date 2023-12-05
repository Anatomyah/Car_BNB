import csv
from datetime import datetime as dt
from config import *
import logging


def auto_log(msg, object_id):

    logging.basicConfig(filename=LOGGER, level=logging.DEBUG,format='%(levelname)s:%(asctime)s:%(message)s')
    logging.info(f"{msg}: ID: {object_id}")


def is_available(order):
    reader = order.load()
    flag = True

    for row in reader:
        pickup_time = dt.strptime(row['Pickup Time'], '%Y-%m-%d %H:%M:%S')
        return_time = dt.strptime(row['Return Time'], '%Y-%m-%d %H:%M:%S')

        if return_time >= order._pickup_time >= pickup_time or pickup_time <= order._return_time <= return_time:
            flag = False

            break

    return flag


def get_by_id(id_, file):
    with open(file=file, mode='r') as fh:
        reader = csv.DictReader(fh)
        rows = [x for x in reader]

    res = None

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
    res = []
    with open(file=CARS_PATH, mode='r') as fh:
        reader = csv.DictReader(fh)
        rows = [x for x in reader]

        for row in rows:
            if row['ID'] == self.id:
                res.append(row)

    return res


def get_orders(self, future_orders=False):
    res = []
    with open(file=RENT_PATH, mode='r') as fh:
        reader = csv.DictReader(fh)
        rows = [x for x in reader]

        if self.__class__.__name__ == 'Person':
            for row in rows:
                pickup_time = dt.strptime(row['Pickup Time'], '%Y-%m-%d %H:%M:%S')
                if int(row['Client']) == int(self.id) and future_orders and pickup_time > dt.now():
                    res.append(row)

                elif int(row['Client']) == int(self.id):
                    res.append(row)

        elif self.__class__.__name__ == 'Car':
            for row in rows:
                pickup_time = dt.strptime(row['Pickup Time'], '%Y-%m-%d %H:%M:%S')
                if int(row['Car']) == int(self.id) and future_orders and pickup_time > dt.now():
                    res.append(row)

                elif int(row['Car']) == int(self.id):
                    res.append(row)

    return res


def rent_cost_general(days, car):

    return days.days * car.day_cost


