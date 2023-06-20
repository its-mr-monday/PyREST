import sqlite3
import os
from PyRest.Exceptions import PyRestException

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_connection(db_file) -> sqlite3.Connection:
    try:
        con = sqlite3.connect(db_file)
        return con
    except Exception as e:
        raise PyRestException(e)
    
def close_connection(con: sqlite3.Connection):
    con.commit()
    con.close()
    
def create_db(path: str, project_name: str):
    #Remove any spaces for _
    project_name = project_name.replace(" ", "_")
    file = os.path.join(path, f"{project_name}_users.db")
    with open(file, "w") as f:
        pass
    con = create_connection(file)
    cur = con.cursor()
    cur.execute('''
                CREATE TABLE PYREST_USERS
                (ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME TEXT, PASSWORD TEXT, REGISTER_DATE INTEGER, LAST_LOGIN INTEGER, OLD_PASSWORD TEXT)''')
    con.commit()
    close_connection(con)
    
def load_db(path: str, project_name: str):
    project_name = project_name.replace(" ", "_")
    file = os.path.join(path, f"{project_name}_users.db")
    
class PyRestDB:
    def __init__(self, project_path: str, project_name: str):
        self.project_path = project_path
        self.project_name = project_name
        