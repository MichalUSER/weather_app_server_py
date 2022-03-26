import asyncio
import random
import datetime
from prisma import Prisma

async def main() -> None:
    db = Prisma(auto_register=True)
    await db.connect()

    lower = random.uniform(21, 22.5)
    upper = random.uniform(22.5, 24.5)
    temp = random.uniform(lower, upper)
    now = datetime.datetime.now()

    await db.temp.create(
        data={
            'y': now.year,
            'm': now.month,
            'd': now.day,
            'h': now.hour,
            'averageTemp': str(round(temp, 2))
        }
    )

    await db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
