#!/usr/bin/env python2
"""
    create_database.py

    Creates the initial database for image hashing.

    :author: Brandon Arrendondo
    :author: James Jenkins
    :license: MIT
"""
import sys
import argparse

from db import hash_db


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbfilepath", default="hashdb.sqlite",
                        help="Filepath of the database to create.")
    args = parser.parse_args()

    db_conn = hash_db.db_open(args.dbfilepath)
    hash_db.reset_db(db_conn)
    print "Initial empty database created."


if __name__ == "__main__":
    main(sys.argv[1:])
