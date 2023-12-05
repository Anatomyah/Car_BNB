import copy
from person import Person
from car import Car
from rent import Rent
from filehandler import FileHandler
from helpers import *
from config import *


def main_menu():
    """
       Displays the main menu of the application and handles user input for menu selection.

       Returns:
           str: The user's choice of action.
       """
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

    # Validate user input
    while action1 not in possible_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        action1 = input('-->')

    return action1


############################ CLIENT MENU ###########################################

def add_client():
    """
    Handles the addition of a new client. It prompts the user to enter client details,
    creates a new client object, logs the addition, and navigates back to the menu.
    """
    print("Please enter new client details:")
    # Collecting client details from the user
    client_d = {'ID': input("ID number: "), 'First Name': input("First name: "),
                'Last Name': input("Last name: "), 'Age': input("Age: "),
                'Email': input("Email address: "), 'Phone': input("Phone number: ")}

    # Saving the new client
    client = save_client(client_d=client_d)

    # Logging the addition of a new client
    auto_log('Client added', object_id=client.id)
    print("\n*** Client added successfully! ***\n")

    # Returning to the main menu
    menu_navigator()


def save_client(client=None, client_d: dict = None):
    """
    Saves a client object to the file system. Can be used to save a new client or update an existing one.

    Parameters:
        client (Person, optional): The client object to be saved. Defaults to None.
        client_d (dict, optional): Dictionary of client information. Defaults to None.

    Returns:
        Person: The saved or updated client object.
    """
    if client:
        client_d = client.obj_to_dict()

    p = None

    # Attempting to create a Person object with the provided details
    while p is None:
        try:
            # Validating and creating a new Person object
            p = Person(id_=client_d['ID'], f_name=client_d['First Name'], l_name=client_d['Last Name'],
                       age=client_d['Age'], email=client_d['Email'], phone=client_d['Phone'])
        except AssertionError as e:
            print(e)
            # Re-prompting for client details in case of an error
            if client_d:
                add_client()
            elif client and client_d:
                edit_client(client)
        else:
            # Successfully created a Person object
            p = Person(id_=client_d['ID'], f_name=client_d['First Name'], l_name=client_d['Last Name'],
                       age=client_d['Age'], email=client_d['Email'], phone=client_d['Phone'])

    # Saving the client object to the file system
    FileHandler.save(p)

    return p


def client_menu():
    """
    Displays the client management menu and handles user interaction for client operations.
    """
    client_actions = ['1', '2', '0']
    print("[1] Edit a client\n[2] Delete a client\n[0] Return to the Main Menu")
    client_act = input("-->")

    # Validating user input
    while client_act not in client_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        client_act = input('-->')

    # Handling the selected action
    match client_act:
        case '1':
            # Editing a client
            # Repeatedly prompt for client ID until a valid number is entered
            while True:
                try:
                    client_id = int(input("Enter client ID"))
                    edit_client(get_client(client_id))
                    break
                except ValueError as e:
                    print(e)
                    print("ID number must contain numbers")
        case '2':
            # Deleting a client
            # Repeatedly prompt for client ID until a valid number is entered
            while True:
                try:
                    client_id = int(input("Enter client ID"))
                    delete_client(client_id)
                    break
                except ValueError as e:
                    print(e)
                    print("ID number must contain numbers")
        case '3':
            # Returning to the main menu
            menu_navigator()


def get_client(id_num):
    """
    Retrieves a client object based on the provided ID number.

    Parameters:
        id_num (int): The ID number of the client to retrieve.

    Returns:
        Person: The client object if found, otherwise None.
    """
    client_d = None

    # Attempting to retrieve client details from the file system
    try:
        client_d = get_by_id(id_num, PERSON_PATH)
        # Creating a client object from the retrieved details
        client = Person(id_=client_d['ID'], f_name=client_d['First Name'], l_name=client_d['Last Name'],
                        age=client_d['Age'], email=client_d['Email'], phone=client_d['Phone'])
        client.show()

        return client
    except TypeError as e:
        print("Entered ID does not exist in our database")
        client_menu()


