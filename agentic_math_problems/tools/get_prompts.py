from typing import List
from models.objective_model import Objective
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool  

import logging

logger = logging.getLogger(__name__)

@tool
def get_final_prompt(objective: Objective) -> str:
    """
    Return a prompt which will be used to generate math problem

    Args:
        objective (Objective): the learning objective which has count and objective_text.

    Returns:
        (str): the prompt which contains the learning objective
        
    """    
    math_template = """
    You are a Senior Math Teacher specializing in elementary and middle school education. 
    You excel at creating engaging, grade-appropriate practice problems that reinforce core mathematical concepts.
    Your task is to generate exactly {count} math practice problems based on the objective: 

    {objective_text}

    When generating math problems, follow all rules strictly:
    1. Problem Structure
    - Generate a JSON array of problems.
    - Each problem must include exactly these fields:
       * "ProblemText": Full problem including answer choices
       * "ProblemAnswer": The correct option (A, B, C, or D)      
    
    2. Problem Content
    - Most problems must be word problems of 3-5 sentences.
    - At most one problem may be a short (1 sentence) or simple expression-based problem.
    - Ensure problems are clear, realistic, and mathematically sound.

    3. Answer Choices
    - Each problem must have exactly 4 options labeled A, B, C, D.
    - Only one option is correct.
    - All answer choices must be included inside "ProblemText" (not separately).
    - Format answer choices like:
        <br/>A. ...
        <br/>B. ...
        <br/>C. ...
        <br/>D. ...
        
    4. LaTeX Formatting
    - Use standard LaTeX for all math expressions.
    - Inline math must be wrapped in $...$ (e.g., $x + 5 = 12$).
    - Do NOT use LaTeX environments such as item, itemize, or similar.
    - Ensure all LaTeX is valid and properly escaped for JSON.
    
    5. Line Breaks
    - Use "<br/>" for all line breaks inside "ProblemText".
    
    6. Charts / Diagrams (if needed)
    - If a chart or diagram is required:
      * Generate valid Asymptote code only (no comments, no extra text).
      * The code must compile in standard environments.
      * Do NOT use: table, grid, graphpaper, or crimson.
      * Embed using:
             <img src="PlaceHolder_<sequence>.png" alt="[asy] ...code... [/asy]" />
    
    7. Correctness & Validation
    Ensure:
    - The correct answer matches "ProblemAnswer".
    - All distractors are plausible but incorrect.
    - JSON output is valid and properly escaped.
    
    8. Output Format
    Return output strictly as:
        [
            {{
                "ProblemText": "...",
                "ProblemAnswer": "A",
            }}
        ]
    
    """
    
    logger.debug(f"In the get_final_prompt:Generating prompt for objective: {objective.text}")
    prompt_template = PromptTemplate.from_template(math_template)
    formatted_text = prompt_template.format(count=objective.count, objective_text=objective.text)
    return formatted_text

