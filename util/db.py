import sqlite3

def get_cursor(db_filename='util/users.db'):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    return [db, c]

def get_dbc(db_filename='util/users.db'):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    return [db, c]

def execute_command(command, params):
    dbc = get_dbc()
    c = dbc[1]
    r = c.execute(command, params)
    dbc[0].commit()
    return r

def get_current_number(): #Makes sure the id is the last used id+1
    comm = "SELECT MAX(id) FROM company"
    r = execute_command()

def add_company(id, name, email, password, info):
    comm = "INSERT INTO company VALUES (?, ?, ?, ?, ?)"
    params = (id, name, email, password, info)
    execute_command(comm, params)

def create_table():
    c = get_cursor()[1]
    r = c.execute("SELECT * FROM company")
    for a in r:
        print a

def check_credentials():
    return True

#create_table()
add_company(1, "Shaina", "darthbeep@gmail.com", "pwd", "no")
