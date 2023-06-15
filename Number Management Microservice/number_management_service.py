import asyncio
import aiohttp
from aiohttp import ClientError

from typing import List
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

async def fetchnum_trial(url):
    try:
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('numbers', [])
                else:
                    raise HTTPException(status_code=resp.status, detail="number fetching failed")
    except ClientError:
        raise HTTPException(status_code=500, detail="number fetching failed")

@app.get("/numbers")
async def getnum_trial(urls: List[str] = Query(...)):
    tasks = [fetchnum_trial(url) for url in urls]
    try:
        results = await asyncio.gather(*tasks)
    except HTTPException as e:
        raise e

    numbers = set()
    for result in results:
        numbers.update(result)

    return {"numbers": sorted(list(numbers))}

