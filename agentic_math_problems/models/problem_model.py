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

    model_config = {
        "title": "Problem",
        "json_schema_extra": {
            "examples": [
                {
                    "ProblemTitle": "HOME-C0420-001",
                    "ProblemCategory": "HOME",
                    "ProblemYear": "C0420",
                    "ProblemNumber": "001",
                    "ProblemText": "What is $1+1$ <br/> A. 1 <br/> B. 2 <br/> C. 3 <br/> D. 4",
                    "ProblemAnswer": "B",
                    "ProblemTags": ["CBE6"],
                    "IsStaging": True,
                    "SolutionText": "",
                    "AnswerOptions": "A,B,C,D",
                    "Action": 1
                }
            ]
        }
    }
