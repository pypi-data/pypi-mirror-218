import sqlite3
conn = sqlite3.connect("database.db")


def create_pm_table():  # FUNCTION TO CREATE PRE MONSOON TABLE
    print("Recommend to write as: pm_<tank_number> to avoid name conflict!")
    # Table name input
    table_name = str(input("Enter pre monsoon table name: "))

    # CHECK WHETHER THE PARTICULAR TABLE IS EXISTED IN THE DATABASE
    # Establish a connection to the SQLite database
    cursor = conn.cursor()
    # Execute a query to check if the table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    # Fetch the result
    result = cursor.fetchone()

    # HANDLE CASE WHEN PARTICULAR TABLE IS ALREADY EXISTED
    if result is not None:
        print("Table already existed!")

    # HANDLE CASE WHEN PARTICULAR TABLE IS NOT EXISTED
    else:
        # Execute Create Table query
        conn.execute('''
            CREATE TABLE IF NOT EXISTS {} (
            sl_num REAL PRIMARY KEY,
            Particulars TEXT,
            Completed TEXT,
            Comments TEXT
            )
            '''.format(table_name))
        print("A pre monsoon table :", table_name,
              " with entries sl_number, Particulars, Completed and Comments is created successfully!")
        conn.close()


def create_pm_tank_specification():  # FUNCTION TO CREATE PRE MONSOON TANK SPECIFICATION TABLE

    # Execute create table query
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pre_monsoon_tank_specification (
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

    # print Execution Confirmation
    print("The table : 'pre_monsoon_tank_specification' with entries Location ,"
          " Tank_num, Service_fluid, Capacity, Diameter, Height,"
          "Tank_type, Last_inspection_date, Current_inspection_date is created successfully! ")
