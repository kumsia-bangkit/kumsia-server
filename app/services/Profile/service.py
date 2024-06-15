import datetime
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.utils.database import create_connection
from app.utils.utility import show_responses, find_duplicate_data

def get_user_profile_by_id(id, user_id):
    pass

def get_org_profile_by_id(id, user_id):
    pass

def get_user_profile(id):
    conn = create_connection()
    cursor = conn.cursor()
    try: 
        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE user_id=%s 
            """,(id,)
        )
        temp_data = cursor.fetchone()
        data = jsonable_encoder(temp_data)
        conn.close()
        return JSONResponse({"data": data}, status_code=200)
    except Exception as err:
        show_responses("Failed to get users information", 404, error=err)

def get_org_profile(id):
    pass

def update_user_profile(request, id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE users SET
            username = COALESCE(%s, username),
            name = COALESCE(%s, name),
            email = COALESCE(%s, email),
            contact = COALESCE(%s, contact),
            guardian_contact = COALESCE(%s, guardian_contact),
            religion = COALESCE(%s, religion),  
            gender = COALESCE(%s, gender),
            dob = COALESCE(%s, dob),
            city = COALESCE(%s, city)
            WHERE user_id = %s
            """, (request.username, request.name, request.email, request.contact, 
                  request.guardian_contact, request.religion, 
                  request.gender, request.dob, request.city, id)
        )
        conn.commit()
        conn.close()
        return show_responses("Profile Updated", 200)
    except Exception as err:
        show_responses("Failed update users profile", 404, error=err)

def update_org_profile(request, id):
    pass