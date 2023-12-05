from datetime import datetime as dt
from person import Person
from car import Car
from rent import Rent
from filehandler import FileHandler
from helpers import auto_log, get_by_id, rent_cost_general


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


# CAR MENU


def add_client():
    print("Please enter new client details:")
    client_d = {'id': input("ID number: "), 'p_name': input("First name: "), 'l_name': input("Last name: "),
                'age': input("Age: "), 'email': input("Email address: "), 'phone': input("Phone number: ")}

    client = save_client(client_d)

    auto_log('Client added', object_id=client.id)
    print("\n*** Client added successfully! ***\n")

    menu_navigator()


def save_client(client_d: dict):
    p = None

    while p is None:
        try:
            Person(id_=client_d['id'], p_name=client_d['p_name'], l_name=client_d['l_name'], age=client_d['age'],
                   email=client_d['email'], phone=client_d['phone'])
        except AssertionError as e:
            print(e)
            add_client()
        else:
            p = Person(id_=client_d['id'], p_name=client_d['p_name'], l_name=client_d['l_name'], age=client_d['age'],
                       email=client_d['email'], phone=client_d['phone'])

    p.save()

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
    client_data = None

    try:
        get_by_id(id_num, table='person')
    except AssertionError as e:
        print("Entered ID does not exist in our database")
        client_menu()
    else:
        client_data = get_by_id(id_num, table='person')

    client = Person(id_=client_data[0][0],
                    p_name=client_data[0][1],
                    l_name=client_data[0][2],
                    age=client_data[0][3],
                    email=client_data[0][4],
                    phone=client_data[0][5])
    client.show()

    return client


