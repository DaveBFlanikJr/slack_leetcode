import os
import csv
from services.db_service import DatabaseBuilder, get_database
from fastapi import Depends

# path to csv file 

csv_file = os.path.join(os.path.dirname(__file__), "../csv/problems.csv")

if csv_file:
    print(f"Path to csv: {csv_file}")
else:
    print("OOPs")

# TODO: Fix the module error 
def migrate_csv_to_db(db: DatabaseBuilder = Depends(get_database)):
    if db:
        db.init_db() 
    # Read the csv 
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
                # Grab the nubmber, problem, code from the csv
            for row in reader:
                problem_number = row["number"]
                problem_name = row["problem_name"]
                code = row["code"]
                # Format the data (especially the number) (0001 -> 1)
                problem_number = int(problem_number)


                # Insert into the db 
                db.insert_solution(
                    problem_number=problem_number,
                    problem_name=problem_name,
                    code=code
                )
                print(f"{problem_number} {problem_name} entered into db successfully.")

    except Exception as e:
        print(f"Error during CSV migration: {e}")

# To run the function
if __name__ == "__main__":
    db_instance = get_database()
    if db_instance:
        migrate_csv_to_db(db=db_instance)
        db_instance.engine.dispose()
    else:
        print("Failed to obtain a database instance.")