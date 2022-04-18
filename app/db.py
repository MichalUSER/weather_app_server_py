from fastapi.encoders import jsonable_encoder
from typing import List
import os
import datetime
from dataclasses import dataclass
from devtools import debug

from prisma import Prisma
from prisma.models import Temp, LastTemp

prisma = Prisma(auto_register=True)

class Db:
    async def connect(self):
        await prisma.connect()

    async def disconnect(self):
        await prisma.disconnect()

    async def add_temp(self, temp):
        debug(temp)
        await Temp.prisma().create(data=temp)

    async def add_last_temp(self, temp):
        last_temp = await LastTemp.prisma().find_first(where={})
        await LastTemp.prisma().update(where={'id': last_temp.id}, data=temp)

    def get_temps(self, m: int, d: int) -> List[Temp]:
        search: List[Temp] = []
        for t in self.temps_coll.find({"m": m, "d": d}):
            temp = Temp(**t)
            search.append(temp)
        return search

    def last_temp(self) -> Temp:
        t = self.last_temp_coll.find_one()
        return Temp(**t) #type: ignore

    def last_days(self, days: int) -> List[Temp]:
        now = datetime.datetime.now()
        before = now - datetime.timedelta(days)
        before_days: List[int] = []
        now_days: List[int] = []
        for i in range(0, days):
            date = now - datetime.timedelta(days=i)
            if date.month == before.month:
                before_days.append(date.day)
            else:
                now_days.append(date.day)
        search: List[Temp] = []
        for t in self.temps_coll.find({"d": {"$in": now_days}, "m": now.month}):
            temp = Temp(**t)
            search.append(temp)
        for t in self.temps_coll.find({"d": {"$in": before_days}, "m": before.month}):
            temp = Temp(**t)
            search.append(temp)
        return search
