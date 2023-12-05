from datetime import datetime as dt
from person import Person
from car import Car
from rent import Rent
from filehandler import FileHandler
from helpers import auto_log, get_by_id, rent_cost_general


def main_menu():
    """
    Displays the main menu for the Carbnb application and prompts the user to choose an action.

    This function prints a list of available actions and uses input to capture the user's choice.
    It ensures that the user's input is one of the valid options.

    Returns:
        str: The user's chosen action as a string.
    """

    # Define a list of valid action inputs
    possible_actions = ['1', '2', '3', '4', '5', '6', '7', '0']

    # Display the main menu options to the user
    print('\n*** Carbnb ***\n'
          '[1] Add a client\n'
          '[2] Edit/Delete a client\n'
          '[3] Add a car\n'
          '[4] Edit/Delete a Car\n'
          '[5] Create a new order\n'
          '[6] Edit/Delete an order\n'
          '[7] Calculate earnings\n'
          '[0] Exit')

    # Capture the user's choice
    action1 = input('-->')

    # Validate the user's input and prompt again if it's not a valid option
    while action1 not in possible_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        action1 = input('-->')

    # Return the valid action chosen by the user
    return action1


# CLIENT MENU


def add_client():
    """
    Prompts the user to enter details for adding a new client and saves the client information.
    """
    print("Please enter new client details:")
    # Collecting client details from user input
    client_d = {'id': input("ID number: "), 'p_name': input("First name: "),
                'l_name': input("Last name: "), 'age': input("Age: "),
                'email': input("Email address: "), 'phone': input("Phone number: ")}

    client = save_client(client_d)  # Saving the client

    auto_log('Client added', object_id=client.id)  # Logging the action
    print("\n*** Client added successfully! ***\n")

    menu_navigator()  # Returning to the main menu


def save_client(client_d: dict):
    """
    Creates and saves a Person object based on the given dictionary of client details.

    Args:
        client_d (dict): Dictionary containing client details.

    Returns:
        Person: The created Person object.
    """
    p = None

    while p is None:
        try:
            # Attempting to create a Person object. If an AssertionError occurs, it retries.
            p = Person(id_=client_d['id'], p_name=client_d['p_name'], l_name=client_d['l_name'],
                       age=client_d['age'], email=client_d['email'], phone=client_d['phone'])
        except AssertionError as e:
            print(e)
            add_client()  # Re-prompting for client details if an error occurs
        else:
            p.save()  # Saving the created Person object

    return p


def client_menu():
    """
    Displays a submenu for client-related actions and handles user choices.
    """
    client_actions = ['1', '2', '0']
    print("[1] Edit a client\n"
          "[2] Delete a client\n"
          "[0] Return to the Main Menu")
    client_act = input("-->")

    # Validation loop for user input
    while client_act not in client_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        client_act = input('-->')

    match client_act:
        case '1':
            # Edit client flow
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
            # Delete client flow
            while True:
                try:
                    client_id = int(input("Enter client ID"))
                except ValueError as e:
                    print(e)
                    print("ID number must contain numbers")
                else:
                    delete_client(client_id)
                    break
        case '0':
            # Return to main menu
            menu_navigator()


def get_client(id_num):
    """
      Retrieves a client's data and displays it.

      Args:
          id_num (int): The client's ID.

      Returns:
          Person: The retrieved client as a Person object.
      """
    client_data = None

    try:
        # Attempting to retrieve client data from the database
        client_data = get_by_id(id_num, table='person')
    except AssertionError as e:
        # Redirecting to the client menu if ID is not found
        print("Entered ID does not exist in our database")
        client_menu()

    # Creating and displaying the client object
    client = Person(id_=client_data[0][0],
                    p_name=client_data[0][1],
                    l_name=client_data[0][2],
                    age=client_data[0][3],
                    email=client_data[0][4],
                    phone=client_data[0][5])
    client.show()

    return client


def edit_client(client):
    """
     Allows editing different attributes of a client.

     Args:
         client (Person): The client object to be edited.
     """
    possible_actions = ['1', '2', '3', '4', '5', '6', '0']
    clauses_lst = []

    while True:
        # Displaying edit options and capturing user choice
        # Loop for handling client attribute edits
        # The client.edit method is called with the clauses_lst
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

    auto_log('Client edited', object_id=client.id)  # Logging the edit action
    print("\n*** Client edited successfully! ***\n")

    menu_navigator()  # Returning to the main menu


