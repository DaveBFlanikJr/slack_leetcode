import argparse
import os
from contextlib import contextmanager
from service.db.db_service import get_database, logger

'''This file will be used to handle commands needed to 
        - Init the db 
        - drop the db 
        - reset the db 
'''
@contextmanager
def database_context():
    with get_database() as db:
        if db:
            yield db
        else:
            logger.error("Failed to connect to the database.")

    # Command to initalize the db
def initialize_db():
    with database_context() as db:
        db.init_db()

# Command to drop the db 
def drop_db():
    with database_context() as db:
        db.drop_table()

# Command to reset the db
def reset_db():
    with database_context() as db:
        db.drop_table()
        db.init_db()

def run_service():
    parser = argparse.ArgumentParser(description="Manage your Leetcode database.")
    subparser = parser.add_subparsers(dest="command")

    # Sub parses for init, drop, reset
    subparser.add_parser("init", help="Initialize the database.")
    subparser.add_parser("drop", help="Drop the solutions table.")
    subparser.add_parser("reset", help="Reset the database (drop and initialize).")

    args = parser.parse_args()

    # commands 
    if args.command == "init":
        initialize_db()
    elif args.command == "drop":
        drop_db()
    elif args.command == "reset":
        reset_db()
    else:
        parser.print_help()

if __name__ == "__main__":
    if not os.getenv("DATABASE_URL"):
        logger.error("Please set the DATABASE_URL environment variable.")
        exit(1)
    run_service()