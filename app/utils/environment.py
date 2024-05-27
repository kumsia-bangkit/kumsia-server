import os
from dotenv import load_dotenv

load_dotenv()

ALGORITHM=os.getenv("ALGORITHM")
SECRET_KEY=os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_DAYS=os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")