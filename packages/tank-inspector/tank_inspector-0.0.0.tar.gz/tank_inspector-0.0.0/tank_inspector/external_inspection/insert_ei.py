import sqlite3
conn = sqlite3.connect("database.db")


def insert_values_ei_table():  # FUNCTION TO INSERT VALUES IN EXTERNAL INSPECTION TABLE

    # table name input
    table_name = input("Enter table name: ")

    # EXECUTE INSERT QUERY WITH ERROR HANDLER
    try:
        # CHECK WHETHER ENTERED TABLE NAME IS EXISTED IN DATABASE
        cursor = conn.cursor()
        # Execute a query to check if the table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        # Fetch the result
        result = cursor.fetchone()

        # HANDLE CASE WHEN TABLE NAME IS FOUND
        if result is not None:
            sl_num = input("Enter serial number: ")
            particulars = input("Particular : ")
            done = input("Enter yes or no : ")
            conn.execute('''
                INSERT INTO {}(sl_num,
                Particulars,yesORno) VALUES(?,?,?)
                '''.format(table_name), (sl_num, particulars, done))
            print("Done!")
            conn.commit()
            conn.close()

        # HANDLE CASE WHEN TABLE IS NOT FOUND
        else:
            print("No such table found!")

    # HANDLE ERROR
    except ValueError:
        print("Invalid Entry!")
    except sqlite3.OperationalError as er:
        print("there is no table to enter these data!", str(er))
    except sqlite3.IntegrityError:
        print("Similar serial number Is Not Allowed!")


# FUNCTION TO INSERT VALUES IN EXTERNAL INSPECTION SPECIFICATION TABLE
def insert_values_ei_tank_specification():

    # EXECUTE INSERT QUERY WITH ERROR HANDLER
    try:
        # location input
        loc = input("Location: ")
        # tank number input
        tank_num = input("Enter Tank number: ")
        # service fluid input
        service_fluid = input("Service fluid : ")
        # capacity input
        capaity = float(input("Enter tank capacity in kL: "))
        # diameter input
        dia = float(input("Enter tank diameter in meter: "))
        # height input
        height = float(input("Enter height in meter: "))
        # tank type input
        tank_type = input("Tank type: ")
        # last inspection date input
        lid = input("Last Inspection Date: ")
        # current inspection date input
        cid = input("Current Inspection Date: ")

        # execute insert query
        conn.execute('''
            INSERT INTO ei_tank_specification(
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

    # HANDLE ERROR
    except ValueError:
        print("Invalid Entry!")
    except sqlite3.OperationalError as er:
        print("there is no table to enter these data!", str(er))
    except sqlite3.IntegrityError:
        print("Similar Tank number Is Not Allowed!")