def delete_client(id_num):
    """
    Prompts the user to confirm the deletion of a client and proceeds with the deletion if confirmed.

    Args:
        id_num (int): The ID number of the client to be deleted.
    """
    # Retrieves the client object based on the provided ID
    client = get_client(id_num)

    # Prompt for confirmation of client deletion
    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")

    while True:
        del_client_act = input("-->")
        # Ensuring the user input is either '1' (Yes) or '2' (No)
        if del_client_act in ['1', '2']:
            break

    match del_client_act:
        case '1':
            # If the user confirms, proceed with client deletion
            client.delete()

            # Logging the deletion action
            auto_log('Client deleted', object_id=client.id)
            print("\n*** Client deleted successfully ***")

            # Returning to the main menu after deletion
            menu_navigator()

        case '2':
            # If the user cancels, return to the client menu
            client_menu()


# CAR MENU


def get_car(id_num):
    """
    Retrieves and displays a car's data based on the given ID number.

    Args:
        id_num (int): The serial number of the car to retrieve.

    Returns:
        Car: The retrieved car as a Car object.
    """
    car_data = None

    try:
        # Attempting to retrieve car data from the database
        car_data = get_by_id(id_num, table='cars')[0]
    except TypeError as e:
        print("Entered ID does not exist in our database")
        car_menu()  # Redirecting to the car menu if ID is not found
    else:
        # Creating and displaying the car object
        car = Car(id_=car_data[0], brand=car_data[1], model=car_data[2], year=car_data[3],
                  engine=car_data[4], day_cost=car_data[5], km=car_data[6], owner=car_data[7])
        car.show()

    return car


def edit_car(car):
    """
    Allows editing different attributes of a car.

    Args:
        car (Car): The car object to be edited.
    """
    possible_actions = ['1', '2', '3', '4', '5', '6', '7', '8', '0']
    clauses_lst = []

    while True:
        # Displaying edit options and capturing user choice
        # Loop for handling car attribute edits
        # The car.edit method is called with the clauses_lst
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

    auto_log('Car edited', object_id=car.id)  # Logging the edit action
    print("\n*** Car edited successfully! ***\n")

    menu_navigator()  # Returning to the main menu


def delete_car(id_num):
    """
    Deletes a car after confirming with the user.

    Args:
        id_num (int): The serial number of the car to be deleted.
    """
    car = get_car(id_num)  # Retrieves the car object

    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")

    while True:
        del_car_act = input("-->")
        if del_car_act == '1' or '2':
            break

    match del_car_act:
        case '1':
            # Deletes the car and logs the action
            car.delete()
            auto_log('Car deleted', object_id=car.id)
            print("\n*** Car deleted successfully ***\n")
            menu_navigator()
        case '2':
            car_menu()  # Returns to car menu if deletion is cancelled


def car_menu():
    """
    Displays a menu for car-related actions and handles user input for these actions.
    """
    car_actions = ['1', '2', '0']
    print("[1] Edit a car\n"
          "[2] Delete a car\n"
          "[0] Return to the Main Menu")
    car_act = input("-->")

    # Validation loop for user input
    while car_act not in car_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        car_act = input('-->')

    # Handling different actions based on user choice
    match car_act:
        case '1':
            # Edit car flow
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
            # Delete car flow
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
            # Return to main menu
            menu_navigator()


def save_car(car_d: dict):
    """
    Creates and saves a Car object based on the given dictionary of car details.

    Args:
        car_d (dict): Dictionary containing car details.

    Returns:
        Car: The created Car object.
    """
    c = None

    while c is None:
        try:
            # Attempts to create a Car object. If an exception occurs, it retries.
            c = Car(id_=car_d['id_'], brand=car_d['brand'], model=car_d['model'], year=car_d['year'],
                    engine=car_d['engine'], day_cost=car_d['day_cost'], km=car_d['km'], owner=car_d['owner'])
        except AssertionError as e:
            print(e)
            add_car()

        except TypeError as e:
            print("Owner ID for this car does not exist in our database.\n Update client card first.")
            menu_navigator()
        else:
            c.save()

    return c


