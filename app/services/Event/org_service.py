from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from . import request_schema, response_schema
from app.enums.event import Status
from app.utils.database import create_connection
from app.services.Event.utils import *

conn = create_connection()
cur = conn.cursor()

def get_all(organization_id: str):
    get_query = f"""
        SELECT 
            e.event_id, 
            e.organization_id, 
            e.name, 
            e.location, 
            e.profie_picture, 
            e.status, 
            e.type, 
            e.event_start, 
            e.city, 
            e.link, 
            e.description, 
            e.attendee_criteria, 
            e.contact_varchar, 
            e.like_count, 
            e.capacity, 
            e.last_edited, 
            e.preference_id, 
            p.hobby AS hobby_preference, 
            p.religion AS religion_preference, 
            p.city AS city_preference, 
            p.gender AS gender_preference
        FROM 
            events e
        JOIN 
            preference p ON e.preference_id = p.preference_id
        WHERE 
            e.organization_id = '{organization_id}';
    """
    cur.execute(get_query)
    events = cur.fetchall()

    return response_schema.OrganizationEventList(events=events)

def get_event_by_id(event_id: str, organization_id: str):
    get_query = f"""
        SELECT 
            e.event_id, 
            e.organization_id, 
            e.name, 
            e.location, 
            e.profie_picture, 
            e.status, 
            e.type, 
            e.event_start, 
            e.city, 
            e.link, 
            e.description, 
            e.attendee_criteria, 
            e.contact_varchar, 
            e.like_count, 
            e.capacity, 
            e.last_edited, 
            e.preference_id, 
            p.hobby AS hobby_preference, 
            p.religion AS religion_preference, 
            p.city AS city_preference, 
            p.gender AS gender_preference
        FROM 
            events e
        JOIN 
            preference p ON e.preference_id = p.preference_id
        WHERE 
            e.organization_id = '{organization_id}' AND
            e.event_id='{event_id}';
    """

    cur.execute(get_query)
    event = cur.fetchone()

    if event:
        return response_schema.OrganizationEvent(**event)
    
    return JSONResponse({"message": f"No event with id {event_id}"}, status_code=404)
    

