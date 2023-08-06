import sqlite3
conn = sqlite3.connect("database.db")


def update_values_ei_table():  # FUNCTION TO UPDATE VALUES FROM EXTERNAL INSPECTION TABLE

    print("UPDATE AN EXTERNAL INSPECTION TABLE DATA TROUGH SERIAL NUMBER")

    # table name input
    table_name = input("Enter table name : ")
    # serial number input
    sl_num = input("Enter serial number: ")

    # EXECUTE UPDATE QUERY WITH ERROR HANDLER
    try:
        # CHECK WHETHER ENTERED SERIAL NUMBER IS PRESENT OR NOT
        cursor = conn.execute(
            "SELECT sl_num FROM {} WHERE sl_num=?".format(table_name), (sl_num,))
        result = cursor.fetchone()  # Retrieve the row
        if result is not None:
            # Access the value
            serial = int(result[0])
        else:
            # Handle the case when no row is found
            serial = None

        # HANDLE CASE WHEN ENTERED SERIAL NUMBER IS NOT PRESENT
        if serial == None:
            print("Sl_num: ", sl_num, " not found!")

        # HANDLE CASE WHEN ENTERED SERIAL NUMBER IS PRESENT
        else:
            # particur input
            particulars = input("Enter update particular: ")
            # done status input
            done = input("Enter yes or no: ")

            # execute update query
            conn.execute('''
                UPDATE {} SET Particulars=?,
                yesOrno=? WHERE sl_num=?
                '''.format(table_name), (particulars, done, sl_num,))
            print("Done!")
            conn.commit()
            conn.close()

    # handle errors
    except sqlite3.OperationalError as err:
        print(err)


def update_values_ei_tank_specification():  # FUNCTION TO UPDATE VALUES FROM EXTERNAL INSPECTION TABLE
    print("UPDATE EXTERNAL INSPECTION TANK SPECIFICATION TABLE DATA THROUGH TANK NUMBER")

    # tank number input
    tank_num = input("Enter tank number: ")

    # EXECUTE UPDATE QUERY WITH ERROR HANDLER
    try:
        # CHECH WHETHER ENTERED TANK NUMBER IS PRESENT OR NOT IN DATABASE
        cursor = conn.execute(
            "SELECT Tank_num FROM ei_tank_specification WHERE Tank_num=?", (tank_num,))
        result = cursor.fetchone()  # Retrieve the row
        if result is not None:
            # Access the value
            tank = result[0]
        else:
            # Handle the case when no row is found
            tank = None

        # HANDLE CASE WHEN ENTERED TANK NUMBER IS NOT PRESENT
        if tank == None:
            print("Tank number: ", tank_num, " not found!")

        # HANDLE CASE WHEN ENTERED TANK NUMBER IS PRESENT
        else:
            # location input
            location = input("Enter update location: ")
            # service input
            service_fluid = input("Enter update service fluid: ")
            # capacity input
            capaity = float(input("Enter tank capacity in kL: "))
            # diameter input
            dia = float(input("Enter tank diameter in meter: "))
            # height input
            height = float(input("Enter height in meter: "))
            # tank type input
            tank_type = input("Enter update tank type: ")
            # last inspection date input
            lid = input("Enter update last inspection date: ")
            # current inspection date input
            cid = input("Enter current inspection date: ")

            # execute update query
            conn.execute('''
                UPDATE ei_tank_specification SET Location=?,
                Service_fluid=?, Capacity=?, Diameter=?, Height=?,
                 Tank_type=?,Last_inspection_date=?,
                Current_inspection_date=? WHERE Tank_num=?
                ''', (location, service_fluid, capaity, dia, height, tank_type, lid, cid, tank_num,))
            print("Done!")
            conn.commit()
            conn.close()

    # handle errors
    except sqlite3.OperationalError as err:
        print(err)
