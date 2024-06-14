
from . import response_schema
from app.utils.database import create_connection

conn = create_connection()
cur = conn.cursor()

def get_master_hobby():
    cur.execute("SELECT * FROM master_hobby;")
    hobby = [h["hobby"] for h in cur.fetchall()]

    return response_schema.HobbyList(Hobbies=hobby)

def get_master_city():
    cur.execute("SELECT * FROM master_city;")
    city = [c["city"] for c in cur.fetchall()]

    return response_schema.CityList(Cities=city)