def post_event(event: request_schema.Event, profile_picture:str, organization_id: str):
    insert_query = """
    INSERT INTO events (
        event_id, organization_id, preference_id, name, location, profie_picture,
        status, type, event_start, city, link, description, attendee_criteria,
        contact_varchar, like_count, capacity, last_edited
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) RETURNING event_id;
    """

    preference = request_schema.Preference(
        hobby=event.hobby_preference,
        religion=event.religion_preference,
        city=event.city_preference,
        gender=event.gender_preference)
    
    preference_id = create_preference(preference)
    name = event.name
    location = event.location
    status = Status.DRAFT
    type = event.type
    event_start = event.event_start
    city = event.city
    link = event.link
    description = event.description
    attendee_criteria = event.attendee_criteria
    contact = event.contact
    like_count = 0
    capacity = event.capacity
    last_edited = datetime.now().isoformat()

    event_data = (
        str(uuid.uuid4()), str(organization_id), preference_id, name, location, profile_picture,
        status, type, event_start, city, link, description, attendee_criteria,
        contact, like_count, capacity, last_edited
    )
    
    try:
        cur.execute(insert_query, event_data)
        conn.commit()

        new_event = cur.fetchone()

        return get_event_by_id(new_event["event_id"], organization_id)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def update_event(event_id:str, event: request_schema.Event, profile_picture:str, organization_id: str):
    cur.execute(f"SELECT * FROM events WHERE organization_id='{organization_id}' AND event_id='{event_id}';")
    cur_event = cur.fetchone()

    if not cur_event:
        return JSONResponse({"message": f"No event with id {event_id}"}, status_code=404)
    
    if cur_event["status"] == Status.CLOSED or cur_event["status"] == Status.CANCELLED:
        return JSONResponse({"message": f"Closed event can't be edited"}, status_code=406)
    
    elif cur_event["status"] == Status.DRAFT:
        update_query = """
            UPDATE events 
            SET name = %s, location = %s, profie_picture = %s,
                type = %s, event_start = %s, city = %s, link = %s, description = %s,
                attendee_criteria = %s, contact_varchar = %s, like_count = %s, capacity = %s, last_edited = %s
            WHERE organization_id = %s AND event_id = %s
            RETURNING event_id;
            """

        preference = request_schema.Preference(
            hobby=event.hobby_preference,
            religion=event.religion_preference,
            city=event.city_preference,
            gender=event.gender_preference)
        
        update_preference(preference, cur_event["preference_id"])

        name = event.name
        location = event.location
        profile_picture = profile_picture if profile_picture else cur_event["profie_picture"]
        type = event.type
        event_start = event.event_start
        city = event.city
        link = event.link
        description = event.description
        attendee_criteria = event.attendee_criteria
        contact = event.contact
        like_count = 0
        capacity = event.capacity
        last_edited = datetime.now().isoformat()

        event_data = (
            name, location, profile_picture, type, event_start, city, link, description, attendee_criteria,
            contact, like_count, capacity, last_edited, str(organization_id), str(event_id)
        )

    elif cur_event["status"] == Status.OPEN:
        event_start = datetime.combine(cur_event["event_start"], datetime.min.time())
        if event_start - timedelta(days=1) < datetime.now():
            return JSONResponse({"message": f"Event can only be edited maximum 24 hours before the event date"}, status_code=406)

        update_query = """
            UPDATE events 
            SET city = %s, location = %s, type = %s, link = %s,
            description = %s, last_edited = %s
            WHERE organization_id = %s AND event_id = %s
            RETURNING event_id;
            """

        city = event.city
        location = event.location
        type = event.type
        link = event.link
        description = event.description
        last_edited = datetime.now().isoformat()

        event_data = (
            city, location, type, link, description,
            last_edited, str(organization_id), str(event_id)
        )
        
    try:
        cur.execute(update_query, event_data)
        conn.commit()

        updated_event = cur.fetchone()

        return get_event_by_id(updated_event["event_id"], organization_id)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def delete_event(event_id: str, organization_id: str):
    cur.execute(f"SELECT * FROM events WHERE organization_id='{organization_id}' AND event_id='{event_id}';")
    cur_event = cur.fetchone()

    if not cur_event:
        return JSONResponse({"message": f"No event with id {event_id}"}, status_code=404)
    
    if cur_event["status"] != Status.DRAFT :
        return JSONResponse({"message": f"You can only delete draft event"}, status_code=406)
    
    delete_query = """
        DELETE FROM events
        WHERE organization_id = %s AND event_id = %s
        RETURNING event_id;
        """
    
    event_data = (
        str(organization_id), event_id
    )
    
    try:
        cur.execute(delete_query, event_data)
        conn.commit()

        deleted_event = cur.fetchone()
        deleted_event_id = deleted_event["event_id"]

        return JSONResponse({"message": f"Event with id {deleted_event_id} is deleted"}, status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def submit_event(event_id: str, organization_id: str):
    cur.execute(f"SELECT * FROM events WHERE organization_id='{organization_id}' AND event_id='{event_id}';")
    cur_event = cur.fetchone()

    if not cur_event:
        return JSONResponse({"message": f"No event with id {event_id}"}, status_code=404)
    
    if cur_event["status"] != Status.DRAFT:
        return JSONResponse({"message": f"You can only submit draft event"}, status_code=406)
    
    update_query = """
        UPDATE events 
        SET status= %s, last_edited = %s
        WHERE organization_id = %s AND event_id = %s
        RETURNING event_id;
        """

    status = Status.OPEN
    last_edited = datetime.now().isoformat()

    event_data = (
        status, last_edited, str(organization_id), str(event_id)
    )
        
    try:
        cur.execute(update_query, event_data)
        conn.commit()

        submitted_event = cur.fetchone()

        return get_event_by_id(submitted_event["event_id"], organization_id)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def cancel_event(event_id: str, organization_id: str):
    cur.execute(f"SELECT * FROM events WHERE organization_id='{organization_id}' AND event_id='{event_id}';")
    cur_event = cur.fetchone()

    if not cur_event:
        return JSONResponse({"message": f"No event with id {id}"}, status_code=404)
    
    if cur_event["status"] == Status.DRAFT :
        return JSONResponse({"message": f"Draft event can't be cancelled"}, status_code=406)
    
    update_query = """
        UPDATE events 
        SET status= %s, last_edited = %s
        WHERE organization_id = %s AND event_id = %s
        RETURNING event_id;
        """

    status = Status.CANCELLED
    last_edited = datetime.now().isoformat()

    event_data = (
        status, last_edited, str(organization_id), str(event_id)
    )
        
    try:
        cur.execute(update_query, event_data)
        conn.commit()

        cancelled_event = cur.fetchone()

        return get_event_by_id(cancelled_event["event_id"], organization_id)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")