import sqlite3
conn = sqlite3.connect("database.db")


def update_values_pm_table():  # Function to update pre monsoon table
    print("UPDATE PRE MONSOON TABLE DATA TROUGH SERIAL NUMBER")
    table_name = input("Enter table name : ")  # Table name input
    sl_num = input("Enter serial number: ")  # Serial number input

    try:
        # Check whether entered serial number is present or not
        cursor = conn.execute(
            "SELECT sl_num FROM {} WHERE sl_num=?".format(table_name), (sl_num,))
        result = cursor.fetchone()  # Retrieve the row
        if result is not None:
            # Access the value
            serial = int(result[0])
        else:
            # Handle the case when no row is found
            serial = None

        # Handle case if entered serial number is not present
        if serial == None:
            print("Sl_num: ", sl_num, " not found!")

        # Handle case if entered serial number is present
        else:
            # Particualar input
            particulars = input("Enter update particular: ")
            # Completion status input
            completed = input("Enter update completion: ")
            comments = input("Enter update comment: ")  # Comment input

            # Update Query execution
            conn.execute('''
                UPDATE {} SET Particulars=?,
                Completed=?, comments=? WHERE sl_num=?
                '''.format(table_name), (particulars, completed, comments, sl_num,))
            print("Done!")
            conn.commit()
            conn.close()

    # Handle errors
    except sqlite3.OperationalError as err:
        print(err)


def update_values_pm_tank_specification():  # Function to update pre monsoon tank specification table
    print("UPDATE PRE MONSOON TANK SPECIFICATION TABLE DATA THROUGH TANK NUMBER")
    tank_num = input("Enter tank number: ")  # tank name input

    # Execute
    try:
        # Check if entered table name is present or not
        cursor = conn.execute(
            "SELECT Tank_num FROM pre_monsoon_tank_specification WHERE Tank_num=?", (tank_num,))
        result = cursor.fetchone()  # Retrieve the row
        if result is not None:
            # Access the value
            tank = result[0]
        else:
            # Handle the case when no row is found
            tank = None

        # Handle case if entered table name is not found
        if tank == None:
            print("Tank number: ", tank_num, " not found!")
        # Handle case if entered table name is found
        else:
            location = input("Enter update location: ")  # Location Input
            # Service fluid input
            service_fluid = input("Enter update service fluid: ")
            # Capacity input
            capaity = float(input("Enter tank capacity in kL: "))
            # Diameter input
            dia = float(input("Enter tank diameter in meter: "))
            # Height input
            height = float(input("Enter height in meter: "))
            # Tank type input
            tank_type = input("Enter update tank type: ")
            # last inspection date input
            lid = input("Enter update last inspection date: ")
            # current inspection date input
            cid = input("Enter current inspection date: ")

            # Execute Update query
            conn.execute('''
                UPDATE pre_monsoon_tank_specification SET Location=?,
                Service_fluid=?, Capacity=?, Diameter=?, Height=?,
                 Tank_type=?,Last_inspection_date=?,
                Current_inspection_date=? WHERE Tank_num=?
                ''', (location, service_fluid, capaity, dia, height, tank_type, lid, cid, tank_num,))
            print("Done!")
            conn.commit()
            conn.close()

    # Handle error
    except sqlite3.OperationalError as err:
        print(err)