def add_car():
    """
    Prompts the user to enter details for adding a new car and saves the car information.
    """
    print("Please enter new car details:")
    # Collecting car details from user input
    car_d = {'id_': input("Serial number: "), 'brand': input("Brand: "), 'model': input("Model: "),
             'year': input("Year: "), 'engine': input("Engine: "), 'day_cost': input("Day Cost: "),
             'km': input('Kilometers: '), 'owner': input('Owner ID: ')}

    car = save_car(car_d=car_d)  # Saving the car

    auto_log('Car added', object_id=car.id)  # Logging the action
    print("\n*** Car added successfully! ***\n")

    menu_navigator()  # Returning to the main menu


# ORDER MENU


def get_order(id_num):
    """
    Retrieves and displays an order's details based on the given ID number.

    Args:
        id_num (int): The ID of the order to retrieve.

    Returns:
        Rent: The retrieved order as a Rent object.
    """
    try:
        # Attempting to retrieve order data from the database
        order_data = get_by_id(id_num, table='rent')[0]
    except TypeError as e:
        print("Entered ID does not exist in our database")
        order_menu()  # Redirecting to the order menu if ID is not found
    else:
        # Creating and displaying the order object
        o = Rent(pickup_time=order_data[1], return_time=order_data[2], client=order_data[3],
                 car=order_data[4], id_=order_data[0], override=True)
        o.show()

    return o


def edit_order(order):
    """
    Allows editing different attributes of an order.

    Args:
        order (Rent): The order object to be edited.
    """
    possible_actions = ['1', '2', '3', '4', '0']
    clauses_lst = []

    while True:
        # Displaying edit options and capturing user choice
        # Loop for handling order attribute edits
        # The order.edit method is called with the clauses_lst
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

    auto_log('Order edited', object_id=order.id)  # Logging the edit action
    print("\n*** Order edited successfully! ***\n")

    menu_navigator()  # Returning to the main menu


def delete_order(id_num):
    """
    Deletes an order after confirming with the user.

    Args:
        id_num (int): The ID of the order to be deleted.
    """
    order = get_order(id_num)  # Retrieves the order object

    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")

    while True:
        del_ord_act = input("-->")
        if del_ord_act in ['1', '2']:
            break

    match del_ord_act:
        case '1':
            # Deletes the order and logs the action
            order.delete()
            auto_log('Order deleted', object_id=order.id)
            print("\n*** Order deleted successfully ***\n")
            menu_navigator()
        case '2':
            order_menu()  # Returns to order menu if deletion is cancelled


def order_menu():
    """
    Displays a menu for order-related actions and handles user input for these actions.
    """
    order_actions = ['1', '2', '0']
    print("[1] Edit an order\n"
          "[2] Delete an order\n"
          "[0] Return to the Main Menu")
    order_act = input("-->")

    # Validation loop for user input
    while order_act not in order_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        order_act = input('-->')

    # Handling different actions based on user choice
    match order_act:
        case '1':
            # Edit order flow
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
            # Delete order flow
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
            # Return to main menu
            menu_navigator()


def save_order(order_d: dict):
    """
    Creates and saves a Rent object based on the given dictionary of order details.

    Args:
        order_d (dict): Dictionary containing order details.

    Returns:
        Rent: The created Rent object.
    """
    o = None

    while o is None:
        try:
            # Attempts to create a Rent object. If an exception occurs, it retries.
            o = Rent(pickup_time=order_d['Pickup Time'], return_time=order_d['Return Time'],
                     client=order_d['Client'], car=order_d['Car'], override=True)
        except AssertionError as e:
            print(e)
            order_menu()  # Redirecting to the order menu if there's an error
        else:
            o.save()  # Saving the created Rent object

    return o


def add_order():
    """
        Prompts the user to enter details for adding a new order and saves the order information.
        """
    print("Please enter new order details:")
    # Collecting order details from user input

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

    order = save_order(order_d=order_d)  # Saving the order

    auto_log('New Order added', object_id=order.id)  # Logging the action
    print("\n*** Order added successfully! ***\n")

    menu_navigator()  # Returning to the main menu


# EARNING CALCULATION


