import sqlite3
import os

from datetime import datetime

def mk_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'db', 'database.db')#

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filestrack (
            Name TEXT REQUIRED,
            Id TEXT PRIMARY KEY,
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

def add_google(data):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'db', 'database.db')#

    today = datetime.now().strftime('%Y-%m-%d')
    
    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    for name, id_ in data.items():
        cursor.execute('''
            INSERT INTO filestrack (Name, Id, GoogleCloud)
            VALUES (?, ?, ?)
        ''', (name, id_, today))

    connection.commit()
    connection.close()

def sort_data():
    data = read_all()
    
    sort_dict = {
        "GoogleDrive": [],
        "Local": [],
        "Transcripted": [],
        "Finished": [],
    }
    
    for entry in data:
        name, id_, googledrive, local, transcripted, finished = entry
        
        if finished:
            sort_dict["Finished"].append(name)
        elif transcripted:
            sort_dict["Transcripted"].append(name)
        elif local:
            sort_dict["Local"].append(name)
        elif googledrive:
            sort_dict["GoogleDrive"].append(name)
            
    return sort_dict

def filter_download():
    data = read_all()
    
    filter_dict = {}
    
    for entry in data:
        name, id_, googledrive, local, transcripted, finished = entry
        
        if googledrive and not local:
            filter_dict[name] = id_
    
    return filter_dict

def update_download_files(download_file_list):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'db', 'database.db')
    
    today = datetime.now().strftime('%Y-%m-%d')

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()
    
    for name, id_ in download_file_list.items():
        cursor.execute('''
            UPDATE filestrack
            SET Local = ?
            WHERE Id = ?
        ''', (today, id_))

    connection.commit()
    connection.close()

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

def delete():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'db', 'database.db')#

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    cursor.execute('''
        DELETE FROM filestrack
        WHERE Id IN (
            SELECT Id FROM filestrack
            ORDER BY Id DESC
            LIMIT 6
        );
    ''')

    connection.commit()
    connection.close()

# delete()