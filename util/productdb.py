import sqlite3
from hashlib import sha1

def get_cursor(db_filename='util/product.db'):
    db = sqlite3.connect(db_filename)
    c = db.cursor()
    return [db, c]

def get_dbc(db_filename='util/product.db'):
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
    comm = "SELECT MAX(productid) FROM product"
    r = execute_command(comm,)
    try:
        for i in r:
            return i[0]+1
    except:
        return 0

def add_product(price, productid, quantity, productname, username, company, time):
    comm = "INSERT INTO product VALUES (?, ?, ?, ?, ?, ?, ?)"
    productid = get_current_number()
    params = (price, productid, quantity, productname, username, company, time)
    execute_param_command(comm, params)
    return True

def create_table():
    c = get_cursor()[1]
    r = c.execute("SELECT * FROM product")
    for a in r:
        print a


#create_table()
#add_product(1, "Shaina", "darthbeep@gmail.com", "pwd", "no")

def print_table():
    comm = "SELECT * FROM product"
    r = execute_command(comm)
    for thing in r:
        print thing

def get_tuple_from_name():
    comm = "SELECT info FROM product WHERE name=?"
    r = execute_param_command(comm, [name])
    for thing in r:
        return thing

def get_info(name):
    comm = "SELECT info FROM product WHERE name=?"
    r = execute_param_command(comm, [name])
    for thing in r:
        return thing[0]

def edit_info(name, new_info):
    comm = "UPDATE product SET info=? WHERE name=?"
    execute_param_command(comm, (new_info, name))


#create_table()
#add_product( 19.99, 1, 10, "headphones", "shaina123", "shiana_corps")
#print_table()