def get_date_range(year=False, date_range=False):
    """
        Prompts the user to input either a specific year or a date range.

        Args:
            year (bool): If True, the user is prompted to enter a calendar year.
            date_range (bool): If True, the user is prompted to enter a date range.

        Returns:
            dict: A dictionary containing 'start' and 'end' datetime objects.
        """
    # Initialization of start and end dates
    start_date, end_date = None, None

    if year:
        # If year is selected, get the start and end dates for the entire year
        c_year = input("Enter calendar year: ")
        start_date = dt.strptime(f"{c_year}-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        end_date = dt.strptime(f"{c_year}-12-31 00:00:00", '%Y-%m-%d %H:%M:%S')

    elif date_range:
        # If date range is selected, prompt for specific start and end dates
        start_year = input("Enter range start date: \n"
                           "Year (YYYY): ")
        start_month = input("Month (MM): ")
        start_day = input("Day (DD): ")

        end_year = input("Enter range end date: \n"
                         "Year (YYYY): ")
        end_month = input("Month (MM): ")
        end_day = input("Day (DD): ")

        # Construct start and end datetime objects
        start_date = dt.strptime(f"{start_year}-{start_month}-{start_day} 00:00:00", '%Y-%m-%d %H:%M:%S')
        end_date = dt.strptime(f"{end_year}-{end_month}-{end_day} 00:00:00", '%Y-%m-%d %H:%M:%S')

    return {'start': start_date, 'end': end_date}


def year_cal(date_d):
    """
      Calculates and prints the total earnings for a given calendar year.

      Args:
          date_d (dict): A dictionary containing 'start' and 'end' datetime objects.
      """
    orders = FileHandler.load(table='rent')  # Load all orders
    cars = Car.load_from_db()  # Load all cars
    res = 0  # Initialize the total earnings

    for order in orders:
        car = [c for c in cars if c.id == int(order[4])][0]  # Find the car for each order
        pickup_date = dt.strptime(order[1], '%Y-%m-%d %H:%M:%S')
        # Check if the order falls within the specified year
        if date_d['start'] <= pickup_date <= date_d['end']:
            return_date = dt.strptime(order[2], '%Y-%m-%d %H:%M:%S')
            days = return_date - pickup_date  # Calculate rental duration
            res += rent_cost_general(days, car)  # Add to total earnings

    # Print total earnings for the year
    print('\n', ('*' * 10), f"Yearly earnings for calendar year {date_d['start'].year} are {res} NIS", ('*' * 10))


def range_cal(date_d):
    """
      Calculates and prints the total earnings for a specified date range.

      Args:
          date_d (dict): A dictionary containing 'start' and 'end' datetime objects.
      """
    # Similar logic as in year_cal, but for a specified date range
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

    # Print total earnings for the date range
    print('\n', ('*' * 10), f"Earnings between {start_str}-{end_str} are {res} NIS", ('*' * 10))


def yearly_earnings():
    """
        Displays options for calculating earnings and handles user selection.
        """
    possible_actions = ['1', '2', '0']

    # Display options for calculating earnings
    print("[1] Calculate by calendar year\n"
          "[2] Calculate a given date range\n"
          "[0] Return to the Main Menu")
    action = input("-->")  # Get user input

    # Validation loop for user input
    while action not in possible_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        action = input('-->')

    # Handle user selection
    match action:
        case '1':
            # Calculate earnings for a year
            date_d = get_date_range(year=True)
            year_cal(date_d)
        case '2':
            # Calculate earnings for a date range
            date_d = get_date_range(date_range=True)
            range_cal(date_d)
        case '0':
            # Return to main menu
            menu_navigator()

    menu_navigator()  # Return to the main menu


def menu_navigator():
    """
    Navigates to different functionalities of the car rental system based on user input from the main menu.
    """
    action = main_menu()  # Calls the main_menu function to display options and capture user choice

    match action:
        case '1':
            add_client()  # Navigates to adding a new client
        case '2':
            client_menu()  # Opens the client submenu for further actions
        case '3':
            add_car()  # Navigates to adding a new car
        case '4':
            car_menu()  # Opens the car submenu for further actions
        case '5':
            add_order()  # Navigates to adding a new order
        case '6':
            order_menu()  # Opens the order submenu for further actions
        case '7':
            yearly_earnings()  # Navigates to calculating yearly earnings
        case '0':
            print('Goodbye!')  # Exits the program
            exit(0)  # Properly exits the application


menu_navigator()