def edit_client(client):
    """
       Handles editing the details of an existing client.

       Parameters:
           client (Person): The client object to be edited.
       """
    client_copy = copy.deepcopy(client)
    possible_actions = ['1', '2', '3', '4', '5', '6', '0']

    # Loop for editing client details
    while True:
        print("[1] Edit ID\n[2] Edit First Name\n[3] Edit Last Name\n[4] Edit Age\n"
              "[5] Edit Email\n[6] Edit Phone\n[0] Return to Main Menu")
        edit_client_act = input("-->")

        # Validating user input
        while edit_client_act not in possible_actions:
            edit_client_act = input("-->")

        # Processing the edit action
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

                # Asking the user if they want to make more edits
        print("Anything else to edit?\n[1] Yes\n[2] No")
        edit_act = input("-->")
        match edit_act:
            case '1':
                pass  # Continue editing
            case '2':
                # Finalize edits and save changes
                if client.id == client_copy.id:
                    FileHandler.delete(client_copy)
                    save_client(client)
                else:
                    save_client(client)
                    FileHandler.delete(client_copy)

                break

    # Log the client edit and return to the main menu
    auto_log('Client edited', object_id=client.id)
    print("\n*** Client edited successfully! ***\n")

    menu_navigator()


def delete_client(id_num):
    """
    Handles the deletion of a client based on the provided ID number.

    Parameters:
        id_num (int): The ID number of the client to delete.
    """
    client = get_client(id_num)

    # Confirm deletion with the user
    print("\nConfirm delete?\n[1] Yes\n[2] No")
    while True:
        del_client_act = input("-->")
        if del_client_act == '1' or '2':
            break

    # Processing the deletion action
    match del_client_act:
        case '1':
            FileHandler.delete(client)

            # Log the client deletion and return to the main menu
            auto_log('Client deleted', object_id=client.id)
            print("\n*** Client deleted successfully ***")
            menu_navigator()

        case '2':
            # Return to the client menu without deleting
            client_menu()


# CAR MENU


def get_car(id_num):
    """
    Retrieves a car object based on the provided serial number.

    Parameters:
        id_num (int): The serial number of the car to retrieve.

    Returns:
        Car: The car object if found, otherwise returns to the car menu.
    """
    car_d = None

    # Attempting to retrieve car details from the file system
    try:
        car_d = get_by_id(id_num, CARS_PATH)
        # Creating a car object from the retrieved details
        car = Car(serial=car_d['Serial'], brand=car_d['Brand'], model=car_d['Model'],
                  year=car_d['Year'], engine=car_d['Engine'], day_cost=car_d['Day Cost'],
                  km=car_d['KM'], owner=car_d['Owner'])
        car.show()
        return car
    except TypeError as e:
        print("Entered ID does not exist in our database")
        car_menu()


def edit_car(car):
    """
    Handles editing the details of an existing car.

    Parameters:
        car (Car): The car object to be edited.
    """
    car_copy = copy.deepcopy(car)
    possible_actions = ['1', '2', '3', '4', '5', '6', '7', '8', '0']

    # Loop for editing car details
    while True:
        print("\n[1] Edit serial number\n[2] Edit Brand\n[3] Edit Model\n[4] Edit Year\n"
              "[5] Edit Engine\n[6] Edit Day Cost\n[7] Edit KM\n[8] Edit Owner\n"
              "[0] Return to Car Menu")
        edit_car_act = input("-->")

        # Validating user input
        while edit_car_act not in possible_actions:
            edit_car_act = input("-->")

        # Processing the edit action
        match edit_car_act:
            case '1':
                car.serial = input("Enter new serial number")
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

                # Asking the user if they want to make more edits
        print("Anything else to edit?\n[1] Yes\n[2] No")
        edit_act = input("-->")
        match edit_act:
            case '1':
                pass  # Continue editing
            case '2':
                # Finalize edits and save changes
                if car.serial == car_copy.serial:
                    save_car(car=car)
                else:
                    save_car(car=car)
                    FileHandler.delete(car_copy)
                break

        # Log the car edit and return to the main menu
    auto_log('Car edited', object_id=car.serial)
    print("\n*** Car edited successfully! ***\n")
    menu_navigator()


def delete_car(serial_num):
    """
    Handles the deletion of a car based on the provided serial number.

    Parameters:
        serial_num (int): The serial number of the car to delete.
    """
    car = get_car(serial_num)

    # Confirm deletion with the user
    print("\nConfirm delete?\n[1] Yes\n[2] No")
    while True:
        del_car_act = input("-->")
        if del_car_act == '1' or '2':
            break

    # Processing the deletion action
    match del_car_act:
        case '1':
            FileHandler.delete(car)

            # Log the car deletion and return to the main menu
            auto_log('Car deleted', object_id=car.serial)
            print("\n*** Car deleted successfully ***\n")
            menu_navigator()

        case '2':
            # Return to the car menu without deleting
            car_menu()


