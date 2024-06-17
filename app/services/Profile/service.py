import datetime
from . import request_schema, response_schema
from app.services.Event.utils import update_preference
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.utils.database import create_connection
from app.utils.utility import show_responses, find_duplicate_data

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
        user_detail = response_schema.ProfileDetail(**data)
        user_detail_dict = user_detail.dict()
        return JSONResponse({"data": user_detail_dict }, status_code=200)
    except Exception as err:
        show_responses("Failed to get users information", 404, error=err)

def get_org_profile(id):
    conn = create_connection()
    cursor = conn.cursor()
    try: 
        cursor.execute(
            """
            SELECT *
            FROM organization
            WHERE organization_id=%s 
            """,(id,)
        )
        temp_data = cursor.fetchone()
        data = jsonable_encoder(temp_data)
        conn.close()
        org_detail = response_schema.OrganizationDetail(**data)
        org_detail_dict = org_detail.dict()
        return JSONResponse({"data": org_detail_dict}, status_code=200)
    except Exception as err:
        show_responses("Failed to get organization information", 404, error=err)

def update_user_profile(request, id):
    conn = create_connection()
    cursor = conn.cursor()
    username = request.username
    user_exists = find_duplicate_data("users", "username", username.lower())
    org_exists = find_duplicate_data("organization", "username", username.lower())
    if user_exists or org_exists:
        return JSONResponse({"messagge": f"username {request.username} has been taken"}, status_code=406)
    
    try:
        preference = request_schema.Preference(
            hobby=request.hobby_preference,
            religion=request.religion_preference,
            city=request.city_preference,
            gender=request.gender_preference
        )
        # update_preference(preference, row["preference_id"])
        
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
            city = COALESCE(%s, city),
            is_new_user = %s
            WHERE user_id = %s
            """, (request.username, request.name, request.email, request.contact, 
                  request.guardian_contact, request.religion, 
                  request.gender, request.dob, request.city, False, id)
        )
        conn.commit()
        conn.close()
        return show_responses("Profile Updated", 200)
    except Exception as err:
        show_responses("Failed update users profile", 404, error=err)

def update_org_profile(request, id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT is_new_user
            FROM organization
            WHERE organization_id=%s
            """, (id,)
        )
        temp_fetch = cursor.fetchone()
        is_new = temp_fetch['is_new_user']
        if is_new == False:
            return show_responses("Only new user can update profile", 401)
        else:
            pass
    except Exception as err:
        return show_responses("Failed to update organization profile", 404, error=err)
    
    username = request.username
    user_exists = find_duplicate_data("users", "username", username.lower())
    org_exists = find_duplicate_data("organization", "username", username.lower())
    if user_exists or org_exists:
        return JSONResponse({"messagge": f"username {request.username} has been taken"}, status_code=406)
    try:
        cursor.execute(
            """
            UPDATE organization SET
            name = COALESCE(%s, name),
            username = COALESCE(%s, username),
            email = COALESCE(%s, email),
            description = COALESCE(%s, description),
            contact = COALESCE(%s, contact),
            is_new_user = %s
            WHERE organization_id = %s
            """, (request.name, request.username, request.email, 
                  request.description, request.contact, False, id)
        )
        conn.commit()
        conn.close()
        return show_responses("Profile Updated", 200)
    except Exception as err:
        return show_responses("Failed to update organization profile", 404, error=err)
    
def delete_org_profile(id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM organization 
            WHERE organization_id=%s
            """, (id,)
        )
        conn.commit()
        conn.close()
        return show_responses("Profile Deleted", 200)
    except Exception as err:
        return show_responses("Failed to delete organization profile", 404, error=err)
    
def delete_profile(id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM user 
            WHERE user_id=%s
            """, (id,)
        )
        conn.commit()
        conn.close()
        return show_responses("Profile Deleted", 200)
    except Exception as err:
        return show_responses("Failed to delete user profile", 404, error=err)