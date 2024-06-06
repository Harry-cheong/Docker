from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient

client = MongoClient('mongodb://mongodb:27017')
eventdb = client["events"]
app = FastAPI()

class Event(BaseModel):
    title: str
    description: str
    tag: list
    month: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/events/all")
def getAll():
    allEvents = []
    for collection in eventdb.list_collection_names():
        selectedCollection = eventdb[collection].find()
        for event in selectedCollection:
            del event["_id"]
            event["month"] = collection
            allEvents.append(event)
            
    return allEvents

@app.get("/events/{month}")
def getByMonth(month: str):
    events = []
    if month in eventdb.list_collection_names():
        selectedCollection = eventdb[month]
        for event in selectedCollection.find():
            del event["_id"]
            events.append(event)
        
        return events
        
@app.post("/events/")
def post_event(event: Event):
    mycollection = eventdb[event.month]
    event = {"title": event.title, "tag": event.tag}
    mycollection.insert_one(event)
