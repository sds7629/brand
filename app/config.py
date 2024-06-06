class Config:
    populate_by_name = True
    arbitrary_types_allowed = True


import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

ACCESS_TOKEN_EXFIRE = os.environ.get("ACCESS_TOKEN_EXFIRES")
REFRESH_TOKEN_EXFIRE = os.environ.get("REFRESH_TOKEN_EXFIRES")
REFRESH_SECRET_KEY = os.environ.get("REFRESH_SECRET_KEY")
ACCESS_SECRET_KEY = os.environ.get("ACCESS_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

KAKAO_REST_API_KEY = os.environ.get("KAKAO_REST_API_KEY")
PORT_ONE_SECRET_KEY = os.environ.get("PORT_ONE_V2_SECRET_KEY")
