from pydantic import BaseModel

class PyBaseModel(BaseModel):
    class Config:
        validate_assignment = True
        validate_all = False
        allow_mutation = True
        allow_population_by_field_name = True
