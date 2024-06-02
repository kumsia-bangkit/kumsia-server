from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from . import schema
from enums.event_status import Status
from utils.database import create_connection
from services.Event.utils import *

conn = create_connection()
cur = conn.cursor()

# TODO: Remove dummy id
user_id = "0b3933fc-1163-49ff-b61d-cc757a408cbf"
organization_id = "0b3933fc-1163-49ff-b61d-cc757a408123"

def get_all():
    cur.execute("SELECT * FROM event;")
    events = cur.fetchall()
    return events

def get_all_joined_event():
    # TODO: Get id from logged in user
    # user_id =
    today = datetime.today()

    get_query = """
        SELECT *
        FROM (
            SELECT * FROM event WHERE date_time >= %s;
        ) as event
        INNER JOIN (
            SELECT * FROM joined_event WHERE user_id = %s;
        ) as joined_event
        ON event.event_id=joined_event.event_id
        ORDER BY event.date_time ASC;
        """
    
    event_data = (today, user_id)

    try:
        cur.execute(get_query, event_data)
        conn.commit()

        events = cur.fetchall()

        return events
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def get_event_by_id(id: str):
    cur.execute(f"SELECT * FROM event WHERE event_id={id};")
    event = cur.fetchone()

    if event:
        return JSONResponse(event[0], status_code=200)
    
    return JSONResponse({"message": f"No event with id {id}"}, status_code=404)
    

