import uuid
from app.services.MasterData.service import get_master_city, get_master_hobby
from app.utils.database import create_connection
from app.utils.authentication import get_user_from_id
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from datetime import datetime, date

conn = create_connection()
cur = conn.cursor()

def get_recommendation(user_id: str):
    # Get Non friends
    f"""
    SELECT * AS
    FROM friends F
    WHERE F.first_party_id != {user_id} OR F.secod_party_id != {user_id}
    """
    """
    SELECT * 
    FROM users U
    JOIN friend F ON U.user_id = F.first_party_id
    LEFT JOIN preference P on U.preference_id = P.preference_id
    WHERE F.first_party_id != 'd29a683e-ce09-438d-9c13-2e452d0ae4e6' OR F.second_party_id != 'd29a683e-ce09-438d-9c13-2e452d0ae4e6'
    UNION
    SELECT * 
    FROM users U 
    JOIN friend F ON U.user_id = F.second_party_id
    LEFT JOIN preference P on U.preference_id = P.preference_id
    WHERE F.first_party_id != 'd29a683e-ce09-438d-9c13-2e452d0ae4e6' OR F.second_party_id != 'd29a683e-ce09-438d-9c13-2e452d0ae4e6';
    
    """
    """
    SELECT * 
    FROM users U
    JOIN friend F ON U.user_id = F.first_party_id
    LEFT JOIN preference P on U.preference_id = P.preference_id
    UNION
    SELECT * 
    FROM users U 
    JOIN friend F ON U.user_id = F.second_party_id
    LEFT JOIN preference P on U.preference_id = P.preference_id

    """
    # d29a683e-ce09-438d-9c13-2e452d0ae4e6
    query = f"""
    SELECT U.*, P.hobby
    FROM users U
    JOIN friend F ON U.user_id = F.first_party_id
    LEFT JOIN preference P on U.preference_id = P.preference_id
    WHERE F.first_party_id != {user_id} OR F.second_party_id != {user_id}
    UNION
    SELECT U.*, P.hobby 
    FROM users U 
    JOIN friend F ON U.user_id = F.second_party_id
    LEFT JOIN preference P on U.preference_id = P.preference_id
    WHERE F.first_party_id != {user_id} OR F.second_party_id != {user_id}
    """

    cur.execute(query)
    non_friends = cur.fetchall()

    # get user logged in and their preferences
    query = f"""
    SELECT P.hobby, P.gender, P.city, P.religion
    FROM users U
    JOIN preference P on U.preference_id = P.preference_id
    WHER u.user_id = {user_id}
    """
    cur.execute(query)
    user_preference = cur.fetchone()

    # turn non-friends into df
    df = pd.DataFrame.from_dict(non_friends)

    # get hobbies
    hobbies = get_master_hobby()
    # one hot encode all hobbies
    for hobby in hobbies:
        df[hobby] = df.apply(lambda x:1 if hobby in x.hobby else 0, axis=1)
    
    # set gender match 
    df["gender_match"] = df["gender"].apply(lambda x: 1 if x in user_preference["gender"] or len(user_preference["gender"]) == 0 else 0) 
    # set city match
    df["city_match"] = df["city"].apply(lambda x: 1 if x in user_preference["city"] or len(user_preference["city"]) == 0 else 0) 
    # set religion match 
    df["religion_match"] = df["religion"].apply(lambda x: 1 if x in user_preference["religion"] or len(user_preference["religion"]) == 0 else 0) 

    # Get Age
    df["dob"] = pd.to_datetime(df["dob"]) 
    df["age"] = df.apply(lambda x: (datetime.today() - x.dob).days, axis=1)

    # Get Days Offline
    df["last_activity"] = pd.to_datetime(df["last_activity"]) 
    df["days_offline"] = df.apply(lambda x: (datetime.today() - x.last_activity).days, axis=1)

    # Check if has profile picture
    df["has_profile_pic"] = df.apply(lambda x: 1 if x.profile_picture else 0)

    return