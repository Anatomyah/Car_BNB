import copy
from datetime import datetime as dt
from person import Person
from car import Car
from rent import Rent
from filehandler import FileHandler
from helpers import *
from config import *


def main_menu():
    possible_actions = ['1', '2', '3', '4', '5', '6', '7', '0']
    print('\n*** Carbnb **\n'
          '[1] Add a client\n'
          '[2] Edit/Delete a client\n'
          '[3] Add a car\n'
          '[4] Edit/Delete a Car\n'
          '[5] Create a new order\n'
          '[6] Edit/Delete an order\n'
          '[7] Calculate earnings\n'
          '[0] Exit')
    action1 = input('-->')

    while action1 not in possible_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        action1 = input('-->')

    return action1


############################ CLIENT MENU ###########################################


def add_client():
    print("Please enter new client details:")
    client_d = {'ID': input("ID number: "), 'First Name': input("First name: "), 'Last Name': input("Last name: "),
                'Age': input("Age: "), 'Email': input("Email address: "), 'Phone': input("Phone number: ")}

    client = save_client(client_d=client_d)

    auto_log('Client added', object_id=client.id)
    print("\n*** Client added successfully! ***\n")

    menu_navigator()


def save_client(client=None, client_d: dict = None):
    if client:
        client_d = client.obj_to_dict()

    p = None

    while p is None:
        try:
            Person(id_=client_d['ID'], f_name=client_d['First Name'], l_name=client_d['Last Name'],
                   age=client_d['Age'], email=client_d['Email'], phone=client_d['Phone'])
        except AssertionError as e:
            print(e)
            if client_d:
                add_client()
            elif client and client_d:
                edit_client(client)
        else:
            p = Person(id_=client_d['ID'], f_name=client_d['First Name'], l_name=client_d['Last Name'],
                       age=client_d['Age'], email=client_d['Email'], phone=client_d['Phone'])

    FileHandler.save(p)

    return p


def client_menu():
    client_actions = ['1', '2', '0']
    print("[1] Edit a client\n"
          "[2] Delete a client\n"
          "[0] Return to the Main Menu")
    client_act = input("-->")

    while client_act not in client_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        client_act = input('-->')

    match client_act:
        case '1':
            while True:
                try:
                    client_id = int(input("Enter client ID"))
                except ValueError as e:
                    print(e)
                    print("ID number must contain numbers")
                else:
                    edit_client(get_client(client_id))
                    break
        case '2':
            while True:
                try:
                    client_id = int(input("Enter client ID"))
                except ValueError as e:
                    print(e)
                    print("ID number must contain numbers")
                else:
                    delete_client(client_id)
                    break
        case '3':
            menu_navigator()


def get_client(id_num):
    client_d = None

    try:
        get_by_id(id_num, PERSON_PATH)
    except TypeError as e:
        print("Entered ID does not exist in our database")
        client_menu()
    else:
        client_d = get_by_id(id_num, PERSON_PATH)

    client = Person(id_=client_d['ID'],
                    f_name=client_d['First Name'],
                    l_name=client_d['Last Name'],
                    age=client_d['Age'],
                    email=client_d['Email'],
                    phone=client_d['Phone'])
    client.show()

    return client


def edit_client(client):
    client_copy = copy.deepcopy(client)
    possible_actions = ['1', '2', '3', '4', '5', '6', '0']

    while True:
        print("[1] Edit ID\n"
              "[2] Edit First Name\n"
              "[3] Edit Last Name\n"
              "[4] Edit Age\n"
              "[5] Edit Email\n"
              "[6] Edit Phone\n"
              "[0] Return to Main Menu")
        edit_client_act = input("-->")

        while edit_client_act not in possible_actions:
            edit_client_act = input("-->")

        match edit_client_act:
            case '1':
                client.id = input("Enter new ID")
            case '2':
                client.f_name = input("Enter new First Name")
            case '3':
                client.l_name = input('Enter new Last Name')
            case '4':
                client.age = input('Enter new Age')
            case '5':
                client.email = input("Enter new Email")
            case '6':
                client.phone = input('Enter new Phone')
            case '0':
                menu_navigator()

        print("Anything else to edit?\n"
              "[1] Yes\n"
              "[2] No")

        edit_act = input("-->")
        match edit_act:
            case '1':
                pass
            case '2':
                if client.id == client_copy.id:
                    FileHandler.delete(client_copy)
                    save_client(client)
                else:
                    save_client(client)
                    FileHandler.delete(client_copy)

                break

    auto_log('Client edited', object_id=client.id)
    print("\n*** Client edited successfully! ***\n")

    menu_navigator()


