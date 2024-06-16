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

    preference_data = (
        str(uuid.uuid4()), preference.hobby, preference.religion, preference.city, preference.gender
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

    preference_data = (
        preference.hobby, preference.religion, preference.city, preference.gender, preference_id
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