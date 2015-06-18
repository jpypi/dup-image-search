"""
    hash_db.py

    Sqlite3 helpers for building up the database that contains mappings between
    a filename and the respective image hash for that filename.

    :author: Brandon Arrendondo
    :license: MIT
"""
import sqlite3
from algorithms.image_utils import hamming_weight


def db_open(db_filepath):
    """
    Returns a db connection to the given database (creates one if not found)
    """
    db_conn = sqlite3.connect(db_filepath)
    return db_conn


def table_exists(db_conn, table_name):
    """
    Checks if a table matching table_name exist in the database
    """
    cur = db_conn.cursor()
    tn = (table_name,)
    cur.execute("select name from sqlite_master where type='table' and name=?", tn)
    result = cur.fetchone()
    if(result):
        return True
    else:
        return False


def drop_if_exists(db_conn, table_name):
    """
    Drops the table having table_name from the database if it exists.
    """
    cur = db_conn.cursor()

    if(table_exists(db_conn, table_name)):
        cur.execute("drop table {0}".format(table_name))


def reset_db(db_conn):
    """
    Removes data from the given DB and recreates the structure only.
    """
    cur = db_conn.cursor()
    drop_if_exists(db_conn, "simple")
    drop_if_exists(db_conn, "dct")

    create_statement = 'create table simple ( "hash" INTEGER PRIMARY KEY NOT NULL UNIQUE'

    create_statement += ', "{0}" INTEGER'.format("hamming_weight")
    create_statement += ', "{0}" TEXT'.format("filename")
    create_statement += ')'
    cur.execute(create_statement)

    create_statement = 'create table dct ( "hash" INTEGER PRIMARY KEY NOT NULL UNIQUE'

    create_statement += ', "{0}" TEXT'.format("filename")
    create_statement += ')'
    cur.execute(create_statement)


def insert_hash(db_conn, type, hash, filename):
    cur = db_conn.cursor()

    if(type == "dct"):
        cur.execute("insert into dct values(?, ?, ?)", (hash,
            hamming_weight(hash), filename))
    elif(type == "simple"):
        cur.execute("insert into simple values(?, ?, ?)", (hash,
            hamming_weight(hash), filename))


def hash_exists(db_conn, type, hash):
    cur = db_conn.cursor()

    if(type == "dct"):
        result = cur.execute("select * from dct where hash=?", (hash, ))
        return cur.fetchone()
    elif(type == "simple"):
        result = cur.execute("select * from simple where hash=?", (hash, ))
        return cur.fetchone()


def get_closest(db_conn, type, hash):
    cur = db_conn.cursor()

    weight = hamming_weight(hash)

    if(type == "dct"):
        result = cur.execute("select * from dct where hamming_weight between {0!s} and {1!s}".format(weight - 5, weight + 5))
        return cur
    elif(type == "simple"):
        result = cur.execute("select * from simple where hamming_weight between {0!s} and {1!s}".format(weight - 5, weight + 5))
        return cur
