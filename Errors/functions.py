import numpy as np
from time import perf_counter
from os import getcwd
import sqlite3 as sql 
# modules imported

# Write your code below
def createConnection( db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sql.connect( db_file)
        return conn
    except sql.Error as e:
        print(e)

    return conn


def createTable( db_dir, table_name, func):
    """ create a table in a database\n
    takes in the directory of the database and the name of the table to be created\n
    this table is specific to the current IP detection array\n
    Returns the column names of the table as a list. 
    """
    try:
        # creating connection
        conn = createConnection( db_dir)

        # thinking that latest data will be at the last so no other values
        if func == 'vehicle':
            create_table_sql = """CREATE TABLE IF NOT EXISTS {}(
                id INTEGER PRIMARY KEY UNIQUE,  
                car INTEGER,
                motorcycle INTEGER,
                bus INTEGER,
                truck INTEGER,
                person INTEGER,
                bicycle INTEGER,
                traffic_light INTEGER);""".format( table_name)

        elif func == 'time':
            create_table_sql = 'CREATE TABLE IF NOT EXISTS {}( id INTEGER PRIMARY KEY UNIQUE, time REAL);'.format( table_name)

        # creating table
        conn.execute(create_table_sql)
        print("table created")

        # closing connection
        conn.close()

    except sql.Error as e:
        print(e)
    
    # closing connection
    conn.close()

    if func == 'vehicle':
        return ['id', 'car', 'motorcycle', 'bus', 'truck', 'person', 'bicycle', 'traffic_light']
    
    elif func == 'time':
        return ['id', 'time']


def insertData( db_dir, table_name, data, func):
    """
    Inserts data into the data table\n
    db_dir contains the directory of the database\n
    table name is the name of the table you want to store value in\n
    data is the data to be stored in the table \n
    WARNING:\n
    data should be an array of dimension (1,7)\n
    """
    # creating connection
    conn = createConnection( db_dir)
    cur = conn.cursor()

    info_dict = {}

    if func == 'vehicle':
        # creating SQL statement
        sql_statement = ''' INSERT INTO {} ( car, motorcycle, bus, truck, person, bicycle, traffic_light)
                VALUES( :car, :motorcycle, :bus, :truck, :person, :bicycle, :traffic_light) '''.format( table_name)
        # preparing for the data
        col_names = [ 'car', 'motorcycle', 'bus', 'truck', 'person', 'bicycle', 'traffic_light']


    elif func == 'time':
        # creating SQL statement
        sql_statement = ''' INSERT INTO {} ( time)
                VALUES(:time) '''.format( table_name)
        col_names = [ 'time']

    
    for col, val in zip( col_names, data):
        info_dict.update( { col: val})

    # storing data
    cur.execute(sql_statement, info_dict)
    print( 'data stored')

    # closing connection
    conn.close()

    return None

def getAllData( db_dir, table_name):
    # creating connection
    conn = createConnection( db_dir)

    # getting all data
    conn.execute('select * from {} LIMIT 1'.format( table_name))
    cur = conn.cursor()

    b = 0

    while b!=None:
        b = cur.fetchone()

        if b != None:
            return b 
        else:
            print( 'no data left')
            break 
    
    #closing connection
    conn.close()

    return None


