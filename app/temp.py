from pydantic import BaseModel

# use this instead https://prisma-client-py.readthedocs.io/en/stable/getting_started/partial-types/

class Temp(BaseModel):
    y: int
    m: int
    d: int
    h: int
    averageTemp: str
