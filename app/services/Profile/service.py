import datetime
from fastapi.responses import JSONResponse
from app.utils.database import create_connection
from app.utils.utility import show_responses, find_duplicate_data

def update_profile(request, id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE users SET
            username=%s, name=%s, email=%s, contact=%s, guardian_contact=%s, religion=%s,
            gender=%s, dob=%s, city=%s
            WHERE user_id=%s
            """, (request.username, request.name, request.email, request.contact, 
                  request.guardian_contact, request.religion, 
                  request.gender, request.dob, request.city, id)
        )
        conn.commit()
        conn.close()
        return "Profile Updated"
    except Exception as err:
        show_responses("Failed update users profile", 404, error=err)