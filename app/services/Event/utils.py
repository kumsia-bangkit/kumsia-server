import uuid
from . import request_schema
from app.utils.database import create_connection

conn = create_connection()
cur = conn.cursor()

def create_preference(preference: request_schema.Preference):
    insert_query = """
        INSERT INTO preference (
            preference_id, hobby, religion, city, gender
        ) VALUES (
            %s, %s, %s, %s, %s
        ) RETURNING preference_id;
        """
    
    hobby = None
    religion = None
    city = None
    gender = None
    
    if preference.hobby:
        hobby = '{'
        for hobby_item in preference.hobby:
            hobby += f'\"{hobby_item}\"'

        hobby += '}'

    if preference.religion:
        religion = '{'
        for religion_item in preference.religion:
            religion += f'\"{religion_item}\"'

        religion += '}'

    if preference.city:
        city = '{'
        for city_item in preference.city:
            city += f'\"{city_item}\"'

        city += '}'

    if preference.gender:
        gender = '{'
        for gender_item in preference.gender:
            gender += f'\"{gender_item.value}\"'

        gender += '}'

    preference_data = (
        str(uuid.uuid4()), hobby, religion, city, gender
    )

    try:
        cur.execute(insert_query, preference_data)
        conn.commit()

        new_preference = cur.fetchone()

        if new_preference:
            return new_preference["preference_id"]
        
        return  ''
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def update_preference(preference: request_schema.Preference, preference_id: str):
    update_query = """
        UPDATE preference 
        SET hobby = %s, religion = %s, city = %s, gender = %s
        WHERE preference_id = %s
        RETURNING preference_id;
        """
    hobby = None
    religion = None
    city = None
    gender = None

    if preference.hobby:
        hobby = '{'
        for hobby_item in preference.hobby:
            hobby += f'\"{hobby_item}\"'

        hobby += '}'

    if preference.religion:
        religion = '{'
        for religion_item in preference.religion:
            religion += f'\"{religion_item}\"'

        religion += '}'

    if preference.city:
        city = '{'
        for city_item in preference.city:
            city += f'\"{city_item}\"'

        city += '}'

    if preference.gender:
        gender = '{'
        for gender_item in preference.gender:
            gender += f'\"{gender_item.value}\"'

        gender += '}'

    preference_data = (
        hobby, religion, city, gender, preference_id
    )

    try:
        cur.execute(update_query, preference_data)
        conn.commit()

        updated_preference = cur.fetchone()

        if updated_preference:
            return updated_preference["preference_id"]
        
        return  ''
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")