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
            Id TEXT REQUIRED,
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
    ''')
    
    result = cursor.fetchall()

    connection.commit()
    connection.close()
    
    return result

def read_google():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'db', 'database.db')#

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    cursor.execute('''
        SELECT Name, Id, GoogleCloud FROM filestrack WHERE GoogleCloud IS NOT NULL
    ''')
    
    result = cursor.fetchall()

    connection.commit()
    connection.close()
    
    return result

def add_test():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'db', 'database.db')#

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO filestrack (Name, Id, GoogleCloud, Local, Transcripted, Finished) VALUES
        ('Name5', 12349, '', '2024-09-09', '', '2024-10-08'),
        ('Name6', 12350, '', '2024-09-09', '2024-09-09', ''),
        ('Name7', 12351, '', '2024-09-09', '', ''),
        ('Name8', 12352, '2024-09-08', '2024-09-09', '', '')
    ''')

    connection.commit()
    connection.close()