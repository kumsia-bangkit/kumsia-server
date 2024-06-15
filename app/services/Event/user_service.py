from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from . import request_schema, response_schema
from app.enums.event import Status
from app.utils.database import create_connection
from app.services.Event.utils import *

conn = create_connection()
cur = conn.cursor()

def get_all(user_id: str):
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
            CASE 
                WHEN je.user_id IS NOT NULL THEN true
                ELSE false
            END AS joined,
            CASE 
                WHEN l.user_id IS NOT NULL THEN true
                ELSE false
            END AS liked,
            e.preference_id, 
            p.hobby AS hobby_preference, 
            p.religion AS religion_preference, 
            p.city AS city_preference, 
            p.gender AS gender_preference
        FROM 
            events e
        JOIN 
            preference p ON e.preference_id = p.preference_id
        LEFT JOIN 
            joined_event je ON e.event_id = je.event_id AND je.user_id = '{user_id}'
        LEFT JOIN 
            event_like l ON e.event_id = l.event_id AND l.user_id = '{user_id}';
    """
    cur.execute(get_query)
    events = cur.fetchall()

    return response_schema.UserEventList(events=events)

def get_all_joined_event(user_id: str):
    today = datetime.today()

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
            true AS joined,
            CASE 
                WHEN l.user_id IS NOT NULL THEN true
                ELSE false
            END AS liked,
            e.preference_id, 
            p.hobby AS hobby_preference, 
            p.religion AS religion_preference, 
            p.city AS city_preference, 
            p.gender AS gender_preference
        FROM 
            events e
        JOIN 
            preference p ON e.preference_id = p.preference_id
        JOIN 
            joined_event je ON e.event_id = je.event_id AND je.user_id = '{user_id}'
        LEFT JOIN 
            event_like l ON e.event_id = l.event_id AND l.user_id = '{user_id}'
        WHERE 
            je.user_id = %s AND e.event_start >= %s
        ORDER BY e.event_start ASC;
    """

    event_data = (user_id, today)
    try:
        cur.execute(get_query, event_data)
        conn.commit()

        events = cur.fetchall()
        return response_schema.UserEventList(events=events)
    
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def get_all_liked_event(user_id: str):
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
            CASE 
                WHEN je.user_id IS NOT NULL THEN true
                ELSE false
            END AS joined,
            true AS liked,
            e.preference_id, 
            p.hobby AS hobby_preference, 
            p.religion AS religion_preference, 
            p.city AS city_preference, 
            p.gender AS gender_preference
        FROM 
            events e
        JOIN 
            preference p ON e.preference_id = p.preference_id
        JOIN 
            event_like l ON e.event_id = l.event_id AND l.user_id = '{user_id}'
        LEFT JOIN 
            joined_event je ON e.event_id = je.event_id AND je.user_id = '{user_id}';
    """
    try:
        cur.execute(get_query)
        conn.commit()

        events = cur.fetchall()
        return response_schema.UserEventList(events=events)
    
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def get_event_by_id(event_id: str, user_id: str):
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
            CASE 
                WHEN je.user_id IS NOT NULL THEN true
                ELSE false
            END AS joined,
            CASE 
                WHEN l.user_id IS NOT NULL THEN true
                ELSE false
            END AS liked,
            e.preference_id, 
            p.hobby AS hobby_preference, 
            p.religion AS religion_preference, 
            p.city AS city_preference, 
            p.gender AS gender_preference
        FROM 
            events e
        JOIN 
            preference p ON e.preference_id = p.preference_id
        LEFT JOIN 
            joined_event je ON e.event_id = je.event_id AND je.user_id = '{user_id}'
        LEFT JOIN 
            event_like l ON e.event_id = l.event_id AND l.user_id = '{user_id}'
        WHERE 
            e.event_id = '{event_id}';
    """
    cur.execute(get_query)
    event = cur.fetchone()

    if event:
        return response_schema.UserEvent(**event)
    
    return JSONResponse({"message": f"No event with id {event_id}"}, status_code=404)

def join_event(event_id: str, user_id: str):
    cur.execute(f"SELECT * FROM joined_event WHERE user_id='{user_id}' AND event_id='{event_id}';")
    cur_joined_event = cur.fetchone()

    if cur_joined_event:
        return JSONResponse({"message": f"Can't join event with id {event_id} more than once"}, status_code=406)
    
    update_query = f"""
        UPDATE events 
        SET capacity = capacity - 1
        WHERE event_id = '{str(event_id)}' AND capacity > 0 AND status = 'Open'
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
        return JSONResponse({"message": f"Can't join event with id {event_id}"}, status_code=406)

    insert_query = """
    INSERT INTO joined_event (
        id, event_id, user_id 
    ) VALUES (
        %s, %s, %s
    ) RETURNING *;
    """
    event_data = (
        str(uuid.uuid4()), event_id, str(user_id)
    )
    
    try:
        cur.execute(insert_query, event_data)
        conn.commit()

        new_joined_event = cur.fetchone()

        return get_event_by_id(new_joined_event["event_id"], user_id)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def cancel_join_event(event_id: str, user_id: str):
    delete_query = """
        DELETE FROM joined_event
        WHERE event_id = %s AND user_id = %s
        RETURNING id;
        """

    event_data = (
        event_id, str(user_id)
    )
    
    try:
        cur.execute(delete_query, event_data)
        conn.commit()

        deleted_joined_event = cur.fetchone()
        if not deleted_joined_event:
            return JSONResponse({"message": f"You have not join this event"}, status_code=406)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

    update_query = f"""
        UPDATE events 
        SET capacity = capacity + 1
        WHERE event_id = '{str(event_id)}'
        RETURNING event_id;
        """
        
    try:
        cur.execute(update_query)
        conn.commit()
        
        unjoined_event = cur.fetchone()

        return get_event_by_id(unjoined_event["event_id"], user_id)

    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")