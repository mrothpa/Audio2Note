import sqlite3
import os


def mk_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'db', 'database.db')#

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filestrack (
            Name TEXT PRIMARY KEY,
            GoogleCloud DATE,
            Local DATE,
            Transcripted DATE,
            Finished DATE
        );
    ''')

    connection.commit()
    connection.close()
    
def read_all():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'db', 'database.db')#

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM filestrack
        );
    ''')
    
    result = cursor.fetchall()

    connection.commit()
    connection.close()
    
    return result