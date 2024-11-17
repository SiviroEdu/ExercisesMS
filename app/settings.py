import os

import aiohttp
from cryptography.fernet import Fernet

SERVICE_KEY = os.environ["SERVICE_KEY"]

db_url = os.environ["DB_URL"]
session = aiohttp.ClientSession()
