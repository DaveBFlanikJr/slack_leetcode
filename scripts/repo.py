import requests
import csv
import os
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

'''
    Pull the ruby solutions from github repo
'''
def get_solutions_list(repo_url, path):
    url = f"https://api.github.com/repos/{repo_url}/contents/{path}"
    try: 
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except Exception as e:
        print(f"Error fetching response: {e}")
        return 1

'''Download the individaul solutions'''
def download_file_contents(file_url):
    try: 
        response = requests.get(file_url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching response: {e}")
        return 1

'''
    Parse the file name
'''
def parse_file(file):
    parts = file.split('-', 1)
    number = parts[0]
    name = parts[1].replace('.rb', '') if len(parts) > 1 else file
    return number, name

'''
    save problems to csv file 
'''
def create_csv(problems, filename='problems.csv'):
    'save to the csv file path'
    directory = './csv'
    if not os.path.exists(directory):    
        print(f"Directory {directory} does not exist. creating directory")
        os.mkdir(directory, exist_ok=True)

    file_path = os.path.join(directory, filename)

    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        filenames = ['number', 'problem_name', 'code']
        writer = csv.DictWriter(csv_file, fieldnames=filenames)
        writer.writeheader()
        for problem in problems:
            writer.writerow(problem)

def fetch_and_store_problems(repo_url, path):
    '''Get the list of problems'''
    files = get_solutions_list(repo_url, path)

    '''Store the problems in a list'''
    problems = []

    for file in files:
        if file['type'] == 'file':
            file_name = file['name']
            file_url = file['download_url']

            code = download_file_contents(file_url)
            number, name = parse_file(file_name)

            problem = {
                'number': number,
                'problem_name': name,
                'code': code
            }
            problems.append(problem)
    '''Save to CSV'''
    create_csv(problems, 'problems.csv')

def fetch():
    REPO_URL = os.getenv('REPO_URL')
    PATH = os.getenv('REPO_PATH')
    if REPO_URL and PATH:
        fetch_and_store_problems(REPO_URL, PATH)
    else:
        print("Environment variables REPO_URL or REPO_PATH are not found.")

if __name__ == "__main__":
    fetch()