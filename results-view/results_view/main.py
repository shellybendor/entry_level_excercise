from fastapi import FastAPI
import redis


app = FastAPI()


@app.get("/home")
async def trying():
    return {"hello world": "shelly"}


@app.get("/sum/{sum_id}")
async def send_nums(sum_id: str):
    # return {"hi": "hello"}
    print(sum_id)
    r = redis.Redis(host='my_redis', port=6379, db=0)
    print(r.get(sum_id))
    return {"sum": r.get(sum_id)}