def car_menu():
    """
    Displays the car management menu and handles user interaction for car operations.
    """
    car_actions = ['1', '2', '0']
    print("[1] Edit a car\n[2] Delete a car\n[0] Return to the Main Menu")
    car_act = input("-->")

    # Validating user input
    while car_act not in car_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        car_act = input('-->')

    # Handling the selected action
    match car_act:
        case '1':
            # Editing a car
            # Repeatedly prompt for serial number until a valid number is entered
            while True:
                try:
                    serial_num = int(input("Enter car Serial Number"))
                    edit_car(get_car(serial_num))
                    break
                except ValueError as e:
                    print(e)
                    print("Serial Number must contain numbers")
        case '2':
            # Deleting a car
            # Repeatedly prompt for serial number until a valid number is entered
            while True:
                try:
                    car_id = int(input("Enter Serial Number"))
                    delete_car(car_id)
                    break
                except ValueError as e:
                    print(e)
                    print("Serial Number must contain numbers")
        case '0':
            # Returning to the main menu
            menu_navigator()


def save_car(car=None, car_d: dict = None):
    """
    Saves a car object to the file system. Can be used to save a new car or update an existing one.

    Parameters:
        car (Car, optional): The car object to be saved. Defaults to None.
        car_d (dict, optional): Dictionary of car information. Defaults to None.

    Returns:
        Car: The saved or updated car object.
    """
    if car:
        car_d = car.obj_to_dict()

    c = None

    # Attempting to create a Car object with the provided details
    while c is None:
        try:
            # Validating and creating a new Car object
            c = Car(serial=car_d['Serial'], brand=car_d['Brand'], model=car_d['Model'], year=car_d['Year'],
                    engine=car_d['Engine'], day_cost=car_d['Day Cost'], km=car_d['KM'], owner=car_d['Owner'])
        except AssertionError as e:
            print(e)
            # Re-prompting for car details in case of an error
            if car_d:
                add_car()
            elif car and car_d:
                edit_car(car)
        except TypeError as e:
            print("Owner ID for this car dos not exist in our database.\n Update client card first.")
        else:
            # Successfully created a Car object
            c = Car(serial=car_d['Serial'], brand=car_d['Brand'], model=car_d['Model'], year=car_d['Year'],
                    engine=car_d['Engine'], day_cost=car_d['Day Cost'], km=car_d['KM'], owner=car_d['Owner'])

    # Saving the car object to the file system
    FileHandler.save(c)

    return c


def add_car():
    """
    Handles the addition of a new car. It prompts the user to enter car details,
    creates a new car object, logs the addition, and navigates back to the menu.
    """
    print("Please enter new car details:")
    # Collecting car details from the user
    car_d = {'Serial': input("Serial number: "), 'Brand': input("Brand: "), 'Model': input("Model: "),
             'Year': input("Year: "), 'Engine': input("Engine: "), 'Day Cost': input("Day Cost: "),
             'KM': input('Kilometers: '), 'Owner': input('Owner ID: ')}

    # Saving the new car
    car = save_car(car_d=car_d)

    # Logging the addition of a new car
    auto_log('Car added', object_id=car.serial)
    print("\n*** Car added successfully! ***\n")

    # Returning to the main menu
    menu_navigator()


############################ ORDER MENU ###########################################


def get_order(id_num):
    """
    Retrieves an order based on the provided ID number.

    Parameters:
        id_num (int): The ID number of the order to retrieve.

    Returns:
        dict: The order details if found, otherwise returns to the order menu.
    """
    order_d = None

    # Attempting to retrieve order details from the file system
    try:
        order_d = get_by_id(id_num, RENT_PATH)
        # Printing the order details
        print("*** Order Details ***")
        for k, v in order_d.items():
            print(f"{k}: {v}")

        return order_d
    except TypeError as e:
        print("Entered ID does not exist in our database")
        order_menu()


