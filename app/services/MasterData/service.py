
from . import response_schema
from app.utils.database import create_connection

conn = create_connection()
cur = conn.cursor()

def get_master_hobby():
    cur.execute("SELECT * FROM master_hobby ORDER BY hobby ASC;")
    hobby = [h["hobby"] for h in cur.fetchall()]

    return response_schema.HobbyList(Hobbies=hobby)

def get_master_city():
    cur.execute("SELECT * FROM master_city ORDER BY city ASC;")
    city = [c["city"] for c in cur.fetchall()]

    return response_schema.CityList(Cities=city)