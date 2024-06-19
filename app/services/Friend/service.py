from fastapi.responses import JSONResponse
from . import response_schema
from app.utils.database import create_connection

conn = create_connection()
cur = conn.cursor()

def get_friends(user_id: str):
    get_query = f"""
        SELECT u.user_id, u.username, u.name, u.profile_picture
        FROM users u
        JOIN friend f ON u.user_id = f.second_party_id
        WHERE f.first_party_id = '{user_id}' AND f.status = true
        UNION
        SELECT u.user_id, u.username, u.name, u.profile_picture
        FROM users u
        JOIN friend f ON u.user_id = f.first_party_id
        WHERE f.second_party_id = '{user_id}' AND f.status = true;
    """

    cur.execute(get_query)
    friend = cur.fetchall()
    
    return response_schema.FriendList(friends=friend)

def get_friend_req(user_id: str):
    get_query = f"""
        SELECT u.user_id, u.username, u.name, u.profile_picture
        FROM users u
        JOIN friend f ON u.user_id = f.first_party_id
        WHERE f.second_party_id = '{user_id}' AND f.status = false;
    """
    
    cur.execute(get_query)
    friend_req = cur.fetchall()
    
    return response_schema.FriendList(friends=friend_req)

def send_friend_req(friend_id:str, user_id: str):
    cur.execute(f"""SELECT * 
                FROM friend 
                WHERE (first_party_id = '{user_id}' and second_party_id = '{friend_id}')
                    or (first_party_id = '{friend_id}' and second_party_id = '{user_id}');""")
    friend_exists = cur.fetchone()

    if friend_exists:
        return JSONResponse({"message": f"User is already friends or have sent a request before"}, status_code=406)

    insert_query = """
    INSERT INTO friend (
        first_party_id, second_party_id, status
    ) VALUES (
        %s, %s, %s
    ) RETURNING *;
    """

    data = (
        user_id, friend_id, False
    )
    
    try:
        cur.execute(insert_query, data)
        conn.commit()

        return JSONResponse({"message": f"Friend request is successfully sent!"}, status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def accept_friend_req(friend_id: str, user_id: str):
    update_query = f"""
        UPDATE friend 
        SET status = TRUE
        WHERE first_party_id = '{friend_id}' and second_party_id = '{user_id}' and status = FALSE
        RETURNING *;
        """
    
    try:
        cur.execute(update_query)
        conn.commit()

        accepted = cur.fetchone()

        if not accepted:
            return JSONResponse({"message": f"There is no friend request from this user"}, status_code=404)
        
        return JSONResponse({"message": f"Request has been accepted"}, status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def reject_friend_req(friend_id: str, user_id: str):
    delete_query = f"""
        DELETE FROM friend
        WHERE first_party_id = '{friend_id}' and second_party_id = '{user_id}' and status = FALSE
        RETURNING *;
        """
    
    try:
        cur.execute(delete_query)
        conn.commit()

        rejected = cur.fetchone()

        if not rejected:
            return JSONResponse({"message": f"There is no friend request from this user"}, status_code=404)
        
        return JSONResponse({"message": f"Request has been rejected"}, status_code=200)
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def is_friends(friend_id: str, user_id: str):
    cur.execute(f"""
        SELECT * 
        FROM friend 
        WHERE status = TRUE and 
            (first_party_id = '{user_id}' and second_party_id = '{friend_id}')
            or (first_party_id = '{friend_id}' and second_party_id = '{user_id}');
        """)
    
    friend_found = cur.fetchone()

    return True if friend_found else False