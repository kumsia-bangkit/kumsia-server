from app.services.MasterData.service import get_master_hobby
from app.utils.database import create_connection
from . import response_schema
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from datetime import datetime
from sklearn.preprocessing import StandardScaler

conn = create_connection()
cur = conn.cursor()

def get_recommendation(user_id: str):
    # Get Non friends
    query = f"""
    SELECT * FROM (
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
    UNION
    SELECT U.*, P.hobby
    FROM users U 
    LEFT JOIN preference P on U.preference_id = P.preference_id
    WHERE U.user_id = {user_id}
    )
    ORDER BY user_id;
    """

    cur.execute(query)
    non_friends = cur.fetchall()

    # get user logged in's preferences
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
    df["gender_match"] = df["gender"].apply(lambda x: 4 if x in user_preference["gender"] or len(user_preference["gender"]) == 0 else 0) 
    # set city match
    df["city_match"] = df["city"].apply(lambda x: 2 if x in user_preference["city"] or len(user_preference["city"]) == 0 else 0) 
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

    # Drop unused columns
    preprocessed_df = df.drop(["preference_id", "username", "name", "password", "email", "contact"
                            "guardian_contact", "profile_picture", "dob", "last_activity", "hobby",
                            "religion", "gender", "city"], axis=1)

    # Standardization only on age and offline days
    scaler = StandardScaler()
    preprocessed_df[["age", "days_offline"]] = scaler.fit_transform(preprocessed_df[["age", "days_offline"]])

    # Get User DF and drop user logged in from preprocessed df
    user_df = preprocessed_df[preprocessed_df["user_id"] == user_id]
    preprocessed_df.drop(preprocessed_df[preprocessed_df["user_id"] == user_id].index)

    # separate id
    id_df = preprocessed_df["user_id"]
    preprocessed_df.drop(["user_id"], axis=1)

    # Neighbours Model
    n_neighbors = len(preprocessed_df) 
    if len(preprocessed_df) > 15:
        n_neighbors = 15

    knn = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto').fit(preprocessed_df)
    distances, indices = knn.kneighbors(user_df)
    top_n_index = indices[0]
    top_n_user = df.iloc[top_n_index]

    # if more than 5 reccommended accounts, pick random 5
    if n_neighbors > 5:
        top_n_user = top_n_user.sample(5)

    recommended_users = []
    for _, row in top_n_user.iterrows():
        recommended_users.append(response_schema.User(user_id=row["user_id"],
                                                      username=row["username"],
                                                      name=row["name"],
                                                      profile_picture=row["profile_picture"],
                                                      religion=row["religion"],
                                                      gender=row["gender"],
                                                      city=row["city"]
                                                    )
                                )
    return response_schema.UsersList(users=recommended_users)