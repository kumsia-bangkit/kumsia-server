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
        LEFT JOIN preference P on U.preference_id = P.preference_id
        WHERE NOT EXISTS (
            SELECT F.first_party_id, F.second_party_id
            FROM friend F
            WHERE (U.user_id = F.first_party_id AND F.second_party_id = '{user_id}') OR (U.user_id = F.second_party_id AND F.first_party_id = '{user_id}')
        )
        UNION
        SELECT U.*, P.hobby
        FROM users U 
        LEFT JOIN preference P on U.preference_id = P.preference_id
        WHERE U.user_id = '{user_id}'
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
    WHERE u.user_id = '{user_id}'
    """
    cur.execute(query)
    user_preference = cur.fetchone()
    # turn non-friends into df
    df = pd.DataFrame.from_dict(non_friends)

    # get hobbies
    hobbies = get_master_hobby().model_dump().get("Hobbies")
    # one hot encode all hobbies
    for hobby in hobbies:
        df[hobby] = df.apply(lambda x:1 if x.hobby and hobby in x.hobby else 0, axis=1)
    # set gender match 
    df["gender_match"] = df["gender"].apply(lambda x: 4 if user_preference["gender"] == None or x in user_preference["gender"] or len(user_preference["gender"]) == 0 else 0) 
    # set city match
    df["city_match"] = df["city"].apply(lambda x: 2 if user_preference["city"] == None or x in user_preference["city"] or len(user_preference["city"]) == 0 else 0) 
    # set religion match 
    df["religion_match"] = df["religion"].apply(lambda x: 1 if user_preference["religion"] == None or x in user_preference["religion"] or len(user_preference["religion"]) == 0 else 0) 

    # Get Age
    df["dob"] = pd.to_datetime(df["dob"]) 
    df["age"] = df.apply(lambda x: (datetime.today() - x.dob).days, axis=1)

    # Get Days Offline
    df["last_activity"] = pd.to_datetime(df["last_activity"]) 
    df["days_offline"] = df.apply(lambda x: (datetime.today() - x.last_activity).days, axis=1)

    # Check if has profile picture
    default_profile_pic = "https://storage.googleapis.com/kumsia-storage/placeholder/user.jpg"
    df["has_profile_pic"] = df.apply(lambda x: 1 if x.profile_picture != default_profile_pic else 0, axis=1)
    # Drop unused columns
    preprocessed_df = df.drop(["preference_id", "username", "name", "password", "email", "contact",
                            "guardian_contact", "profile_picture", "dob", "last_activity", "hobby",
                            "religion", "gender", "city", "is_new_user"], axis=1)
    # Standardization only on age and offline days
    scaler = StandardScaler()
    preprocessed_df[["age", "days_offline"]] = scaler.fit_transform(preprocessed_df[["age", "days_offline"]])
    # Get User DF and drop user logged in from preprocessed df
    user_df = preprocessed_df.loc[preprocessed_df["user_id"] == user_id]
    neighbors_df = preprocessed_df.loc[preprocessed_df["user_id"] != user_id]
    # drop id
    neighbors_df = neighbors_df.drop(["user_id"], axis=1)
    user_df = user_df.drop(["user_id"], axis=1)
    # Neighbours Model
    n_neighbors = len(neighbors_df) 
    if len(neighbors_df) > 15:
        n_neighbors = 15
    knn = NearestNeighbors(n_neighbors=n_neighbors, algorithm='auto').fit(neighbors_df)
    _, indices = knn.kneighbors(user_df)
    top_n_index = indices[0]
    top_n_user = df.iloc[top_n_index]

    # if more than 5 reccommended accounts, pick random 5
    if n_neighbors > 6:
        top_n_user = top_n_user[top_n_user["user_id"] != user_id].sample(6)

    recommended_users = []
    for _, row in top_n_user.iterrows():
        recommended_users.append(response_schema.User(user_id=row["user_id"],
                                                      username=row["username"],
                                                      name=row["name"],
                                                      dob=row["dob"].strftime("%Y-%m-%d"),
                                                      profile_picture=row["profile_picture"],
                                                      religion=row["religion"],
                                                      gender=row["gender"],
                                                      city=row["city"],
                                                      hobbies=row["hobby"],
                                                    )
                                )
    return response_schema.UsersList(users=recommended_users)