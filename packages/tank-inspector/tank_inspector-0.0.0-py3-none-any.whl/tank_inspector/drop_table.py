import sqlite3
conn = sqlite3.connect("database.db")


def drop_table():  # Function to drop table

    # Execute Drop Table execute with try except error handler
    try:
        # table name input
        table_name = input("Enter a table name to be dropped: ")

        # Execute Drop Table Query
        conn.execute('''
            DROP TABLE {}
            '''.format(table_name))
        print(table_name, " dropped successfully!")
        conn.commit()
        conn.close()

    # Handle error
    except sqlite3.OperationalError as err:
        print(err)
