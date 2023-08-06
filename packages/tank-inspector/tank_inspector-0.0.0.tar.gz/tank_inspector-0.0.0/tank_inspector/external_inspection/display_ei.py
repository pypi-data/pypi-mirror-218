import sqlite3
conn = sqlite3.connect("database.db")


def display_values_ei_table():  # FUNCTION TO DISPLAY VALUES FROM EXTERNAL INSPECTION TANK TABLE
    print("DISPLAY DATA FROM AN EXTERNAL INSPECTION TABLE THROUGH SERIAL NUMBER")

    # table name input
    table_name = input("Enter a external inspection table name: ")
    # serial number input
    sl_num = input("Enter serial number: ")

    # EXECUTE SELECT QUERY WITH ERROR HANDLER
    try:
        # CHECK WHETHER ENTERED SERIAL NUMBER IS PRESENT OR NOT
        cursor = conn.execute(
            "SELECT sl_num FROM {} WHERE sl_num=?".format(table_name), (sl_num,))
        result = cursor.fetchone()  # Retrieve the row
        if result is not None:
            # Access the value
            serial = result[0]
        else:
            # Handle the case when no row is found
            serial = None

        # HANDLE CASE IF ENTERED SERIAL NUMBER IS FOUND
        if serial == None:
            print("Serial number: ", sl_num, " not found!")

        # HANDLE CASE IF ENTERED SERIAL NUMBER IS FOUND
        else:
            # execute select query
            data = conn.execute('''
                SELECT * FROM {} WHERE sl_num=?
                '''.format(table_name), (sl_num,))

            # print data
            for n in data:
                print("Serial number: ", n[0], ",", " Particulars: ", n[1],
                      ","" yes or no: ", n[2],)

    # handle error
    except sqlite3.OperationalError as err:
        print(err)


# FUNCTION TO DISPLAY VALUES FROM EXTERNAL INSPECTION SPECIFICATION TABLE
def display_values_ei_tank_specification():
    print("DISPLAY DATA FROM EXTERNAL INSPECTION TANK SPECIFICATION TABLE THROUGH TANK NUMBER")

    # enter tank number
    Tank_num = input("Enter tank number: ")

    # EXECUTE SELECT QUERY WITH ERROR HANDLER
    try:
        # CHECK WHETHER THE ENTERED TANK NUMBER IS PRESENT OR NOT IN THE DATABASE
        cursor = conn.execute(
            "SELECT Tank_num FROM ei_tank_specification WHERE Tank_num=?", (Tank_num,))
        result = cursor.fetchone()  # Retrieve the row
        if result is not None:
            # Access the value
            serial = result[0]
        else:
            # Handle the case when no row is found
            serial = None

        # HANDLE CASE WHEN ENTERED TANK NUMBER IS NO FOUND
        if serial == None:
            print("Tank number: ", Tank_num, " not found!")

        # HANDLE CASE WHEN ENTERED TANK NUMBER IS FOUND
        else:
            # execute select query
            data = conn.execute('''
                SELECT * FROM ei_tank_specification WHERE Tank_num=?
                ''', (Tank_num,))

            # print data
            for n in data:
                print("Location: ", n[0], ", Tank number: ", n[1],
                      ", Service fluid: ", n[2], ", Capacity in kL: ", n[3],
                      ", Diameter in m: ", n[4], ", Height in m: ", n[5], ", Tank type: ", n[6],
                      ", Last inspection date: ", n[7], ", Current inspection date: ", n[8])
    # HANDLE ERROR
    except sqlite3.OperationalError as err:
        print(err)
