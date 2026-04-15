"""
This script is used to upload math problems to the database. 
It reads a json file which has math problems, prepares the problems and then saves them to the database using the API.
"""
import os 
from kidproblem_apis import prepare_problems, save_problems, get_access_token_from_cognito
import logging
import sys
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main(json_file:str, start_num:int, production: bool):
     # Read sensitive values from environment variables
    USERNAME = os.getenv("COGNITO_USERNAME")
    PASSWORD = os.getenv("COGNITO_PASSWORD")
    
    if not all([USERNAME, PASSWORD]):
        raise ValueError("One or more required environment variables are missing.")
    
    access_token = get_access_token_from_cognito(USERNAME, PASSWORD)    
    with open(json_file, "r", encoding="utf-8") as f:
         data = json.load(f)
    problems = prepare_problems(data, start_num)
    logger.info(problems)
    results = save_problems(problems, access_token, production)
    print(results)
    

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print("Usage: python upload.py <path to a json file which has math problems> <start problem number> [prod]")
        exit(1)
    if args[2].isdigit():
        start_num = int(args[2])
    else:
        start_num = 1

    if len(args) > 3 and args[3].strip().lower == 'prod':
        production = True
    else:
        production = False
    
    main(args[1], start_num, production)