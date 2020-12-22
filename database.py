from desk import Desk


class Database:
    def __init__(self):
        self.desks = {}
        self._last_desk_key = 0

    def add_desk(self, desk):
        self._last_desk_key += 1
        self.desks[self._last_desk_key] = desk
        return self._last_desk_key

    def update_desk(self, desk_key, desk):
        self.desks[desk_key] = desk

    def delete_desk(self, desk_key):
        if desk_key in self.desks:
            del self.desks[desk_key]

    def get_desk(self, desk_key):
        desk = self.desks.get(desk_key)
        if desk is None:
            return None
        desk_ = Desk(desk.deskName)
        return desk_

    def get_desks(self):
        desks = []
        for desk_key, desk in self.desks.items():
            desk_ = Desk(desk.deskName)
            desks.append((desk_key, desk_))
        return desks