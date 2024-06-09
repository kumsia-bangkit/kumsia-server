from datetime import datetime, timedelta
import uuid
from fastapi.responses import JSONResponse
from . import request_schema, response_schema
from app.utils.database import create_connection

conn = create_connection()
cur = conn.cursor()

# TODO: Remove dummy id
user_id = "0b3933fc-1163-49ff-b61d-cc757a408cbf"
organization_id = "0b3933fc-1163-49ff-b61d-cc757a408123"

def is_liked(event_id: str):
    # TODO: Get id from logged in user
    # user_id =

    get_query = f"""
        SELECT *
        FROM 
            event_like
        WHERE 
            event_id = '{event_id}' and user_id = '{user_id}';
    """
    cur.execute(get_query)
    liked = cur.fetchone()

    return True if liked else False
    
def post_like(event_id: str):
    # TODO: Get id from logged in user
    # user_id =

    cur.execute(f"SELECT * FROM event_like WHERE event_id='{event_id}' and user_id='{user_id}';")
    liked = cur.fetchone()

    if liked:
        return JSONResponse({"message": f"User already liked event with id {event_id}"}, status_code=406)

    insert_query = """
    INSERT INTO event_like (
        like_id, user_id, event_id
    ) VALUES (
        %s, %s, %s
    ) RETURNING like_id;
    """

    like_data = (
        str(uuid.uuid4()), user_id, event_id
    )
    
    try:
        cur.execute(insert_query, like_data)
        conn.commit()

        new_like = cur.fetchone()

        return True if new_like else False
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def delete_like(event_id: str):
    # TODO: Get id from logged in user
    # user_id =

    cur.execute(f"SELECT * FROM event_like WHERE event_id='{event_id}' and user_id='{user_id}';")
    liked = cur.fetchone()

    if not liked:
        return JSONResponse({"message": f"User have not like event with id {event_id}"}, status_code=404)
    
    delete_query = f"""
        DELETE FROM event_like
        WHERE event_id = '{event_id}' and user = '{user_id}'
        RETURNING like_id;
        """
    
    try:
        cur.execute(delete_query)
        conn.commit()

        deleted_like = cur.fetchone()

        return False if deleted_like else True
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")