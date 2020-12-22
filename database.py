from desk import Desk

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_desk(self, desk):
        query = "INSERT INTO desk (deskID, deskName) VALUES (DEFAULT, %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (desk.deskName,))
        self.dbfile.commit()
        desk_key = cursor.lastrowid
        return desk_key

    def update_desk(self, desk_key, desk):
        query = "UPDATE desk SET deskName = %s WHERE (deskID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (desk.deskName, desk_key))
        self.dbfile.commit()

    def delete_desk(self, desk_key):
        query = "DELETE FROM desk WHERE (deskID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (desk_key, ))
        self.dbfile.commit()

    def get_desk(self, desk_key):
        query = "SELECT deskName FROM desk WHERE (deskID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (desk_key, ))
        self.dbfile.commit()

    def get_desks(self):
        desks = []
        query = "SELECT deskID, deskName FROM desk ORDER BY deskID"
        cursor = self.dbfile.cursor()
        cursor.execute(query)
        self.dbfile.commit()
        for deskID, deskName in cursor:
                desks.append((deskID, deskName))
        return desks