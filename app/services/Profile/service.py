from app.utils.authentication import create_access_token, verify_password, get_password_hash
from . import request_schema, response_schema
from app.services.Event.utils import update_preference
from fastapi.responses import JSONResponse
from app.utils.database import create_connection
from app.utils.utility import show_responses, find_duplicate_data

def get_profile(id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.*,
                p.hobby AS preference_hobby,
                p.religion AS preference_religion,
                p.city AS preference_city,
                p.gender AS preference_gender
            FROM users u
            LEFT JOIN preference p ON u.preference_id = p.preference_id
            WHERE user_id=%s
            """, (id,)
        )
        temp_data = cursor.fetchone()
        if not temp_data:
            show_responses("Failed to get users information", 404, error=err)

        temp_data["is_friends"] = True

        conn.close()
        return response_schema.ProfileDetail(**temp_data)
    except Exception as err:
        show_responses("Failed to get users information", 404, error=err)

def get_user_profile(user_id, id, role):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT u.*,
                p.hobby AS preference_hobby,
                p.religion AS preference_religion,
                p.city AS preference_city,
                p.gender AS preference_gender
            FROM users u
            LEFT JOIN preference p ON u.preference_id = p.preference_id
            WHERE user_id=%s
            """, (user_id,)
        )

        user = cursor.fetchone()

        if user and role == "user":
            cursor.execute(
                f"""
                SELECT *
                FROM friend
                WHERE status = TRUE and 
                    (first_party_id = '{user_id}' and second_party_id = '{id}')
                    or (first_party_id = '{id}' and second_party_id = '{user_id}');
                """
            )

            friend = cursor.fetchone()

            if not friend and user_id != id:
                user["contact"] = None
                user["guardian_contact"] = None
                user["is_friends"] = False
            else:
                user["is_friends"] = True

        elif user and role == "organization":
            cursor.execute(
                f"""
                SELECT *
                FROM joined_event je
                JOIN
                    events e ON e.event_id = je.event_id
                WHERE je.user_id = '{user_id}' AND e.organization_id = '{id}';
                """
            )

            joined = cursor.fetchall()

            if not joined:
                user["contact"] = None
                user["guardian_contact"] = None
                user["is_friends"] = False
            else:
                user["is_friends"] = True

        conn.close()
        return response_schema.ProfileDetail(**user)

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
        conn.close()
        return response_schema.OrganizationDetail(**temp_data)
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
            SELECT *
            FROM users
            WHERE user_id=%s
            """, (id,)
        )
        data = cursor.fetchone()

        request.password = request.password if request.password else ""

        if not data.get("is_new_user") and not verify_password(request.password, data.get("password")):
            return JSONResponse({"messagge": f"Incorrect password"}, status_code=406)

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
        
        new_pass = None
        if request.new_password:
            new_pass = get_password_hash(request.new_password)

        cursor.execute(
            """
            UPDATE users SET
            username = COALESCE(%s, username),
            name = COALESCE(%s, name),
            email = COALESCE(%s, email),
            password = COALESCE(%s, password),
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
            """, (request.username, request.name, request.email, new_pass, request.contact, 
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
            }, "user"]
        
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
