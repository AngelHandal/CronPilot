from pydantic import BaseModel, Field

class CronJobCreate(BaseModel):
    expression: str = Field(..., example="0 5 * * 1")
    command: str = Field(..., example="echo 'hello world'")
