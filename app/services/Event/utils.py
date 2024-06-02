from . import schema
from utils.database import create_connection

conn = create_connection()
cur = conn.cursor()

def create_preference(preference: schema.Preference):
    insert_query = """
        INSERT INTO preference (
            hobby, religion, city, gender
        ) VALUES (
            %s, %s, %s, %s
        ) RETURNING preference_id;
        """
    hobby = '{'
    for hobby_item in preference.hobby:
        hobby += f'\"{hobby_item}\"'

    hobby += '}'

    religion = '{'
    for religion_item in preference.religion:
        religion += f'\"{religion_item}\"'

    religion += '}'

    city = '{'
    for city_item in preference.city:
        city += f'\"{city_item}\"'

    city += '}'

    gender = '{'
    for gender_item in preference.gender:
        gender += f'\"{gender_item}\"'

    gender += '}'

    preference_data = (
        hobby, religion, city, gender
    )

    try:
        cur.execute(insert_query, preference_data)
        conn.commit()

        new_preference = cur.fetchone()

        if preference:
            return str(new_preference[0])
        
        return  ''
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def update_preference(preference: schema.Preference):
    update_query = """
        UPDATE preference 
        SET hobby = %s, religion = %s, city = %s, gender = %s
        WHERE preference_id = %s
        RETURNING preference_id;
        """

    hobby = '{'
    for hobby_item in preference.hobby:
        hobby += f'\"{hobby_item}\"'

    hobby += '}'

    religion = '{'
    for religion_item in preference.religion:
        religion += f'\"{religion_item}\"'

    religion += '}'

    city = '{'
    for city_item in preference.city:
        city += f'\"{city_item}\"'

    city += '}'

    gender = '{'
    for gender_item in preference.gender:
        gender += f'\"{gender_item}\"'

    gender += '}'

    preference_data = (
        hobby, religion, city, gender, preference.preference_id
    )

    try:
        cur.execute(update_query, preference_data)
        conn.commit()

        updated_preference = cur.fetchone()

        if preference:
            return str(updated_preference[0])
        
        return  ''
        
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")