def edit_order(order_d):
    """
    Handles editing the details of an existing order.

    Parameters:
        order_d (dict): The dictionary containing the order details.
    """
    possible_actions = ['1', '2', '3', '4', '0']

    # Loop for editing order details
    while True:
        print("\n[1] Edit Pickup Time\n[2] Edit Return Time\n[3] Edit Client\n[4] Edit Car\n[0] Return to Car Menu")
        edit_order_act = input("-->")

        # Validating user input
        while edit_order_act not in possible_actions:
            edit_order_act = input("-->")

        # Processing the edit action
        match edit_order_act:
            case '1':
                # Editing pickup time
                # Collecting new pickup time details
                pickup_year = input("Enter new Pickup Time:\nYear (YYYY): ")
                pickup_month = input("Month (MM): ")
                pickup_day = input('Day (DD): ')
                order_d['Pickup Time'] = f"{pickup_year}-{pickup_month}-{pickup_day}"
            case '2':
                # Editing return time
                return_year = input("Enter pickup time: \n"
                                    "Year (YYYY): ")
                return_month = input("Month (MM): ")
                return_day = input("Day (DD): ")
                order_d['Return Time'] = f"{return_year}-{return_month}-{return_day}"
            case '3':
                # Editing client ID
                order_d['Client'] = input('Enter new Client ID')
            case '4':
                # Editing car ID
                order_d['Car'] = input("Enter new Car ID")
            case '0':
                # Returning to the car menu
                car_menu()

        # Asking if the user wants to make more edits
        print("Anything else to edit?\n[1] Yes\n[2] No")
        edit_act = input("-->")
        match edit_act:
            case '1':
                pass  # Continue editing
            case '2':
                # Save the edited order and break the loop
                save_order(order_d)
                break

    # Log the order edit and return to the main menu
    auto_log('Order edited', object_id=order_d['ID'])
    print("\n*** Order edited successfully! ***\n")
    menu_navigator()



def delete_order(id_num):
    """
    Handles the deletion of an order based on the provided ID number.

    Parameters:
        id_num (int): The ID number of the order to delete.
    """
    order_d = get_order(id_num)

    # Confirm deletion with the user
    print("\nConfirm delete?\n[1] Yes\n[2] No")
    while True:
        del_ord_act = input("-->")
        if del_ord_act in ['1', '2']:
            break

    # Processing the deletion action
    match del_ord_act:
        case '1':
            # Delete the order and log the action
            FileHandler.delete(object_d=order_d)
            auto_log('Order deleted', object_id=order_d['ID'])
            print("\n*** Order deleted successfully ***\n")
            menu_navigator()
        case '2':
            # Return to the order menu without deleting
            order_menu()


def order_menu():
    """
        Displays the order management menu and handles user interaction for order operations.
        """
    order_actions = ['1', '2', '0']
    print("[1] Edit an order\n[2] Delete an order\n[0] Return to the Main Menu")
    order_act = input("-->")

    # Validating user input
    while order_act not in order_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        order_act = input('-->')

    # Handling the selected action
    match order_act:
        case '1':
            # Editing an order
            # Repeatedly prompt for order ID until a valid number is entered
            while True:
                try:
                    order_id = int(input("Enter order ID"))
                except ValueError as e:
                    print(e)
                    print("ID number must contain numbers")
                else:
                    edit_order(get_order(order_id))
                    break
        # Repeatedly prompt for order ID until a valid number is entered
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
            # Returning to the main menu
            menu_navigator()


def save_order(order_d: dict, new_order=False):
    """
    Saves an order to the file system. Can be used for a new order or updating an existing one.

    Parameters:
        order_d (dict): Dictionary of order information.
        new_order (bool): True if it's a new order, False otherwise.
    """
    res = None

    # Attempting to create a Rent object with the provided details
    while res is None:
        try:
            # Validating and creating a new Rent object
            Rent(pickup_time=order_d['Pickup Time'], return_time=order_d['Return Time'],
                 client=order_d['Client'], car=order_d['Car'])
        except AssertionError as e:
            print(e)
            order_menu()
        else:
            if new_order:
                # Handling new order creation
                o = Rent(pickup_time=order_d['Pickup Time'], return_time=order_d['Return Time'],
                         client=order_d['Client'], car=order_d['Car'])
                res = o
                FileHandler.save(self=o)
            elif res is None:
                # Updating an existing order
                FileHandler.save(object_d=order_d)
                break

        return res


def add_order():
    """
    Handles the addition of a new order. It prompts the user to enter order details,
    creates a new order object, logs the addition, and navigates back to the menu.
    """
    print("Please enter new order details:")
    # Collecting order details from the user
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

    # Logging the addition of a new order
    auto_log('New Order added', object_id=order.id)
    print("\n*** Order added successfully! ***\n")

    # Returning to the main menu
    menu_navigator()


