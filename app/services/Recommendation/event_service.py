from app.utils.database import create_connection
from . import response_schema
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from datetime import datetime
from sklearn.preprocessing import StandardScaler

conn = create_connection()
cur = conn.cursor()

def add_has_profile_pic(row):
    if row["profie_picture"] and row["profie_picture"] != "https://storage.googleapis.com/kumsia-storage/placeholder/event.jpg":
        return 1
    
    return 0

def get_master_hobby():
    cur.execute("SELECT * FROM master_hobby ORDER BY hobby ASC;")
    hobby_list = [h["hobby"] for h in cur.fetchall()]  # Store list directly
    return hobby_list  # Return the list itself

def get_event_recommendation(user_id: str):
    # Get Non event joined by logged-in user
    query = f"""
    SELECT e.*, p.hobby, p.religion, p.city, p.gender, j.user_id AS joined
    FROM events e
    LEFT JOIN preference p ON e.preference_id = p.preference_id
    LEFT JOIN joined_event j ON e.event_id = j.event_id AND j.user_id = '{user_id}'
    WHERE e.status = 'Open' AND j.user_id IS NULL
    ORDER BY e.event_start ASC;
    """

    cur.execute(query)
    non_join = cur.fetchall()

    # get user logged in's preferences and info
    query = f"""
    SELECT u.user_id, P.hobby, P.gender, P.city, P.religion
    FROM users U
    JOIN preference P on U.preference_id = P.preference_id
    WHERE u.user_id = '{user_id}'
    """
    cur.execute(query)
    user_preference = cur.fetchone()

    # turn user preference into df
    df = pd.DataFrame.from_dict(non_join)
    data = [user_preference]
    user_df = pd.DataFrame(data)

    # Get hobbies
    hobbies = get_master_hobby()
    # One hot encode all hobbies
    for hobby in hobbies:
        df[hobby] = df.apply(lambda x:1 if hobby in x.hobby else 0, axis=1)
        user_df[hobby] = user_df.apply(lambda x:1 if hobby in x.hobby else 0, axis=1)

    # Set gender match 
    df["gender_match"] = df["gender"].apply(lambda x: 4 if user_preference["gender"] == None or x in user_preference["gender"] or len(user_preference["gender"]) == 0 else 0) 
    user_df["gender_match"] = 4
    # Set city match
    df["city_match"] = df["city"].apply(lambda x: 1 if (x in user_preference.get("city", []) or x == []) else 0)
    user_df["city_match"] = 1
    # Set religion match 
    df["religion_match"] = df["religion"].apply(lambda x: 1 if (x in user_preference.get("religion", []) or x == []) else 0)
    user_df["religion_match"] = 1
    # Check if has profile picture
    df["has_profile_pic"] = df.apply(add_has_profile_pic, axis=1)
    user_df["has_profile_pic"] = 1
    # Drop unused columns
    preprocessed_df = df.drop(["organization_id", "preference_id", "name", "location", "profie_picture", 
                            "status", "type", "event_start", "link", "description", "attendee_criteria", 
                            "contact_varchar", "like_count", "capacity", "last_edited"], axis=1)

    preprocessed_user_df = user_df.drop(["user_id", "hobby", "gender", "city", "religion"], axis=1)
    preprocessed_df = preprocessed_df.drop(["event_id", "city", "hobby", "religion", "gender", "joined"], axis=1)

    # Neighbours Model
    n_neighbors = len(preprocessed_df) 
    if len(preprocessed_df) > 15:
        n_neighbors = 15

    knn = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto').fit(preprocessed_df)
    _, indices = knn.kneighbors(preprocessed_user_df)
    top_n_index = indices[0]
    top_n_event = df.iloc[top_n_index]

    #if more than 5 reccommended accounts, pick random 5
    if n_neighbors > 5:
        top_n_event = top_n_event.sample(5)
    recommended_events = []
    for _, row in top_n_event.iterrows():

        get_query = f"""
            SELECT 
                e.*,
                o.name AS organization_name,
                CASE 
                    WHEN je.user_id IS NOT NULL THEN true
                    ELSE false
                END AS joined,
                CASE 
                    WHEN l.user_id IS NOT NULL THEN true
                    ELSE false
                END AS liked,
                p.hobby AS hobby_preference, 
                p.religion AS religion_preference, 
                p.city AS city_preference, 
                p.gender AS gender_preference
            FROM 
                events e
            JOIN
                organization o ON e.organization_id = o.organization_id
            JOIN 
                preference p ON e.preference_id = p.preference_id
            LEFT JOIN 
                joined_event je ON e.event_id = je.event_id AND je.user_id = '{user_id}'
            LEFT JOIN 
                event_like l ON e.event_id = l.event_id AND l.user_id = '{user_id}'
            WHERE 
                e.event_id = '{row["event_id"]}';
        """

        cur.execute(get_query)
        event = cur.fetchone()

        recommended_events.append(response_schema.Event(**event))

    return response_schema.EventList(events=recommended_events)