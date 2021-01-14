from desk import Desk, Flashcard
from user import User

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_desk(self, desk, userID):
        query = "INSERT INTO desk (deskName, languageID) VALUES ( %s, NULL) RETURNING deskID"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (desk.deskName,))
        deskID = cursor.fetchone()[0]
        query = "INSERT INTO userdesks (userID, deskID) VALUES ( %s, %s)"
        cursor.execute(query, (userID, deskID))
        self.dbfile.commit()
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

    def get_desks(self, ID):
        desks = []
        query = "SELECT deskID, deskName FROM desk NATURAL JOIN userdesks WHERE (userID = %s) ORDER BY deskID"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (ID, ))
        for deskID, deskName in cursor:
                desk = Desk(deskName)
                desks.append((deskID, desk))
        return desks

    def check_username(self, nickName):
        return False
    
    def check_usermail(self, mail):
        return False
    
    def add_user(self, username, passwordHash, mail, firstName, lastName):
        query = "INSERT INTO useraccount (nickName, mail, passwordHash, firstName, lastName) VALUES ( %s, %s, %s, %s, %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (username, mail, passwordHash,firstName, lastName))
        self.dbfile.commit()
    
    """ def get_user(self, userID):
        query = "SELECT nickName, mail, passwordHash, firstName, lastName FROM useraccount WHERE (userID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (userID, ))
        user_info = cursor.fetchone()
        user = User(user_info[1], user_info[2], user_info[3], user_info[4], user_info[5])
        return user
     """
    def get_users(self):
        users = []
        query = "SELECT userID, nickName, mail, passwordHash, firstName, lastName FROM useraccount ORDER BY userID"
        cursor = self.dbfile.cursor()
        cursor.execute(query)
        for userID, nickName, mail, passwordHash, firstName, lastName in cursor:
                user = User(nickName, mail, passwordHash, firstName, lastName)
                users.append((userID, user))
        return users

    def load_user(self, nickName):
        query = "SELECT nickName, passwordHash, mail, firstName, lastName, userID FROM useraccount WHERE (nickName = %s)"
        cursor = self.dbfile.cursor()
        try:
            cursor.execute(query, (nickName,))
            user_info = cursor.fetchone()
            print("-----info-------------",user_info)
            user = User(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5])
        except:
            user = None
        return user

    def add_card(self, card, deskID):
        query = "INSERT INTO flashcard (word, translation, languageID) VALUES (%s, %s, NULL) RETURNING flashID"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (card.word, card.translation))
        flashID = cursor.fetchone()[0]
        query = "INSERT INTO cardsindesks (deskID, flashID) VALUES ( %s, %s)"
        cursor.execute(query, (deskID, flashID))
        self.dbfile.commit()
        return flashID

    def get_cards(self, deskID):
        cards = []
        query = "SELECT flashID, word, translation FROM flashcard NATURAL JOIN cardsindesks WHERE (deskID = %s) ORDER BY flashID"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (deskID, ))
        for flashID, word, translation in cursor:
                card = Flashcard(word, translation)
                cards.append((flashID, card))
        return cards

    def get_card(self, flashID):
        query = "SELECT word, translation FROM flashcard WHERE (flashID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (flashID, ))
        data = cursor.fetchone()
        card = Flashcard(data[0], data[1])
        return card
    
    def update_card(self, flashID, card):
        query = "UPDATE flashcard SET word = %s, translation = %s WHERE (flashID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (card.word, card.translation, flashID))
        self.dbfile.commit()

    def delete_card(self, flashID, deskID):
        query = """DELETE FROM flashcard WHERE (flashID = %s);
                DELETE FROM cardsindesks WHERE (flashID = %s AND deskID = %s) """
        cursor = self.dbfile.cursor()
        cursor.execute(query, (flashID, flashID, deskID))
        self.dbfile.commit()