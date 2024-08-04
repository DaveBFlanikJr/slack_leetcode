from logging import getLogger
import sqlalchemy
from attrs import define, field
import os

# Logger
logger = getLogger(__name__)

# Define the table for the leetcode problems 
@define
class DatabaseBuilder:
    #Define instance variables 
    database_url: str
    engine: sqlalchemy.engine.base.Engine = field(init=False)
    metadata: sqlalchemy.MetaData = field(init=False)
    solutions: sqlalchemy.Table = field(init=False)

    # constructor method
    def __attrs_post_init__(self):
        self.engine = sqlalchemy.create_engine(self.database_url)
        self.metadata = sqlalchemy.MetaData()
        self.solutions = sqlalchemy.Table(
            "solutions",
            self.metadata,
            sqlalchemy.Column("problem_number", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("problem_name", sqlalchemy.String, nullable=False),
            sqlalchemy.Column("code", sqlalchemy.String, nullable=False)
        )

    # initalize the db
    def init_db(self):
        logger.info("Initializing DB.")
        try:
            self.metadata.create_all(self.engine)
            logger.info("DB initialized successfully.")
        except Exception as e:
            logger.info(f"Error initializing DB: {e}")

    # drop table if needed 
    def drop_table(self):
        logger.info("Dropping solutions table.")
        try:
            self.metadata.drop_all(self.engine, [self.solutions])
            logger.info("Solutions table dropped successfully.")
        except Exception as e:
            logger.error(f"Error dropping solutions table: {e}")

    # Must have a method to create an entry into the db 
    def insert_solution(self, problem_number, problem_name, code):
        logger.info("Inserting solution into the DB")
        # Open connection
        try:
            with self.engine.connect() as conn:
                query = self.solutions.insert().values(
                    problem_number=problem_number,
                    problem_name=problem_name,
                    code=code
                )
                # Execute query 
                conn.execute(query)
                logger.info(f"Solution for problem number {problem_number} inserted successfully.")
        except Exception as e:
            logger.error(f"Error inserting solution: {e}")

    # Must have a method to fetch a entry 
    def fetch_solution(self, problem_number):
        try:
            with self.engine.connect() as conn:
                query = self.solutions.select().where(self.solutions.c.problem_number == problem_number)
                result = conn.execute(query).fetchone()
                if result:
                    logger.info(f"Solution for problem number {problem_number} fetched successfully.")
                    return result['code']
                else:
                    logger.warning(f"No solution found for problem number {problem_number}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching solution: {e}")
            return None

# Get the db
def get_database():
    # pass in the URL for the database
    database_url = os.getenv("DATABASE_URL")
    # Safty check 
    if not database_url:
        logger.error("DATABASE_URL environment variable is not set.")
        return
    database = DatabaseBuilder(database_url)
    try:
        yield database
    finally:
        database.engine.dispose()
