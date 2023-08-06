import sqlite3
import csv

conn = sqlite3.connect("database.db")


def table_csv():  # FUNCTION TO CREATE CSV FILES TABLE

    # EXECUTE CREATE TABLE QUERY WITH ERROR HANDLER
    try:
        # file name input
        name = input("Enter CSV file name: ")
        # table name input
        table_name = input("Enter table name: ")

        # Create the table
        create_table_query = f"CREATE TABLE  {table_name} ("
        with open(name, 'r') as file:
            csv_data = csv.reader(file)
            header = next(csv_data)  # Retrieve the header row
            for field in header:
                create_table_query += f"{field} TEXT, "
            # Remove the last comma and space
            create_table_query = create_table_query[:-2]
            create_table_query += ")"
        conn.execute(create_table_query)

        # Insert data into the table
        with open(name, 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)  # Skip the header row if it exists

            insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(header))})"
            conn.executemany(insert_query, csv_data)
        print("Data entered successfully!")
        conn.commit()
        conn.close()

    # handle errors
    except sqlite3.OperationalError as err:
        print(err)
    except FileNotFoundError:
        print("No such file found!")