def post_event(event: schema.Event):
    insert_query = """
    INSERT INTO event (
        organization_id, preference_id, name, location, profile_picture,
        status, type, date_time, city, link, description, attendee_criteria,
        contact, like_count, capacity, last_edited
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) RETURNING event_id;
    """
    # TODO: Get id from logged in user
    # organization_id =

    preference = schema.Preference(
        hobby=event.hobby,
        religion=event.religion,
        city=event.city,
        gender=event.gender)
    
    preference_id = create_preference(preference)
    name = event.name
    location = event.location
    # TODO: Set up cloud storage
    profile_picture = event.profile_picture
    status = Status.DRAFT
    type = event.type
    date_time = event.date_time
    city = event.city
    link = event.link
    description = event.description
    attendee_criteria = event.attendee_criteria
    contact = event.contact
    like_count = 0
    capacity = event.capacity
    last_edited = datetime.now().isoformat()
    
    if isinstance(date_time, datetime):
        date_time = date_time.isoformat()

    event_data = (
        str(organization_id), preference_id, name, location, profile_picture,
        status, type, date_time, city, link, description, attendee_criteria,
        contact, like_count, capacity, last_edited
    )
    
    try:
        cur.execute(insert_query, event_data)
        conn.commit()

        new_event = cur.fetchone()

        return JSONResponse(new_event[0], status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def update_event(event: schema.Event):
    # TODO: Get id from logged in user
    # organization_id =
    event_id = event.event_id

    cur.execute(f"SELECT * FROM event WHERE organization_id = {organization_id} AND event_id={event_id};")
    cur_event = cur.fetchone()

    if cur_event:
        cur_event = cur_event[0]
    else:
        return JSONResponse({"message": f"No event with id {id}"}, status_code=404)
    
    if cur_event["status"] == Status.CLOSED or cur_event["status"] == Status.CANCELLED:
        return JSONResponse({"message": f"Closed event can't be edited"}, status_code=406)
    
    elif cur_event["status"] == Status.DRAFT:
        update_query = """
            UPDATE event 
            SET name = %s, location = %s, profile_picture = %s,
                type = %s, date_time = %s, city = %s, link = %s, description = %s,
                attendee_criteria = %s, contact = %s, like_count = %s, capacity = %s, last_edited = %s
            WHERE organization_id = %s AND event_id = %s
            RETURNING event_id;
            """

        preference = schema.Preference(
            hobby=event.hobby,
            religion=event.religion,
            city=event.city,
            gender=event.gender)
        
        update_preference(preference)

        name = event.name
        location = event.location
        # TODO: Set up cloud storage
        profile_picture = event.profile_picture
        type = event.type
        date_time = event.date_time
        city = event.city
        link = event.link
        description = event.description
        attendee_criteria = event.attendee_criteria
        contact = event.contact
        like_count = 0
        capacity = event.capacity
        last_edited = datetime.now().isoformat()
        
        if isinstance(date_time, datetime):
            date_time = date_time.isoformat()

        event_data = (
            name, location, profile_picture, type, date_time, city, link, description, attendee_criteria,
            contact, like_count, capacity, last_edited, str(organization_id), str(event_id)
        )

    elif cur_event["status"] == Status.OPEN:
        if cur_event["date_time"] - timedelta(days=1) < datetime.now():
            return JSONResponse({"message": f"Event can only be edited maximum 24 hours before the event date"}, status_code=406)

        update_query = """
            UPDATE event 
            SET location = %s, type = %s, city = %s,
            link = %s, description = %s, capacity = %s, last_edited = %s
            WHERE organization_id = %s AND event_id = %s
            RETURNING event_id;
            """

        location = event.location
        type = event.type
        city = event.city
        link = event.link
        description = event.description
        capacity = event.capacity
        last_edited = datetime.now().isoformat()

        event_data = (
            location, type, city, link, description, capacity,
            last_edited, str(organization_id), str(event_id)
        )
        
    try:
        cur.execute(update_query, event_data)
        conn.commit()

        updated_event = cur.fetchone()

        return JSONResponse(updated_event[0], status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def delete_event(event_id: str):
    # TODO: Get id from logged in user
    # organization_id =

    cur.execute(f"SELECT * FROM event WHERE organization_id = {organization_id} AND event_id={event_id};")
    cur_event = cur.fetchone()

    if cur_event:
        cur_event = cur_event[0]
    else:
        return JSONResponse({"message": f"No event with id {id}"}, status_code=404)
    
    if cur_event["status"] != Status.DRAFT :
        return JSONResponse({"message": f"You can only delete draft event"}, status_code=406)
    
    delete_query = """
        DELETE FROM event
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

        return JSONResponse(deleted_event[0], status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def submit_event(event_id: str):
    # TODO: Get id from logged in user
    # organization_id =

    cur.execute(f"SELECT * FROM event WHERE organization_id = {organization_id} AND event_id={event_id};")
    cur_event = cur.fetchone()

    if cur_event:
        cur_event = cur_event[0]
    else:
        return JSONResponse({"message": f"No event with id {id}"}, status_code=404)
    
    if cur_event["status"] != Status.DRAFT:
        return JSONResponse({"message": f"You can only submit draft event"}, status_code=406)
    
    update_query = """
        UPDATE event 
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

        return JSONResponse(submitted_event[0], status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def cancel_event(event_id: str):
    # TODO: Get id from logged in user
    # organization_id =

    cur.execute(f"SELECT * FROM event WHERE organization_id = {organization_id} AND event_id={event_id};")
    cur_event = cur.fetchone()

    if cur_event:
        cur_event = cur_event[0]
    else:
        return JSONResponse({"message": f"No event with id {id}"}, status_code=404)
    
    if cur_event["status"] == Status.DRAFT :
        return JSONResponse({"message": f"Draft event can't be cancelled"}, status_code=406)
    
    update_query = """
        UPDATE event 
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

        return JSONResponse(cancelled_event[0], status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def join_event(event_id: str):
    # TODO: Get id from logged in user
    # user_id =

    cur.execute(f"SELECT * FROM joined_event WHERE user_id = {user_id} AND event_id={event_id};")
    cur_joined_event = cur.fetchone()

    if cur_joined_event:
        return JSONResponse({"message": f"Can't join event with id {id} more than once"}, status_code=406)
    
    update_query = f"""
        UPDATE event 
        SET capacity = capacity - 1
        WHERE event_id = {str(event_id)} AND capacity > 0
        RETURNING event_id;
        """
        
    try:
        cur.execute(update_query)
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

    event = cur.fetchone()

    if not event:
        return JSONResponse({"message": f"Can't join event with id {id}"}, status_code=406)

    insert_query = """
    INSERT INTO joined_event (
        event_id, user_id, 
    ) VALUES (
        %s, %s
    ) RETURNING joined_event_id;
    """
    event_data = (
        event_id, str(user_id)
    )
    
    try:
        cur.execute(insert_query, event_data)
        conn.commit()

        new_joined_event = cur.fetchone()

        return JSONResponse(new_joined_event[0], status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def cancel_join_event(event_id: str):
    # TODO: Get id from logged in user
    # user_id =

    delete_query = """
        DELETE FROM joined_event
        WHERE event_id = %s AND user_id = %s
        RETURNING joined_event_id;
        """

    event_data = (
        event_id, str(user_id)
    )
    
    try:
        cur.execute(delete_query, event_data)
        conn.commit()

        deleted_joined_event = cur.fetchone()

        return JSONResponse(deleted_joined_event[0], status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

    if not deleted_joined_event:
        return JSONResponse({"message": f"You have not join this event"}, status_code=406)

    update_query = f"""
        UPDATE event 
        SET capacity = capacity + 1
        WHERE event_id = {str(event_id)}
        RETURNING event_id;
        """
        
    try:
        cur.execute(update_query)
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")