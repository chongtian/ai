from pydantic import BaseModel, Field

class Objective(BaseModel):
    objective: int
    count: int
    text: str

    model_config = {
        "title": "Objective",
        "json_schema_extra": {
            "examples": [
                {
                    "objective": 1,
                    "count": 10,
                    "text": "Understand basic principles"
                }
            ]
        }
    }
