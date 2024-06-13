from datetime import datetime, timedelta
import uuid
from fastapi.responses import JSONResponse
from . import request_schema, response_schema
from app.utils.database import create_connection
from app.utils.authentication import validate_token_and_id

conn = create_connection()
cur = conn.cursor()

# TODO: Remove dummy id
user_id = "0b3933fc-1163-49ff-b61d-cc757a408cbf"
organization_id = "0b3933fc-1163-49ff-b61d-cc757a408123"

def get_all_by_event(event_id: str):
    get_query = f"""
        SELECT *
        FROM 
            comment_table
        WHERE 
            event_id = '{event_id}';
    """
    cur.execute(get_query)
    comments = cur.fetchall()

    return response_schema.CommentList(comments=comments)
    
def post_comment(comment: request_schema.Comment, user_id: str):
    insert_query = """
    INSERT INTO comment_table (
        comment_id, user_id, event_id, comment_text
    ) VALUES (
        %s, %s, %s, %s
    ) RETURNING *;
    """

    event_id = comment.event_id
    comment_text = comment.comment_text

    comment_data = (
        str(uuid.uuid4()), user_id, event_id, comment_text
    )
    
    try:
        cur.execute(insert_query, comment_data)
        conn.commit()

        new_comment = cur.fetchone()

        if new_comment:
            return response_schema.Comment(**new_comment)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def delete_comment(comment_id: str, user_id: str):
    cur.execute(f"SELECT * FROM comment_table WHERE comment_id='{comment_id}' and user_id='{user_id}';")
    comment = cur.fetchone()

    if not comment:
        return JSONResponse({"message": f"This user doesn't have comment with id {comment_id}"}, status_code=404)
    
    delete_query = f"""
        DELETE FROM comment_table
        WHERE comment_id = '{comment_id}'
        RETURNING comment_id;
        """
    
    try:
        cur.execute(delete_query)
        conn.commit()

        deleted_comment = cur.fetchone()
        deleted_comment_id = deleted_comment["comment_id"]

        return JSONResponse({"message": f"Comment with id {deleted_comment_id} is deleted"}, status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")