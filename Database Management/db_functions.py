import numpy as np
from time import perf_counter
from os import getcwd
from sqlite3 import connect, Error
# modules imported

id_to_table_name = { 0:'up', 1:'left', 2:'right', 3:'down'}

# Write your code below
def createConnection( db_file):
    """ create a database connection to a SQLite database and returns it    """
    conn = None
    try:
        conn = connect( db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def createTable( db_dir, table_name, func, if_id= False):
    """ create a table in a database\n
    takes in the directory of the database and the name of the table to be created\n
    this table is specific to the current IP detection array\n
    func decides what type of table you want to create - vehicles or time\n
    Returns the column names of the table as a list. 
    """
    if if_id:
        table_name = id_to_table_name[table_name]

    try:
        # creating connection
        conn = createConnection( db_dir)

        # thinking that latest data will be at the last so no other values
        if func == 'vehicle':
            create_table_sql = """CREATE TABLE IF NOT EXISTS {}(
                id INTEGER PRIMARY KEY,  
                car INTEGER,
                motorcycle INTEGER,
                bus INTEGER,
                truck INTEGER,
                person INTEGER,
                bicycle INTEGER,
                traffic_light INTEGER);""".format( table_name)

        elif func == 'time':
            create_table_sql = 'CREATE TABLE IF NOT EXISTS '+table_name+'( id INTEGER PRIMARY KEY, time REAL);'

        # creating table
        conn.execute(create_table_sql)
        print("table created")
        conn.commit()

        # closing connection
        conn.close()

    except Error as e:
        print(e)
    
    # closing connection
    conn.close()

    if func == 'vehicle':
        return ['id', 'car', 'motorcycle', 'bus', 'truck', 'person', 'bicycle', 'traffic_light']
    
    elif func == 'time':
        return ['id', 'time']


def insertData( db_dir, table_name, data, func, if_id= False):
    """
    Inserts data into the data table\n
    db_dir contains the directory of the database\n
    table name is the name of the table you want to store value in\n
    data is the data to be stored in the table \n
    func decides what type of data you want to store - vehicles or time\n
    WARNING:\n
    data should be an array of dimension (7,) for vehicles and (1,) for time\n
    """
    if if_id:
        table_name = id_to_table_name[table_name]

    # creating connection
    conn = createConnection( db_dir)
    cur = conn.cursor()

    # info_dict = {}

    if func == 'vehicle':
        # creating SQL statement
        sql_statement =  'INSERT INTO {}( car, motorcycle, bus, truck, person, bicycle, traffic_light) VALUES(?,?,?,?,?,?,?) '.format( table_name)
        # preparing for the data
      


    elif func=='time':
    # creating SQL statement
        sql_statement = '''INSERT INTO {}(time) VALUES(?)'''.format( table_name)
    
  
    # storing data
    data= data.tolist()
    cur.execute(sql_statement,data)
    conn.commit()

    # closing connection
    conn.close()

    return 'data stored'

def getAllData( db_dir, table_name, if_id= False):
    """
    Gets all the data from the table in the database\n
    db_dir contains the directory of the database\n
    table name is the name of the table you want to get values from\n
    prints all the values one by one\n
    returns the list of the data with each element as the data\n
    """
    if if_id:
        table_name = id_to_table_name[table_name]

    # creating connection
    conn = createConnection( db_dir)
    cur = conn.cursor()

    # getting all data
    cur.execute('SELECT * FROM {}'.format( table_name))

    data_point = 0
    ret_data = []

    # looping over the data
    while data_point != None:

        # taking one point out
        data_point = cur.fetchone()

        # adding value to return list if data is present
        if data_point != None:
            ret_data.append( data_point[1:])
        else:
            break 
    
    #closing connection
    conn.close()

    return ret_data

def getLastPoint( db_dir, table_name, if_id= False):
    """
    db_dir contains the directory of the database\n
    table name is the name of the table you want to get value from\n
    returns the last point of the data from the database\n
    """
    if if_id:
        table_name = id_to_table_name[table_name]

    # creating connection
    conn = createConnection( db_dir)
    cur = conn.cursor()

    # getting all data
    cur.execute('''SELECT * FROM {0} WHERE id = ( SELECT MAX(id) FROM {0})'''.format( table_name))
    # sql_statement = '''SELECT * FROM {}  
    #                 ORDER BY column_name DESC  
    #                 LIMIT 1;  '''.format( )

    data_point = 0

    data_point = cur.fetchone()  
    
    #closing connection
    conn.close()

    if data_point != None:
        return data_point[1:]

    else:
        print( 'no data present')
        return None
        
    



