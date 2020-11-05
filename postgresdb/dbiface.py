'''
    Author: Chandra Krintz, UCSB, ckrintz@cs.ucsb.edu, AppScale BSD license
    USAGE: python dbiface.py 169.231.XXX.YYY table_name postgres_user_name password
'''
import psycopg2, sys, argparse, os
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

DEBUG=False

TABLE_TYPE_MAP = {
    'data':""" (dt timestamp PRIMARY KEY, 
        meas real
    )
    """,
    'temphum':""" (dt timestamp PRIMARY KEY, 
        temp real,
        hum real 
    )
    """,
    'status':""" (dt timestamp PRIMARY KEY, 
        TimeStamp timestamp,
        Record bigint,
        OSVersion varchar(32),
        OSSignature real,
        LastSystemScan timestamp,
        PortStatus1 boolean,
    )
    """
}

class DBobj(object):
    '''A postgresql instance object
    Attributes:
        conn: A database connection
    '''

    #constructor of a DBobj object
    #https://www.psycopg.org/docs/connection.html
    def __init__(self, dbname=None, url=None, pwd=None, host='localhost',user='postgres'):
        if not url: #sanity check
            if not dbname and not pwd:
                raise Exception("Either url parameter {} or dbname and pwd must be set (dbname='{}')".format(url,dbname))

        if url is not None:
            args = url
        else:
            args = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbname,user,host,pwd)

        try: 
            self.args = args
            self.conn = psycopg2.connect(args)
        except Exception as e:
            print(e)
            print('Problem connecting to DB')
            sys.exit(1)

    #reset the connection
    #https://www.psycopg.org/docs/connection.html
    def reset(self):
        try:
            self.conn = psycopg2.connect(self.args)
        except Exception as e:
            print(e)
            print('Problem connecting to DB in reset')
            sys.exit(1)
    
    #return the cursor
    #https://www.psycopg.org/docs/connection.html#connection.cursor
    def get_cursor(self,svrcursor=None):
        if svrcursor:
            return self.conn.cursor(svrcursor)
        return self.conn.cursor()

    #commit the changes to the db
    #https://www.psycopg.org/docs/connection.html
    def commit(self):
        if self.conn:
            self.conn.commit()

    #see if table exists, return True else False
    #https://www.psycopg.org/docs/connection.html#connection.cursor
    def table_exists(self,tablename): 
        curs = self.conn.cursor()
        curs.execute("select exists(select * from information_schema.tables where table_name=%s)", (tablename,))
        val = curs.fetchone()[0]
        return val

    #create a table
    #https://www.psycopg.org/docs/connection.html#connection.cursor
    def create_table(self,typename,tablename):
        curs = self.conn.cursor()
        typestring = TABLE_TYPE_MAP[typename]
        if typestring is None:
            print('Error: unable to create table {0}, no types in typemap: {1}'.format(tablename,TABLE_TYPE_MAP))
            return False
        try:
            curs.execute("DROP TABLE IF EXISTS {0}".format(tablename))
            curs.execute("CREATE TABLE {0} {1}".format(tablename,typestring))
        except Exception as e:
            print(e)
            print('Error: unable to create table {0}, in exceptional case. Type: \n{1}'.format(tablename,typestring))
            return False
        self.conn.commit()
        return True


    #delete a table
    #https://www.psycopg.org/docs/connection.html#connection.cursor
    def rm_table(self,tablename):
        curs = self.conn.cursor()
        try:
            curs.execute("DROP TABLE {0}".format(tablename))
        except:
            pass
        self.conn.commit()


    #invoke an SQL query on the db
    #https://www.psycopg.org/docs/connection.html#connection.cursor
    #https://intellipaat.com/mediaFiles/2019/02/SQL-Commands-Cheat-Sheet.pdf
    def execute_sql(self,sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            print('execute_sql: SQL problem:\n\t{0}'.format(sql))
            sys.exit(1)
        return cur

    #close the DB connection
    #https://www.psycopg.org/docs/connection.html#connection.cursor
    def closeConnection(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

def main():
    parser = argparse.ArgumentParser(description='Test a connection to a postgres DB')
    parser.add_argument('--host',action='store', default='localhost', help='DB host IP')
    parser.add_argument('--db',action='store', default='cs148db', help='DB name')
    parser.add_argument('--user',action='store', default='centos', help='postgres user name')
    parser.add_argument('--tablename',action='store', default='testtable', help='tablename: to create')
    parser.add_argument('--removetable',action='store_true', default=False, help='Use this to delete table when done')
    parser.add_argument('pwd',action='store',help='postgres user password')
    args = parser.parse_args()
    
    #test connectivity to the DB by getting the version
    db = DBobj(dbname=args.db,pwd=args.pwd,host=args.host,user=args.user)
    sql = 'SELECT version()'
    cur = db.execute_sql(sql)
    ver = cur.fetchone()
    print('Postgres version test using the names passed in on the command line: {}'.format(ver))

    #test connectivity using the DB URL environment variable
    url = os.getenv('DATABASE_URL') #returns None if non-existent key name
    if url:
        db = DBobj(url=url)
        sql = 'SELECT version()'
        cur = db.execute_sql(sql)
        ver = cur.fetchone()
        print('Postgres version test using DATABASE_URL environment variable, if set: {}'.format(ver))
    else: 
        print("DATABASE_URL is not set...")

    #create, write, and read from tablename
    tablename = args.tablename
    table_exists = db.table_exists(tablename)
    print('Does the table already exist (True=Yes)? {}'.format(table_exists))

    if not table_exists:
        #this will delete (ie drop) the table if it exists
        retn = db.create_table('data',tablename) #schema, tablename

    cur = db.get_cursor()
    #see TABLE_TYPE_MAP above for data object which specifies schema, must match insert below; returns T/F
    cur.execute("INSERT INTO {0} (dt,meas) VALUES (%s, %s)".format(tablename), [datetime.now(),-1.0])
    cur.execute("INSERT INTO {0} (dt,meas) VALUES (%s, %s)".format(tablename), [datetime.now(),2.0])
    cur.execute("INSERT INTO {0} (dt,meas) VALUES (%s, %s)".format(tablename), [datetime.now(),2.4])
    cur.close()
    db.commit()

    cur = db.get_cursor() #need to do this again because we close it above
    cur.execute("SELECT * from {}".format(tablename))
    rows = cur.fetchall()
    print("All data found in table {}:".format(tablename))
    for row in rows:
        print(row)
    
    if args.removetable:
        print("removing table {}".format(tablename))
        db.rm_table(tablename)
    db.closeConnection()

if __name__ == '__main__':
    main()
