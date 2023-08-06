import sqlite3
conn = sqlite3.connect("database.db")


def create_table_pdf():  # FUNCTION TO CREATE PDF FILE TABLE

    # execute create table query
    # table name is not user provide and is defined as pdf_table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pdf_table (
        sl_num INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Data BLOB
        )
        ''')
    print("pdf_table created successfully!")
    conn.close()
