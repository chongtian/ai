"""
This script generates math problems for CBE6 math practice, using a language model and saves them to a database.
"""

import os 
from get_problems import generate_cbe6_math_problems, initialize_openai_llm, initialize_local_llm
from kidproblem_apis import prepare_problems, save_problems, get_access_token_from_cognito
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

USE_OPEN_AI = False

def main(objective_num: int, start_num: int, production: bool):
     # Read sensitive values from environment variables
    USERNAME = os.getenv("COGNITO_USERNAME")
    PASSWORD = os.getenv("COGNITO_PASSWORD")
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    if not all([USERNAME, PASSWORD]):
        raise ValueError("One or more required environment variables are missing.")
    
    if OPENAI_API_KEY and USE_OPEN_AI:
        llm = initialize_openai_llm()
        logger.info("Use OpenAI Model") 
    else:
        llm = initialize_local_llm()
        logger.info("Use Local Model") 
    
    logger.info(f'The generated math problems will be saved to {"Production" if production else "Staging"} environment.')
  
    logger.info("Call llm to generate math problems ... ")
    raw_problems =  generate_cbe6_math_problems(llm, objective_num, USE_OPEN_AI)
    logger.info("Math problems are generated.")
    logger.info(raw_problems)  

    problems = prepare_problems(raw_problems, start_num)
    if not problems or len(problems) == 0:
        logger.info("No valid math problem is generated.")
        return
    logger.info("Math problems are processed.")
    logger.info(problems)

    access_token = get_access_token_from_cognito(USERNAME, PASSWORD)
    results = save_problems(problems, access_token, production)
    logger.info("Math problems are saved.")
    logger.debug(results)
    

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print("Usage: python cbe6.py <1-based topic number> <start problem number> [prod]")
        exit(1)

    if args[1].isdigit():
        objective_num = int(args[1])-1
    else:
        # this will pull in all objectives
        objective_num = -1
    
    if len(args) > 2 and args[2].isdigit():
        start_num = int(args[2])
    else:
        start_num = 1

    if len(args) > 3 and args[3].strip().lower == 'prod':
        production = True
    else:
        production = False        

    main(objective_num, start_num, production)