def edit_client(client):
    possible_actions = ['1', '2', '3', '4', '5', '6', '0']
    clauses_lst = []

    while True:
        print("\n[1] Edit ID\n"
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
                clauses_lst.append(f"id = '{client.id}'")
            case '2':
                client.f_name = input("Enter new first mame")
                clauses_lst.append(f"pname = '{client._f_name}'")
            case '3':
                client.l_name = input('Enter new last name')
                clauses_lst.append(f"lname = '{client._l_name}'")
            case '4':
                client.age = input('Enter new age')
                clauses_lst.append(f"age = {client.age}")
            case '5':
                client.email = input("Enter new Email address")
                clauses_lst.append(f"email = '{client.email}'")
            case '6':
                client.phone = input('Enter new phone number')
                clauses_lst.append(f"phone = '{client._phone}'")
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
                client.edit(set_clauses=clauses_lst)

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
            client.delete()

            auto_log('Client deleted', object_id=client.id)
            print("\n*** Client deleted successfully ***")

            menu_navigator()

        case '2':
            client_menu()


# CAR MENU


def get_car(id_num):
    car_data = None

    try:
        get_by_id(id_num, table='cars')
    except TypeError as e:
        print("Entered ID does not exist in our database")
        car_menu()
    else:
        car_data = get_by_id(id_num, table='cars')[0]

    car = Car(id_=car_data[0], brand=car_data[1], model=car_data[2], year=car_data[3],
              engine=car_data[4], day_cost=car_data[5], km=car_data[6], owner=car_data[7])

    car.show()

    return car


def edit_car(car):
    possible_actions = ['1', '2', '3', '4', '5', '6', '7', '8', '0']
    clauses_lst = []

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
                clauses_lst.append(f'id = "{car._id}"')
            case '2':
                car.brand = input("Enter new Brand")
                clauses_lst.append(f'brand = "{car._brand}"')
            case '3':
                car.model = input('Enter new Model')
                clauses_lst.append(f'model = "{car._model}"')
            case '4':
                car.year = input('Enter new Year')
                clauses_lst.append(f'year = {car._year}')
            case '5':
                car.engine = input("Enter new Engine")
                clauses_lst.append(f'engine = {car._engine}')
            case '6':
                car.day_cost = input('Enter new Day Cost')
                clauses_lst.append(f'day_cost = {car._day_cost}')
            case '7':
                car.km = input('Enter new KM')
                clauses_lst.append(f'km = {car._km}')
            case '8':
                car.owner = input('Enter new Owner')
                clauses_lst.append(f'owner = "{car.owner}"')
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
                car.edit(set_clauses=clauses_lst)

                break

    auto_log('Car edited', object_id=car.id)
    print("\n*** Client edited successfully! ***\n")

    menu_navigator()


def delete_car(id_num):
    car = get_car(id_num)

    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")
    while True:
        del_car_act = input("-->")
        if del_car_act == '1' or '2':
            break

    match del_car_act:
        case '1':
            car.delete()

            auto_log('Car deleted', object_id=car.id)
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
                    car_id = int(input("Enter car serial number"))
                except ValueError as e:
                    print(e)
                    print("Serial number must contain numbers only")
                else:
                    edit_car(get_car(car_id))
                    break
        case '2':
            while True:
                try:
                    car_id = int(input("Enter serial number"))
                except ValueError as e:
                    print(e)
                    print("Serial number must contain numbers only")
                else:
                    delete_car(car_id)
                    break
        case '0':
            menu_navigator()


def save_car(car_d: dict):
    c = None

    while c is None:
        try:
            Car(id_=car_d['id_'], brand=car_d['brand'], model=car_d['model'], year=car_d['year'],
                engine=car_d['engine'], day_cost=car_d['day_cost'], km=car_d['km'], owner=car_d['owner'])
        except AssertionError as e:
            print(e)
            add_car()

        except TypeError as e:
            print("Owner ID for this car does not exist in our database.\n Update client card first.")
            menu_navigator()
        else:
            c = Car(id_=car_d['id_'], brand=car_d['brand'], model=car_d['model'], year=car_d['year'],
                    engine=car_d['engine'], day_cost=car_d['day_cost'], km=car_d['km'], owner=car_d['owner'])

    c.save()

    return c


def add_car():
    print("Please enter new car details:")
    car_d = {'id_': input("Serial number: "), 'brand': input("Brand: "), 'model': input("Model: "),
             'year': input("Year: "),
             'engine': input("Engine: "), 'day_cost': input("Day Cost: "), 'km': input('Kilometers: '),
             'owner': input('Owner ID: ')}

    car = save_car(car_d=car_d)

    auto_log('Car added', object_id=car.id)
    print("\n*** Car added successfully! ***\n")

    menu_navigator()


# ORDER MENU


def get_order(id_num):
    order_data = None

    try:
        get_by_id(id_num, table='rent')
    except TypeError as e:
        print("Entered ID does not exist in our database")
        order_menu()
    else:
        order_data = get_by_id(id_num, table='rent')[0]

    o = Rent(pickup_time=order_data[1],
             return_time=order_data[2],
             client=order_data[3],
             car=order_data[4],
             id_=order_data[0], override=True)

    o.show()

    return o


def edit_order(order):
    possible_actions = ['1', '2', '3', '4', '0']
    clauses_lst = []

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
                order.pickup_time = f"{pickup_year}-{pickup_month}-{pickup_day} 00:00:00"
                clauses_lst.append(f'pickup = "{order._pickup_time}"')
            case '2':
                return_year = input("Enter pickup time: \n"
                                    "Year (YYYY): ")
                return_month = input("Month (MM): ")
                return_day = input("Day (DD): ")
                order.return_time = f"{return_year}-{return_month}-{return_day} 00:00:00"
                clauses_lst.append(f'return = "{order._return_time}"')
            case '3':
                order.client = input('Enter new Client ID')
                clauses_lst.append(f'client = "{order.client}"')
            case '4':
                order.car = input("Enter new Car ID")
                clauses_lst.append(f'car = "{order.car}"')
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
                order.edit(set_clauses=clauses_lst)

                break

    auto_log('Order edited', object_id=order.id)
    print("\n*** Order edited successfully! ***\n")

    menu_navigator()


def delete_order(id_num):
    order = get_order(id_num)

    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")
    while True:
        del_ord_act = input("-->")
        if del_ord_act == '1' or '2':
            break

    match del_ord_act:
        case '1':
            order.delete()

            auto_log('Order deleted', object_id=order.id)
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


def save_order(order_d: dict):
    o = None

    while o is None:
        try:
            Rent(pickup_time=order_d['Pickup Time'], return_time=order_d['Return Time'], client=order_d['Client'],
                 car=order_d['Car'], override=True)

        except AssertionError as e:
            print(e)
            order_menu()
        else:
            o = Rent(pickup_time=order_d['Pickup Time'], return_time=order_d['Return Time'],
                     client=order_d['Client'],
                     car=order_d['Car'])

        o.save()

        return o


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

    order = save_order(order_d=order_d)

    auto_log('New Order added', object_id=order.id)
    print("\n*** Order added successfully! ***\n")

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
    orders = FileHandler.load(table='rent')
    cars = Car.load_from_db()
    res = 0

    for order in orders:
        car = [c for c in cars if c.id == int(order[4])][0]
        pickup_date = dt.strptime(order[1], '%Y-%m-%d %H:%M:%S')
        if date_d['start'] < pickup_date < date_d['end']:
            return_date = dt.strptime(order[2], '%Y-%m-%d %H:%M:%S')
            days = return_date - pickup_date
            res += rent_cost_general(days, car)

    print('\n', ('*' * 10), f"Yearly earnings for calendar year {date_d['start'].year} are {res} NIS", ('*' * 10))


def range_cal(date_d):
    orders = FileHandler.load(table='rent')
    cars = Car.load_from_db()
    res = 0
    start_str = dt.strftime(date_d['start'], '%Y-%m-%d')
    end_str = dt.strftime(date_d['end'], '%Y-%m-%d')

    for order in orders:
        car = [x for x in cars if x.id == int(order[4])][0]
        pickup_date = dt.strptime(order[1], '%Y-%m-%d %H:%M:%S')
        if date_d['start'] < pickup_date < date_d['end']:
            return_date = dt.strptime(order[2], '%Y-%m-%d %H:%M:%S')
            days = return_date - pickup_date
            res += rent_cost_general(days, car)

    print('\n', ('*' * 10), f"Earnings between {start_str}-{end_str} are {res} NIS", ('*' * 10))


def yearly_earnings():
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
