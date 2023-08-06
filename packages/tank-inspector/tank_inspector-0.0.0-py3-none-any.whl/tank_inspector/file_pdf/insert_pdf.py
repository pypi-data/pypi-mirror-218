import sqlite3
conn = sqlite3.connect("database.db")


def insert_pdf():  # FUNCTION TO INSERT A PDF FILE TO PDF TABLE

    # EXECUTE INSERT QUERY WITH ERROR HANDLER
    try:
        # file name input
        file_name = input("Enter pdf file name: ")

        # Read pdf
        with open(file_name, 'rb') as file:
            pdf_data = file.read()

        # execute insert query
        conn.execute('''    
                INSERT INTO pdf_table (Name, data) VALUES(?,?)
            ''', (file_name, pdf_data))
        print("Data inserted at pdf_table succesfully!")
        conn.commit()
        conn.close()
    except FileNotFoundError:
        print("No such file or directory: ", file_name)
    except sqlite3.OperationalError as err:
        print(err)
