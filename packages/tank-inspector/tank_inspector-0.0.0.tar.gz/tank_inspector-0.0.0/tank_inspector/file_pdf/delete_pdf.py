import sqlite3
conn = sqlite3.connect("database.db")


def delete_pdf():  # FUNCTION TO DELETE A PDF FILE FROM PDF TABLE
    print("DELETE A PDF FILE THROUGH ITS NAME")

    # pdf file name input
    pdf_name = input("Enter pdf file name to be deleted: ")

    # EXECUTE DELETE QUERY WITH ERROR HANDLER
    try:
        conn.execute('''
            DELETE FROM pdf_table WHERE Name=?
        ''', (pdf_name,))
        print("Done!")
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as err:
        print(err)