# EARNING CALCULATION


def get_date_range(year=False, date_range=False):
    """
    Determines the start and end dates for earnings calculations.

    Parameters:
        year (bool): If True, calculates for a specific year.
        date_range (bool): If True, calculates for a custom date range.

    Returns:
        dict: Dictionary containing 'start' and 'end' datetime objects.
    """
    start_date = None
    end_date = None

    if year:
        # Handling calculation for a specific year
        c_year = input("Enter calendar year: ")
        start_date = dt.strptime(f"{c_year}-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        end_date = dt.strptime(f"{c_year}-12-31 00:00:00", '%Y-%m-%d %H:%M:%S')

    elif date_range:
        # Handling calculation for a custom date range
        # Code to gather start and end date inputs from the user
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
    """
    Calculates and prints the total earnings for a given calendar year.

    Parameters:
        date_d (dict): Dictionary with 'start' and 'end' dates.
    """
    orders = FileHandler.load(file_path=RENT_PATH)
    cars = Car.load_from_csv()
    res = 0

    # Iterating through orders to calculate earnings
    for order in orders:
        car = [x for x in cars if x.id == int(order['Car'])][0]
        pickup_date = dt.strptime(order['Pickup Time'], '%Y-%m-%d %H:%M:%S')
        if date_d['start'] < pickup_date < date_d['end']:
            # Calculating earnings for each order within the date range
            return_date = dt.strptime(order['Return Time'], '%Y-%m-%d %H:%M:%S')
            days = return_date - pickup_date
            res += rent_cost_general(days, car)

    # Printing the calculated yearly earnings
    print('\n', ('*' * 10), f"Yearly earnings for calendar year {date_d['start'].year} are {res} NIS", ('*' * 10))


def range_cal(date_d):
    """
    Calculates and prints the total earnings for a custom date range.

    Parameters:
        date_d (dict): Dictionary with 'start' and 'end' dates.
    """
    orders = FileHandler.load(file_path=RENT_PATH)
    cars = Car.load_from_csv()
    res = 0

    # Formatting start and end dates for display
    start_str = dt.strftime(date_d['start'], '%Y-%m-%d')
    end_str = dt.strftime(date_d['end'], '%Y-%m-%d')

    # Iterating through orders to calculate earnings
    for order in orders:
        car = [x for x in cars if x.id == int(order['Car'])][0]
        pickup_date = dt.strptime(order['Pickup Time'], '%Y-%m-%d %H:%M:%S')
        if date_d['start'] < pickup_date < date_d['end']:
            # Calculating earnings for each order within the date range
            return_date = dt.strptime(order['Return Time'], '%Y-%m-%d %H:%M:%S')
            days = return_date - pickup_date
            res += rent_cost_general(days, car)

    # Printing the calculated earnings for the custom date range
    print('\n', ('*' * 10), f"Earnings between {start_str}-{end_str} are {res} NIS", ('*' * 10))


def yearly_earnings(year=False, date_range=False):
    """
    Provides options for calculating earnings either by a calendar year or a custom date range.
    User inputs are handled to choose the preferred calculation method.
    """
    possible_actions = ['1', '2', '0']

    print("[1] Calculate by calendar year\n[2] Calculate a given date range\n[0] Return to the Main Menu")
    action = input("-->")

    # Validating user input
    while action not in possible_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        action = input('-->')

    # Processing the selected action for earnings calculation
    match action:
        case '1':
            date_d = get_date_range(year=True)
            year_cal(date_d)
        case '2':
            date_d = get_date_range(date_range=True)
            range_cal(date_d)
        case '0':
            # Returning to the main menu
            menu_navigator()

    menu_navigator()


def menu_navigator():
    """
    This function navigates through different functionalities of the application based on user input.
    It calls the respective function for each action selected from the main menu.
    """
    action = main_menu()  # Displaying the main menu and capturing user action

    # Matching the user's input to the corresponding function
    match action:
        case '1':
            add_client()  # Navigates to add a new client
        case '2':
            client_menu()  # Opens the client management menu
        case '3':
            add_car()  # Navigates to add a new car
        case '4':
            car_menu()  # Opens the car management menu
        case '5':
            add_order()  # Navigates to add a new order
        case '6':
            order_menu()  # Opens the order management menu
        case '7':
            yearly_earnings()  # Calculates and displays yearly earnings
        case '0':
            print('Goodbye!')  # Exits the application
            exit(0)


menu_navigator()
