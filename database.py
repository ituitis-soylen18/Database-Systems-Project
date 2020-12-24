from desk import Desk

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_desk(self, desk):
        query = "INSERT INTO desk (deskName, languageID) VALUES ( %s, NULL) RETURNING deskID"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (desk.deskName,))
        self.dbfile.commit()
        deskID = cursor.fetchone()[0]
        return deskID

    def update_desk(self, deskID, desk):
        query = "UPDATE desk SET deskName = %s WHERE (deskID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (desk.deskName, deskID))
        self.dbfile.commit()

    def delete_desk(self, deskID):
        query = "DELETE FROM desk WHERE (deskID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (deskID, ))
        self.dbfile.commit()

    def get_desk(self, deskID):
        query = "SELECT deskName FROM desk WHERE (deskID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (deskID, ))
        deskName = cursor.fetchone()
        desk = Desk(deskName)
        return desk

    def get_desks(self):
        desks = []
        query = "SELECT deskID, deskName FROM desk ORDER BY deskID"
        cursor = self.dbfile.cursor()
        cursor.execute(query)
        for deskID, deskName in cursor:
                desk = Desk(deskName)
                desks.append((deskID, desk))
        return desks