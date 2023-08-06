import sqlite3
conn = sqlite3.connect("database.db")


def delete_values_pm_table():  # function to delete values from pre monsoon table

    print("DELETE A ROW WITH A PARTICULAR SERIAL NUMBER FROM PRE MONSOON TABLES")
    # Table name input
    table_name = input("Enter table name: ")
    # Serial number input
    sl_num = input("Enter serial number to be deleted: ")

    # Execute Delete query with try and except error handler
    try:
        conn.execute('''
            DELETE FROM {} WHERE sl_num=?
        '''.format(table_name), (sl_num,))
        print("Done!")
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as err:
        print(err)


# funtion to delete values from pre monsoon tank specification table
def delete_values_pm_tank_specification():

    print("DELETE A ROW WITH A PARTICULAR TABLE NUMBER FROM PRE MONSOON TANK SPECIFICATION TABLE")
    tank_num = input("Enter tank number to be deleted: ")  # input tank number

    # execute Delete query with try and except error handler
    try:
        conn.execute('''
            DELETE FROM pre_monsoon_tank_specification WHERE Tank_num=?
        ''', (tank_num,))
        print("Done!")
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as err:
        print(err)
