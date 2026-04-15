from pydantic import BaseModel

class InputContext(BaseModel):
    Count: int = 1
    ObjectiveText: str
    StartNum: int = 1
    SimpleSchema: bool = False
    Production: bool = False
    AccessToken: str
