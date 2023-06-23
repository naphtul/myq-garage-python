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
        self.myq = None
        self.legend = {}
        self.web_session = ClientSession()
        self.event_loop = asyncio.get_event_loop()
        self.refresh_garage_doors()

    def refresh_garage_doors(self) -> dict:
        self.myq = self.event_loop.run_until_complete(pymyq.login(self.user, self.pwd, self.web_session))
        garage_doors = self.myq.covers
        for id, door in garage_doors.items():
            self.legend[door.name] = dict(id=id, state=door.state)
        return self.legend

    def get_garage_doors(self) -> dict:
        if not self.legend:
            return self.refresh_garage_doors()
        return self.legend

    def open_garage_door(self, name: str) -> bool:
        id = self.legend.get(name).get('id')
        res = self.event_loop.run_until_complete(self.myq.covers.get(id).open())
        return True if res._state == 'PENDING' else False

    def close_garage_door(self, name: str) -> bool:
        id = self.legend.get(name).get('id')
        res = self.event_loop.run_until_complete(self.myq.covers.get(id).close())
        return True if res._state == 'PENDING' else False


if __name__ == '__main__':
    my_q = MyQ('', '')
    print(my_q.get_garage_doors())
    my_q.open_garage_door('Grass')
    my_q.close_garage_door('Grass')
