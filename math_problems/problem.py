from pydantic import BaseModel
from typing import List

class Problem(BaseModel):
    ProblemTitle: str
    ProblemCategory: str
    ProblemYear: str
    ProblemNumber: str
    ProblemText: str
    ProblemAnswer: str | None = None
    ProblemTags: List[str] | None = None
    IsStaging: bool = False
    SolutionText: str | None = None
    AnswerOptions: str | None = None
    Action: int = 0
