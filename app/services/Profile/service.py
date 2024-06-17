import datetime

from app.utils.authentication import create_access_token
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
            """, (id,)
        )
        temp_data = cursor.fetchone()
        if not temp_data:
            raise ValueError("User not found")
        data = jsonable_encoder(temp_data)

        try:
            cursor.execute(
            """
            SELECT hobby, religion, city, gender
            FROM preference
            WHERE preference_id = %s
            """, (data['preference_id'],)
            )
            preference_data = cursor.fetchone()
            
            preference_dict = {
                "hobby": preference_data.get('hobby'),
                "religion": preference_data.get('religion'),
                "city": preference_data.get('city'),
                "gender": preference_data.get('gender')
            }
            data["preference"] = preference_dict
        except Exception as err:
            show_responses("Failed to get users information", 404, error=err)

        conn.close()
        user_detail = response_schema.ProfileDetail(**data)
        user_detail_dict = user_detail.dict()
        return JSONResponse({"data": user_detail_dict}, status_code=200)
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

def update_user_profile(request, id, current_usn, picture):
    conn = create_connection()
    cursor = conn.cursor()
    username = request.username

    if username != current_usn and username != None:
        user_exists = find_duplicate_data("users", "username", username.lower())
        org_exists = find_duplicate_data("organization", "username", username.lower())
        if user_exists or org_exists:
            return JSONResponse({"messagge": f"username {request.username} has been taken"}, status_code=406)
    
    preference_id = None
    try:
        cursor.execute(
            """
            SELECT preference_id
            FROM users
            WHERE user_id=%s
            """, (id,)
        )
        data = cursor.fetchone()
        preference_id = data['preference_id']
    except Exception as err:
        show_responses("Failed get user preferences", 401, error=err)
    try:
        preference = request_schema.Preference(
            hobby=request.hobby_preference,
            religion=request.religion_preference,
            city=request.city_preference,
            gender=request.gender_preference
        )
        update_preference(preference, preference_id)
        
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
            profile_picture = COALESCE(%s, profile_picture),
            is_new_user = %s
            WHERE user_id = %s
            RETURNING *;
            """, (request.username, request.name, request.email, request.contact, 
                  request.guardian_contact, request.religion, 
                  request.gender, request.dob, request.city, picture, False, id)
        )
        conn.commit()

        new_data = cursor.fetchone()

        data = [{
            "sub": new_data['user_id'],
            "name": new_data['name'],
            "username": new_data['username'],
            "is_new_user": new_data['is_new_user']
            }, "organization"]
        
        new_token = create_access_token(data[0], data[1])
        conn.close()
        return response_schema.Token(access_token=new_token)
    except Exception as err:
        show_responses("Failed update users profile", 404, error=err)

def update_org_profile(request, id, current_usn, picture):
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
    if username != current_usn and username != None:
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
            profile_picture = COALESCE(%s, profile_picture),
            is_new_user = %s
            WHERE organization_id = %s
            RETURNING *;
            """, (request.name, request.username, request.email, 
                  request.description, request.contact, picture, False, id)
        )
        conn.commit()
        new_data = cursor.fetchone()

        data = [{
            "sub": new_data['organization_id'],
            "name": new_data['name'],
            "username": new_data['username'],
            "is_new_user": new_data['is_new_user']
            }, "organization"]
        
        new_token = create_access_token(data[0], data[1])

        conn.close()
        return response_schema.Token(access_token=new_token)
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