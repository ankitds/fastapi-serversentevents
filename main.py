import asyncio
from multiprocessing import Event
from tkinter.tix import Balloon
from urllib import response
import uvicorn
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import requests
from pydantic import BaseModel
from typing import List


app = FastAPI()


def get_balances(Request, chain, address):
    url = f"https://v2.unifront.io/v2/{chain}/address/{address}/balances"
    
    response = requests.get(url = url)
    data = response.json()
    return data


Balance_details = {}

#API to send the success response
@app.post("/response/")
async def root(request: Request):
    response = {}
    data = await request.json()
    chain,address = data.get("chain"), data.get("address")
    response['data'] = {"chain" : chain, "address" : address}
    response['status'] = "200 OK"
    Balance = get_balances(Request, chain, address)
    
    if Balance:
        print("rresult",Balance)
        Balance_details['balance'] = Balance
        events = message_stream(Request)
        if events != Balloon:
            pass
    return response


STREAM_DELAY = 2  # second
RETRY_TIMEOUT = 1500 


#API to generate events and streamed data
@app.get('/stream/data')
async def message_stream(request: Request):

    async def event_generator():
        # while True:
            # if await request.is_disconnected():
            #     break  
        if Balance_details:
            yield {
                    "data": Balance_details
            }
        await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())

