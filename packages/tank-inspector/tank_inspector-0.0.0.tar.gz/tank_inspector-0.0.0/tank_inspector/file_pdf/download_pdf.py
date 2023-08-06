import sqlite3
conn = sqlite3.connect("database.db")


def download_pdf():  # FUNCTION TO DOWNLOAD A PDF

    # EXECUTE WITH ERROR HANDLERS
    try:
        # file name input
        file_name = input("Enter file name: ")

        # check whether entered file is present or not in table
        result = conn.execute(
            "SELECT data FROM pdf_table WHERE Name=?", (file_name,))
        row = result.fetchone()

        # HANDLE CASE WHEN FILE IS PRESENT
        if row is not None:
            pdf_data = row[0]
            with open(file_name, 'wb') as file:
                file.write(pdf_data)  # download pdf file
            print("Download successful!")

        # HANDLE CASE WHEN FILE IS NOT PRESENT
        else:
            print(f"No pdf name '{file_name}' found!")
        conn.close()
    except sqlite3.OperationalError as err:
        print(err)
