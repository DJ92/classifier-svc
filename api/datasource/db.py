import MySQLdb
import os


def connect():
    """ https://mysqlclient.readthedocs.io/user_guide.html#mysqldb """
    return MySQLdb.connect(host=os.environ['MYSQL_HOST'],
                           user=os.environ['MYSQL_USER'],
                           password=os.environ['MYSQL_ROOT_PASSWORD'],
                           database=os.environ['MYSQL_DATABASE'])
