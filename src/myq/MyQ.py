import asyncio
import os

import pymyq
from aiohttp import ClientSession


class MyQ:
    def __init__(self, user: str = '', pwd: str = ''):
        self.user = user if user else os.environ.get('MYQ_USER')
        self.pwd = pwd if pwd else os.environ.get('MYQ_PASS')
        if not (self.user and self.pwd):
            raise ValueError('Username and Password params are not properly defined.')
        self.legend = {}
        self.get_garage_doors()
        self.myq = None
        self.web_session = ClientSession()

    async def get_garage_doors(self) -> dict:
        self.myq = await pymyq.login(self.user, self.pwd, self.web_session)
        garage_doors = self.myq.covers
        for id, door in garage_doors.items():
            self.legend[door.name] = dict(id=id, state=door.state)
        return self.legend

    async def open_garage_door(self, name: str) -> bool:
        id = self.legend.get(name).get('id')
        state = await self.myq.covers.get(id).open()
        return state

    async def close_garage_door(self, name: str) -> bool:
        id = self.legend.get(name).get('id')
        state = await self.myq.covers.get(id).close()
        return state


if __name__ == '__main__':
    my_q = MyQ('', '')
    asyncio.get_event_loop().run_until_complete(my_q.get_garage_doors())
    asyncio.get_event_loop().run_until_complete(my_q.open_garage_door('Grass'))
    asyncio.get_event_loop().run_until_complete(my_q.close_garage_door('Grass'))