def delete_client(id_num):
    client = get_client(id_num)

    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")
    while True:
        del_client_act = input("-->")
        if del_client_act == '1' or '2':
            break

    match del_client_act:
        case '1':
            FileHandler.delete(client)

            auto_log('Client deleted', object_id=client.id)
            print("\n*** Client deleted successfully ***")

            menu_navigator()

        case '2':
            client_menu()


# CAR MENU


def get_car(id_num):
    car_d = None

    try:
        get_by_id(id_num, CARS_PATH)
    except TypeError as e:
        print("Entered ID does not exist in our database")
        car_menu()
    else:
        car_d = get_by_id(id_num, CARS_PATH)

    car = Car(serial=car_d['Serial'], brand=car_d['Brand'], model=car_d['Model'], year=car_d['Year'],
              engine=car_d['Engine'], day_cost=car_d['Day Cost'], km=car_d['KM'], owner=car_d['Owner'])

    car.show()

    return car


def edit_car(car):
    car_copy = copy.deepcopy(car)
    possible_actions = ['1', '2', '3', '4', '5', '6', '7', '8', '0']

    while True:
        print("\n[1] Edit serial number\n"
              "[2] Edit Brand\n"
              "[3] Edit Model\n"
              "[4] Edit Year\n"
              "[5] Edit Engine\n"
              "[6] Edit Day Cost\n"
              "[7] Edit KM\n"
              "[8] Edit Owner\n"
              "[0] Return to Car Menu")
        edit_car_act = input("-->")

        while edit_car_act not in possible_actions:
            edit_car_act = input("-->")

        match edit_car_act:
            case '1':
                car.id = input("Enter new serial number")
            case '2':
                car.brand = input("Enter new Brand")
            case '3':
                car.model = input('Enter new Model')
            case '4':
                car.year = input('Enter new Year')
            case '5':
                car.engine = input("Enter new Engine")
            case '6':
                car.day_cost = input('Enter new Day Cost')
            case '7':
                car.km = input('Enter new KM')
            case '8':
                car.owner = input('Enter new Owner')
            case '0':
                car_menu()

        print("Anything else to edit?\n"
              "[1] Yes\n"
              "[2] No")

        edit_act = input("-->")
        match edit_act:
            case '1':
                pass
            case '2':
                if car.id == car_copy.id:
                    save_car(car=car)
                else:
                    save_car(car=car)
                    FileHandler.delete(car_copy)
                break

    auto_log('Car edited', object_id=car.id)
    print("\n*** Client edited successfully! ***\n")

    menu_navigator()


def delete_car(serial_num):
    car = get_car(serial_num)

    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")
    while True:
        del_car_act = input("-->")
        if del_car_act == '1' or '2':
            break

    match del_car_act:
        case '1':
            FileHandler.delete(car)

            auto_log('Car deleted', object_id=car.serial)
            print("\n*** Car deleted successfully ***\n")

            menu_navigator()

        case '2':
            car_menu()


def car_menu():
    car_actions = ['1', '2', '0']
    print("[1] Edit a car\n"
          "[2] Delete a car\n"
          "[0] Return to the Main Menu")
    car_act = input("-->")

    while car_act not in car_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        car_act = input('-->')

    match car_act:
        case '1':
            while True:
                try:
                    serial_num = int(input("Enter car Serial Number"))
                except ValueError as e:
                    print(e)
                    print("Serial Number must contain numbers")
                else:
                    edit_car(get_car(serial_num))
                    break
        case '2':
            while True:
                try:
                    car_id = int(input("Enter Serial Number"))
                except ValueError as e:
                    print(e)
                    print("Serial Number must contain numbers")
                else:
                    delete_car(car_id)
                    break
        case '0':
            menu_navigator()


def save_car(car=None, car_d: dict = None):
    if car:
        car_d = car.obj_to_dict()

    c = None

    while c is None:
        try:
            Car(serial=car_d['Serial'], brand=car_d['Brand'], model=car_d['Model'], year=car_d['Year'],
                engine=car_d['Engine'], day_cost=car_d['Day Cost'], km=car_d['KM'], owner=car_d['Owner'])
        except AssertionError as e:
            print(e)
            if car_d:
                add_car()
            elif car and car_d:
                edit_car(car)

        except TypeError as e:
            print("Owner ID for this car dos not exist in our database.\n Update client card first.")
        else:
            c = Car(serial=car_d['Serial'], brand=car_d['Brand'], model=car_d['Model'], year=car_d['Year'],
                    engine=car_d['Engine'], day_cost=car_d['Day Cost'], km=car_d['KM'], owner=car_d['Owner'])

    FileHandler.save(c)

    return c


