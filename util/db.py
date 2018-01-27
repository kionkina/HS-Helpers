import sqlite3
from hashlib import sha1

def get_cursor(db_filename='util/users.db'):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    return [db, c]

def get_dbc(db_filename='util/users.db'):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    return [db, c]

def execute_command(command):
    dbc = get_dbc()
    c = dbc[1]
    r = c.execute(command)
    dbc[0].commit()
    return r

def execute_param_command(command, params):
    dbc = get_dbc()
    c = dbc[1]
    r = c.execute(command, params)
    dbc[0].commit()
    return r

def get_current_number(): #Makes sure the id is the last used id+1
    comm = "SELECT MAX(id) FROM company"
    r = execute_command(comm,)
    for i in r:
        return i[0]+1

def add_company(name, email, password, info=""):
    comm = "INSERT INTO company VALUES (?, ?, ?, ?, ?)"
    id = get_current_number()
    hashed_password = sha1(password).hexdigest()
    params = (id, name, email, hashed_password, info)
    execute_param_command(comm, params)

def create_table():
    c = get_cursor()[1]
    r = c.execute("SELECT * FROM company")
    for a in r:
        print a

def print_table():
    comm = "SELECT * FROM company"
    r = execute_command(comm)
    for thing in r:
        print thing

def check_credentials(username, password):
    hashed_password = sha1(password).hexdigest()
    comm = "SELECT * FROM company WHERE name=? AND password=?"
    r = execute_param_command(comm, (username, hashed_password))
    for thing in r:
        return True
    return False
#create_table()
#add_company("Shaina4", "darthbeep@gmail.com", "pwd", "no")
#print_table()
#print check_credentials("Shaina4", "pwd")
