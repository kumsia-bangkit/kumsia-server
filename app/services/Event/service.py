from datetime import datetime
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from . import schema
from enums.event_status import Status
from utils.database import create_connection

conn = create_connection()
cur = conn.cursor()

def get_all():
    cur.execute("SELECT * FROM events;")
    events = cur.fetchall()
    return events

def post_event(event: schema.Event):
    insert_query = """
    INSERT INTO events (
        city, capacity, contact_link, date_time, description, disclaimer,
        gender_restriction, last_edited, location, name, organizer, status
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) RETURNING id;
    """
    
    event_id = uuid4()
    
    if isinstance(event.date_time, datetime):
        date_time = event.date_time.isoformat()

    # TODO: change str(event_id) to organizer's id once auth is implemented
    event_data = (
        event.city, event.capacity, event.contact_link, date_time, event.description, event.disclaimer,
        event.gender_restriction, datetime.now(), event.location, event.name, str(event_id), Status.draft
    )
    
    try:
        cur.execute(insert_query, event_data)
        conn.commit()

        new_event = cur.fetchone()

        return JSONResponse(jsonable_encoder({"id": str(new_event[0])}), status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")