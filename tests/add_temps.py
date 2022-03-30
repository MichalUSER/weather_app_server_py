import requests
import datetime
import random
from dataclasses import dataclass, asdict

URL = "http://localhost:8000"
add_url = "{}/add_temp".format(URL)

@dataclass
class Temp:
    y: int
    m: int
    d: int
    h: int = 0
    averageTemp: str = ""

now = datetime.datetime.now()
data = Temp(now.year, now.month, now.day)

def post_temp(url: str):
    requests.post(url, json=asdict(data))

for i in range (0, 24):
    lower = random.uniform(21, 22.5)
    upper = random.uniform(22.5, 24.5)
    temp = random.uniform(lower, upper)
    data.averageTemp = str(round(temp, 2))
    data.h = i 
    post_temp(add_url)
