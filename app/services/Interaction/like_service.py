import uuid
from fastapi.responses import JSONResponse
from . import response_schema
from app.utils.database import create_connection

conn = create_connection()
cur = conn.cursor()

def is_liked(event_id: str, user_id: str):
    get_query = f"""
        SELECT *
        FROM 
            event_like
        WHERE 
            event_id = '{event_id}' and user_id = '{user_id}';
    """
    cur.execute(get_query)
    liked = cur.fetchone()

    response = response_schema.Like(
        event_id=event_id, user_id=user_id,
        is_liked= True if liked else False)
    
    return response
    
def post_like(event_id: str, user_id: str):
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

        if new_like:
            update_query = f"""
                UPDATE events 
                SET like_count = like_count + 1
                WHERE event_id = '{str(event_id)}'
                RETURNING *;
                """
            
            cur.execute(update_query)
            conn.commit()

        response = response_schema.Like(
            event_id=event_id, user_id=user_id,
            is_liked= True if new_like else False)
    
        return response
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def delete_like(event_id: str, user_id: str):
    cur.execute(f"SELECT * FROM event_like WHERE event_id='{event_id}' and user_id='{user_id}';")
    liked = cur.fetchone()

    if not liked:
        return JSONResponse({"message": f"User have not like event with id {event_id}"}, status_code=404)
    
    delete_query = f"""
        DELETE FROM event_like
        WHERE event_id = '{event_id}' and user_id = '{user_id}'
        RETURNING like_id;
        """
    
    try:
        cur.execute(delete_query)
        conn.commit()

        deleted_like = cur.fetchone()

        if deleted_like:
            update_query = f"""
                UPDATE events 
                SET like_count = like_count - 1
                WHERE event_id = '{str(event_id)}'
                RETURNING event_id;
                """
            
            cur.execute(update_query)
            conn.commit()

        response = response_schema.Like(
            event_id=event_id, user_id=user_id,
            is_liked= False if deleted_like else True)
        
        return response
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")