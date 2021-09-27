from flask import Flask
from credentials import CredsManager
from events import EventRetriever

app = Flask(__name__)
creds_manager = CredsManager()
event_retriever = EventRetriever(creds_manager.creds)

@app.route("/")
def get_events():
    events = event_retriever.retrieve_events()
    return {"upcoming_birthdays": [event.to_dict() for event in events], "total": len(events)}