def add_car():
    print("Please enter new car details:")
    car_d = {'Serial': input("Serial number: "), 'Brand': input("Brand: "), 'Model': input("Model: "), 'Year': input("Year: "),
             'Engine': input("Engine: "), 'Day Cost': input("Day Cost: "), 'KM': input('Kilometers: '),
             'Owner': input('Owner ID: ')}

    car = save_car(car_d=car_d)

    auto_log('Car added', object_id=car.serial)
    print("\n*** Car added successfully! ***\n")

    menu_navigator()


############################ ORDER MENU ###########################################


def get_order(id_num):
    order_d = None
    try:
        get_by_id(id_num, RENT_PATH)
    except TypeError as e:
        print("Entered ID does not exist in our database")
        order_menu()
    else:
        order_d = get_by_id(id_num, RENT_PATH)

    print("*** Order Details ***")
    for k, v in order_d.items():
        print(f"{k}: {v}")

    return order_d


def edit_order(order_d):
    possible_actions = ['1', '2', '3', '4', '0']

    while True:
        print("\n[1] Edit Pickup Time\n"
              "[2] Edit Return Time\n"
              "[3] Edit Client\n"
              "[4] Edit Car\n"
              "[0] Return to Car Menu")
        edit_order_act = input("-->")

        while edit_order_act not in possible_actions:
            edit_order_act = input("-->")

        match edit_order_act:
            case '1':
                pickup_year = input("Enter new Pickup Time:\n"
                                    "Year (YYYY): ")
                pickup_month = input("Month (MM): ")
                pickup_day = input('Day (DD): ')
                order_d['Pickup Time'] = f"{pickup_year}-{pickup_month}-{pickup_day}"
            case '2':
                return_year = input("Enter pickup time: \n"
                                    "Year (YYYY): ")
                return_month = input("Month (MM): ")
                return_day = input("Day (DD): ")
                order_d['Return Time'] = f"{return_year}-{return_month}-{return_day}"
            case '3':
                order_d['Client'] = input('Enter new Client ID')
            case '4':
                order_d['Car'] = input("Enter new Car ID")
            case '0':
                car_menu()

        print("Anything else to edit?\n"
              "[1] Yes\n"
              "[2] No")

        edit_act = input("-->")
        match edit_act:
            case '1':
                pass
            case '2':
                save_order(order_d)
                break

    auto_log('Order edited', object_id=order_d['ID'])
    print("\n*** Order edited successfully! ***\n")

    menu_navigator()


def delete_order(id_num):
    order_d = get_order(id_num)

    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")
    while True:
        del_ord_act = input("-->")
        if del_ord_act == '1' or '2':
            break

    match del_ord_act:
        case '1':
            FileHandler.delete(object_d=order_d)

            auto_log('Order deleted', object_id=order_d['ID'])
            print("\n*** Order deleted successfully ***\n")

            menu_navigator()

        case '2':
            order_menu()


def order_menu():
    order_actions = ['1', '2', '0']
    print("[1] Edit an order\n"
          "[2] Delete an order\n"
          "[0] Return to the Main Menu")
    order_act = input("-->")

    while order_act not in order_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        order_act = input('-->')

    match order_act:
        case '1':
            while True:
                try:
                    order_id = int(input("Enter order ID"))
                except ValueError as e:
                    print(e)
                    print("ID number must contain numbers")
                else:
                    edit_order(get_order(order_id))
                    break
        case '2':
            while True:
                try:
                    order_id = int(input("Enter order ID"))
                except ValueError as e:
                    print(e)
                    print("ID number must contain numbers")
                else:
                    delete_order(order_id)
                    break
        case '0':
            menu_navigator()


def save_order(order_d: dict, new_order=False):
    res = None

    while res is None:
        try:
            Rent(pickup_time=order_d['Pickup Time'], return_time=order_d['Return Time'], client=order_d['Client'],
                 car=order_d['Car'])

        except AssertionError as e:
            print(e)
            order_menu()
        else:
            if new_order:
                o = Rent(pickup_time=order_d['Pickup Time'], return_time=order_d['Return Time'],
                         client=order_d['Client'],
                         car=order_d['Car'])
                res = o
                FileHandler.save(self=o)

            elif res is None:
                FileHandler.save(object_d=order_d)
                break

        return res


