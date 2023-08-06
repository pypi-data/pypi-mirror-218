import sqlite3
conn = sqlite3.connect("database.db")


def insert_values_pm_table():  # Function to insert values at pre monsoon table

    table_name = input("Enter table name: ")  # Table name input

    # Execute INSERT query with try and except error handle
    try:
        cursor = conn.cursor()

        # Execute a query to check if the table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()  # Fetch the result

        # Handle case if particular table exists
        if result is not None:
            sl_num = input("Enter serial number: ")  # serial number input
            particulars = input("Particular : ")  # particular input
            completed = input("Completed: ")  # complete status input
            comments = input("Comment: ")  # comments input
            conn.execute('''
                INSERT INTO {}(sl_num,
                Particulars,Completed,Comments) VALUES(?,?,?,?)
                '''.format(table_name), (sl_num, particulars, completed, comments))
            print("Done!")
            conn.commit()
            conn.close()
        # Handle case if particular table not exists
        else:
            print("No such table found!")

    except ValueError:
        print("Invalid Entry!")
    except sqlite3.OperationalError as er:
        print("there is no table to enter these data!", str(er))
    except sqlite3.IntegrityError:
        print("Similar serial number Is Not Allowed!")


def insert_values_pm_tank_specification():  # Function to insert values at pre monsoon specification table

    # Execute INSERT query with try and except error handler
    try:
        loc = input("Location: ")  # location input
        tank_num = input("Enter Tank number: ")  # tank number input
        service_fluid = input("Service fluid : ")  # service fluid input
        capaity = float(input("Enter tank capacity in kL: "))  # capacity input
        dia = float(input("Enter tank diameter in meter: "))  # diameter input
        height = float(input("Enter height in meter: "))  # height input
        tank_type = input("Tank type: ")  # tank type input
        lid = input("Last Inspection Date: ")  # last inspection date input
        # current inspection date input
        cid = input("Current Inspection Date: ")

        conn.execute('''
            INSERT INTO pre_monsoon_tank_specification(
            Location,
            Tank_num,
            Service_fluid,
            Capacity,
            Diameter,
            Height,
            Tank_type,
            Last_inspection_date,
            Current_inspection_date) VALUES(?,?,?,?,?,?,?,?,?)
            ''', (loc, tank_num, service_fluid, capaity, dia, height, tank_type, lid, cid))
        print("Done!")
        conn.commit()
        conn.close()

    # Handle error
    except ValueError:
        print("Invalid Entry!")
    except sqlite3.OperationalError as er:
        print("there is no table to enter these data!", str(er))
    except sqlite3.IntegrityError:
        print("Similar Tank number Is Not Allowed!")
