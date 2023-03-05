from fastapi import FastAPI
from pydantic import BaseModel


class TwoInts(BaseModel):
    first: int
    second: int


app = FastAPI()


@app.post("/sum")
async def send_nums(two_ints: TwoInts):
    return {"id": str(two_ints.first) + str(two_ints.second)}
    # return two_ints
