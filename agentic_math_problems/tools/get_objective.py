from typing import List
from models.objective_model import Objective
from langchain_core.tools import tool
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = PROJECT_ROOT / "resources"
LOCAL_OBJECTIVES_FILE = RESOURCE_DIR / "cbe6_objectives.txt"


@tool
def get_objective(objective_num : int) -> Objective:
    """
    Return a learning objective for 6th grade's math CBE test. There are 9 objectives in total.

    Args:
        objective_num (int): the index of the objective in the collection of all objectives. It is one-based.

    Returns:
        Objective: The requested objective
        
    """
    with open(LOCAL_OBJECTIVES_FILE, "r", encoding="utf-8") as f:
        s = f.read()
    objectives = []
    raw = s.split("########")
    regex = re.compile(r"Objective:.+?(\d)\nCount:.+?(\d{1,2})(.*)", flags=re.DOTALL)
    for t in raw:
        matches = regex.finditer(t)
        match = next(matches, None)
        if match:
            obj = Objective(
                objective=int(match.group(1)),
                count=int(match.group(2)),
                text=(match.group(3)).strip()
            )
            objectives.append(obj)
    
    if objective_num >0 and objective_num <= len(objectives):
        return objectives[objective_num-1]     
    else:
        return objectives[0]


@tool
def get_all_objectives() -> List[Objective]:
    """
    Return all the learning objectives for 6th grade's math CBE test

    Args:
        There is no argument.

    Returns:
        List[Objective]: List of all available objectives
        
    """
    with open(LOCAL_OBJECTIVES_FILE, "r", encoding="utf-8") as f:
        s = f.read()
    objectives = []
    raw = s.split("########")
    regex = re.compile(r"Objective:.+?(\d)\nCount:.+?(\d{1,2})(.*)", flags=re.DOTALL)
    for t in raw:
        matches = regex.finditer(t)
        match = next(matches, None)
        if match:
            obj = Objective(
                objective=int(match.group(1)),
                count=int(match.group(2)),
                text=(match.group(3)).strip()
            )
            objectives.append(obj)
    
    return objectives