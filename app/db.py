from fastapi.encoders import jsonable_encoder
from typing import List
import datetime

from prisma import Prisma
from prisma.models import Temp, LastTemp
from temp import Temp as TempClass

prisma = Prisma(auto_register=True)

class Db:
    async def connect(self):
        await prisma.connect()

    async def disconnect(self):
        await prisma.disconnect()

    async def add_temp(self, temp: TempClass):
        await Temp.prisma().create(data=jsonable_encoder(temp))

    async def add_last_temp(self, temp: TempClass):
        last_temp = await LastTemp.prisma().find_first()
        if last_temp is None:
            await LastTemp.prisma().create(data=jsonable_encoder(temp))
            return
        await LastTemp.prisma().update(where={'id': last_temp.id}, data=jsonable_encoder(temp)) #type: ignore

    async def get_temps(self, m: int, d: int) -> List[Temp]:
        return await Temp.prisma().find_many(where={'m': m, 'd': d})

    async def last_temp(self) -> LastTemp | None:
        return await LastTemp.prisma().find_first()

    async def last_days(self, days: int) -> List[Temp]:
        now = datetime.datetime.now()
        before = now - datetime.timedelta(days)
        before_days: List[int] = []
        now_days: List[int] = []
        for i in range(0, days):
            date = now - datetime.timedelta(days=i)
            if date.month == before.month:
                now_days.append(date.day)
            else:
                before_days.append(date.day)
        return await Temp.prisma().find_many(where={
            "OR": [
                {"d": {"in": now_days}, "m": now.month},
                {"d": {"in": before_days}, "m": before.month}
            ]
        })