def add_order():
    print("Please enter new order details:")

    pickup_year = input("Enter pickup time: \n"
                        "Year (YYYY): ")
    pickup_month = input("Month (MM): ")
    pickup_day = input("Day (DD): ")

    return_year = input("Enter return time: \n"
                        "Year (YYYY): ")
    return_month = input("Month (MM): ")
    return_day = input("Day (DD): ")

    order_d = {'Pickup Time': f"{pickup_year}-{pickup_month}-{pickup_day} 00:00:00",
               'Return Time': f"{return_year}-{return_month}-{return_day} 00:00:00",
               'Client': input("Enter Client ID: "), 'Car': input("Enter Car ID: ")}

    order = save_order(order_d=order_d, new_order=True)

    auto_log('New Order added', object_id=order.id)
    print("\n*** Car added successfully! ***\n")

    menu_navigator()


# EARNING CALCULATION


def get_date_range(year=False, date_range=False):
    start_date = None
    end_date = None

    if year:
        c_year = input("Enter calendar year: ")
        start_date = dt.strptime(f"{c_year}-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        end_date = dt.strptime(f"{c_year}-12-31 00:00:00", '%Y-%m-%d %H:%M:%S')

    elif date_range:
        start_year = input("Enter range start date: \n"
                           "Year (YYYY): ")
        start_month = input("Month (MM): ")
        start_day = input("Day (DD): ")

        end_year = input("Enter range end date: \n"
                         "Year (YYYY): ")
        end_month = input("Month (MM): ")
        end_day = input("Day (DD): ")

        start_date = dt.strptime(f"{start_year}-{start_month}-{start_day} 00:00:00", '%Y-%m-%d %H:%M:%S')
        end_date = dt.strptime(f"{end_year}-{end_month}-{end_day} 00:00:00", '%Y-%m-%d %H:%M:%S')

    return {'start': start_date, 'end': end_date}


def year_cal(date_d):
    orders = FileHandler.load(file_path=RENT_PATH)
    cars = Car.load_from_csv()
    res = 0

    for order in orders:
        car = [x for x in cars if x.id == int(order['Car'])][0]
        pickup_date = dt.strptime(order['Pickup Time'], '%Y-%m-%d %H:%M:%S')
        if date_d['start'] < pickup_date < date_d['end']:
            return_date = dt.strptime(order['Return Time'], '%Y-%m-%d %H:%M:%S')
            days = return_date - pickup_date
            res += rent_cost_general(days, car)

    print('\n', ('*' * 10), f"Yearly earnings for calendar year {date_d['start'].year} are {res} NIS", ('*' * 10))


def range_cal(date_d):
    orders = FileHandler.load(file_path=RENT_PATH)
    cars = Car.load_from_csv()
    res = 0
    start_str = dt.strftime(date_d['start'], '%Y-%m-%d')
    end_str = start_str = dt.strftime(date_d['end'], '%Y-%m-%d')

    for order in orders:
        car = [x for x in cars if x.id == int(order['Car'])][0]
        pickup_date = dt.strptime(order['Pickup Time'], '%Y-%m-%d %H:%M:%S')
        if date_d['start'] < pickup_date < date_d['end']:
            return_date = dt.strptime(order['Return Time'], '%Y-%m-%d %H:%M:%S')
            days = return_date - pickup_date
            res += rent_cost_general(days, car)

    print('\n', ('*' * 10), f"Earnings between {start_str}-{end_str} are {res} NIS", ('*' * 10))


def yearly_earnings(year=False, date_range=False):
    possible_actions = ['1', '2', '0']

    print("[1] Calculate by calendar year\n"
          "[2] Calculate a given date range\n"
          "[0] Return to the Main Menu")
    action = input("-->")

    while action not in possible_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        action = input('-->')

    match action:
        case '1':
            date_d = get_date_range(year=True)
            year_cal(date_d)
        case '2':
            date_d = get_date_range(date_range=True)
            range_cal(date_d)
        case '0':
            menu_navigator()

    menu_navigator()


# Unitesting



def menu_navigator():
    action = main_menu()
    match action:
        case '1':
            add_client()
        case '2':
            client_menu()
        case '3':
            add_car()
        case '4':
            car_menu()
        case '5':
            add_order()
        case '6':
            order_menu()
        case '7':
            yearly_earnings()
        case '0':
            'Goodbye!'
            exit(0)


menu_navigator()
