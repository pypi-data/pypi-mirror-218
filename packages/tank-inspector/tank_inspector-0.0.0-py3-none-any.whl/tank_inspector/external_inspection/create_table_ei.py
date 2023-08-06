import sqlite3
conn = sqlite3.connect("database.db")


def create_ei_table():  # FUNCTION TO CREATE EXTERNAL INSPECTION TABLE
    print("CREATING ANNUAL EXTERNAL TANK INSPECTION TABLE ")
    print("[NOTE: external inspection is denoted as 'ei' ]")
    print('')
    print("Recommend to write as: ei_<tank_number> to avoid name conflict!")
    table_name = str(input("Enter EI table name: "))  # Table name input

    # CHECK WHETHER THE PARTICULAR TABLE IS EXISTED IN THE DATABASE
    cursor = conn.cursor()
    # Execute a query to check if the table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    # Fetch the result
    result = cursor.fetchone()

    # HANDLE CASE WHEN TABLE IS ALREADY EXISTED
    if result is not None:
        print("Table already existed!")

    else:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS {} (
            sl_num REAL PRIMARY KEY,
            Particulars TEXT,
            yesORno TEXT
            )
            '''.format(table_name))
        print("A EI table :", table_name,
              " with entries sl_number, Particulars and yesORno is created successfully!")
        conn.close()


def create_ei_tank_specification():  # FUNCTION TO CREATE EXTERNAL INSPECTION TANK SPECIFICATION TABLE

    # Execute Create table Query
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ei_tank_specification (
        Location TEXT,
        Tank_num TEXT PRIMARY KEY,
        Service_fluid TEXT,
        Capacity REAL,
        Diameter REAL,
        Height REAL,
        Tank_type TEXT,
        Last_inspection_date TEXT,
        Current_inspection_date TEXT
        )
        ''')

    # CONFIMATION PRINT
    print("The EI table : 'ei_tank_specification' with entries Location ,"
          " Tank_num, Service_fluid, Capacity, Diameter, Height,"
          "Tank_type, Last_inspection_date, Current_inspection_date is created successfully! ")
