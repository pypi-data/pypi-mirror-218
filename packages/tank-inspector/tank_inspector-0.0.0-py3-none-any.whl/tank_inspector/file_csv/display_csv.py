import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


def display_csv():  # FUCTION TO DISPLAY VALUES FROM A CSV TABLE

    # table name input
    table_name = input("Enter table name: ")

    # EXECUTE SELECT QUERY WITH ERROR HANDLERS
    try:
        # CHECK WHETHER ENTERED TABLE IS EXISTED OR NOT IN DATABASE
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()

        # HANDLE CASE IF TABLE EXISTS
        if result:
            # COLLECT NAME OF FIELDS IN ENTERED TABLE
            # Fetch the column names
            columns_query = f"PRAGMA table_info({table_name})"
            columns_result = conn.execute(columns_query)
            columns = [column[1] for column in columns_result]

            # PRINT FIELD NAME
            print("Field Names: " + ', '.join(columns))

            # ASK USER TO SELECT A FIELD NAME AND PROVIDE A VALUE TO IT
            field_name = input("Select a field from the above: ")
            value = input("Enter a value for the field entered: ")

            # execute search query
            data = conn.execute('''
                    SELECT * FROM {} WHERE {}=?
                '''.format(table_name, field_name), (value,))
            print("")

            # print messege if no value is not present
            print(
                f"[NOTE: IF NO VALUES ARE SHOWN THEN THERE IS NO '{value}' PRESENT IN THE FIELD '{field_name}']")

            # print if value is present
            print(f"Field name: '{field_name}' Value: '{value}' corresponding entries of " + ', '.join(columns) +
                  " are shown below:")
            for d in data:
                print(d)

        # HANDLE CASE WHEN TABLE IS NOT FOUND
        else:
            print(f"table '{table_name}' not found!")

        conn.close()

    # HANDLE ERRORS
    except sqlite3.OperationalError as err:
        print(err)
