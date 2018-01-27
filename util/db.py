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
    return True

def create_table():
    c = get_cursor()[1]
    r = c.execute("SELECT * FROM company")
    for a in r:
        print a


def check_credentials(username, password):
    return True

#create_table()
#add_company(1, "Shaina", "darthbeep@gmail.com", "pwd", "no")

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

def is_username_used(username):
    comm = "SELECT * FROM company WHERE name=?"
    r = execute_param_command(comm, [username])
    for thing in r:
        return True
    return False

def get_info(name):
    comm = "SELECT info FROM company WHERE name=?"
    r = execute_param_command(comm, [name])
    for thing in r:
        return thing[0]

def edit_info(name, new_info):
    comm = "UPDATE company SET info=? WHERE name=?"
    execute_param_command(comm, (new_info, name))

#print is_username_used('Shaina')
#create_table()
#add_company("Shaina4", "darthbeep@gmail.com", "pwd", "no")
#edit_info("Shaina", "Updated info")
#print_table()
#print check_credentials("Shaina4", "pwd")
print get_info("Shaina")
