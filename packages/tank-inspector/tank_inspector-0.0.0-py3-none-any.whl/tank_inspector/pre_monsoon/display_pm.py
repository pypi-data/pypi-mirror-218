import sqlite3
conn = sqlite3.connect("database.db")


def display_values_pm_table():  # function to display the values from pre monsoon table
    print("DISPLAY DATA FROM A PRE MONSOON TABLE THROUGH SERIAL NUMBER")
    table_name = input("Enter a pre monsoon table name: ")  # table name input
    sl_num = input("Enter serial number: ")  # serial number input

    # Execute SELECT query with try and except error handle
    try:
        # Check whether the entered serial number is present or not
        cursor = conn.execute(
            "SELECT sl_num FROM {} WHERE sl_num=?".format(table_name), (sl_num,))
        result = cursor.fetchone()  # Retrieve the row
        if result is not None:
            # Handle the case when row is found: Access the value
            serial = result[0]
        else:
            # Handle the case when no row is found
            serial = None

        # Handle the case of execution when no serial number is present
        if serial == None:
            print("Serial number: ", sl_num, " not found!")

        # Handle the case of execution when serial number is not present
        else:
            data = conn.execute('''
                SELECT * FROM {} WHERE sl_num=?
                '''.format(table_name), (sl_num,))

            for n in data:  # printing the data
                print("Serial number: ", n[0], ",", " Particulars: ", n[1],
                      ","" Completed: ", n[2], ","" Comment: ", n[3],)

    except sqlite3.OperationalError as err:
        print(err)


# Function to display the values from pre monsoon tank specification table
def display_values_pm_tank_specification():

    print("DISPLAY DATA FROM PRE MONSOON TANK SPECIFICATION TABLE THROUGH TANK NUMBER")
    Tank_num = input("Enter tank number: ")  # Tank number Input

    # Execute SELECT query with try and except error handle
    try:
        # Chech whether the entered tank number is present or not in the table
        cursor = conn.execute(
            "SELECT Tank_num FROM pre_monsoon_tank_specification WHERE Tank_num=?", (Tank_num,))
        result = cursor.fetchone()  # Retrieve the row
        if result is not None:
            # Access the value
            serial = result[0]
        else:
            # Handle the case when no row is found
            serial = None

        # Handle the case when table number entered is not found
        if serial == None:
            print("Tank number: ", Tank_num, " not found!")

        # Handle the case when table number entered is found
        else:
            data = conn.execute('''
                SELECT * FROM pre_monsoon_tank_specification WHERE Tank_num=?
                ''', (Tank_num,))
            for n in data:  # print data
                print("Location: ", n[0], ", Tank number: ", n[1],
                      ", Service fluid: ", n[2], ", Capacity in kL: ", n[3],
                      ", Diameter in m: ", n[4], ", Height in m: ", n[5], ", Tank type: ", n[6],
                      ", Last inspection date: ", n[7], ", Current inspection date: ", n[8])
    except sqlite3.OperationalError as err:
        print(err)
