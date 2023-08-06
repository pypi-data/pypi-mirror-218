import sqlite3
conn = sqlite3.connect("database.db")


def delete_values_ei_table():  # FUNCTION TO DELETE VALUES FROM EXTERNAL INSPECTION TABLE
    print("DELETE A ROW WITH A PARTICULAR SERIAL NUMBER FROM EXTERNAL INSPECTION TABLES")

    # table name input
    table_name = input("Enter table name: ")
    # serial number input
    sl_num = input("Enter serial number to be deleted: ")

    # Execute Delete query with error handler
    try:
        conn.execute('''
            DELETE FROM {} WHERE sl_num=?
        '''.format(table_name), (sl_num,))
        print("Done!")
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as err:
        print(err)


# FUNCTION TO DELETE VALUES FROM EXTERNAL INSPECTION SPECIFICATION TABLE
def delete_values_ei_tank_specification():
    print("DELETE A ROW WITH A PARTICULAR TABLE NUMBER FROM EXTERNAL INSPECTION TANK SPECIFICATION TABLE")

    # enter tank name
    tank_num = input("Enter tank number to be deleted: ")
    try:
        # execute delete query
        conn.execute('''
            DELETE FROM ei_tank_specification WHERE Tank_num=?
        ''', (tank_num,))
        print("Done!")
        conn.commit()
        conn.close()

    # handle error
    except sqlite3.OperationalError as err:
        print(err)
