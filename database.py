from desk import Desk, Flashcard, Language
from user import User
from datetime import datetime, timedelta

def strfdelta(tdelta):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    return d

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_desk(self, desk, userID, languageID):
        query = "INSERT INTO desk (deskName, languageID) VALUES ( %s, %s) RETURNING deskID"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (desk.deskName, languageID))
        deskID = cursor.fetchone()[0]
        query = "INSERT INTO userdesks (userID, deskID) VALUES ( %s, %s)"
        cursor.execute(query, (userID, deskID))
        self.dbfile.commit()
        return deskID

    def update_desk(self, deskID, desk, languageID):
        query = "UPDATE desk SET deskName = %s, languageID = %s WHERE (deskID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (desk.deskName, languageID, deskID))
        self.dbfile.commit()

    def delete_desk(self, deskID):
        query = """
                DELETE FROM flashcard WHERE flashID IN( SELECT flashID FROM cardsindesks WHERE deskID = %s);
                DELETE FROM desk WHERE (deskID = %s);"""
        cursor = self.dbfile.cursor()
        cursor.execute(query, ( deskID, deskID))
        self.dbfile.commit()

    def get_desk(self, deskID):
        query = "SELECT deskName, languageID FROM desk WHERE (deskID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (deskID, ))
        deskinfo = cursor.fetchone()
        desk = (Desk(deskinfo[0]), deskinfo[1])
        return desk

    def get_desks(self, ID):
        desks = []
        query = "SELECT deskID, deskName, languageID FROM desk NATURAL JOIN userdesks WHERE (userID = %s) ORDER BY deskID"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (ID, ))
        for deskID, deskName, languageID in cursor:
            if languageID is not None:
                langstr = self.get_language(languageID)
            else:
                langstr = ""
            desk = Desk(deskName)
            desks.append((deskID, desk, langstr))
        return desks

    def check_userdesk(self, deskID, userID):
        query = "SELECT deskID, deskName, languageID FROM desk NATURAL JOIN userdesks WHERE (deskID = %s AND userID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (deskID, userID))
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def search_desks(self, search):
        desks = []
        query = "SELECT * FROM desk WHERE deskName LIKE %s"
        cursor = self.dbfile.cursor()
        search = '%'+search+'%'
        cursor.execute(query, (search, ))
        for deskID, deskName, languageID in cursor:
            if languageID is not None:
                langstr = self.get_language(languageID)
            else:
                langstr = ""
            desk = Desk(deskName)
            desks.append((deskID, desk, langstr))
        return desks

    def share_desk(self, deskID, userID):
        query = "INSERT INTO userdesks (deskID, userID) VALUES ( %s, %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (deskID, userID))
        self.dbfile.commit()

    def check_user(self, nickName, mail):
        query = "SELECT * FROM useraccount WHERE (nickname = %s) UNION SELECT * FROM useraccount WHERE (mail = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (nickName, mail))
        if cursor.fetchone() == None:
            return False
        else:
            return True
    
    def add_user(self, username, passwordHash, mail, firstName, lastName):
        query = "INSERT INTO useraccount (nickName, mail, passwordHash, firstName, lastName) VALUES ( %s, %s, %s, %s, %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (username, mail, passwordHash,firstName, lastName))
        self.dbfile.commit()
    
    def update_user(self, username, passwordHash, mail, firstName, lastName, userID):
        query = "UPDATE useraccount SET nickName = %s, mail = %s, passwordHash = %s, firstName = %s, lastName = %s WHERE (userID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (username, mail, passwordHash, firstName, lastName, userID))
        self.dbfile.commit()

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
            user = User(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5])
        except:
            user = None
        return user

    def add_card(self, card, deskID):
        query = "INSERT INTO flashcard (word, translation, languageID, image, wordform) VALUES (%s, %s, NULL, %s, %s) RETURNING flashID"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (card.word, card.translation, card.image, card.wordform))
        flashID = cursor.fetchone()[0]
        query = "INSERT INTO cardsindesks (deskID, flashID) VALUES ( %s, %s)"
        cursor.execute(query, (deskID, flashID))
        self.dbfile.commit()
        return flashID

    def get_cards(self, deskID):
        cards = []
        query = "SELECT flashID, word, translation, image, wordform FROM flashcard NATURAL JOIN cardsindesks WHERE (deskID = %s) ORDER BY flashID"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (deskID, ))
        for flashID, word, translation, image, wordform in cursor:
                card = Flashcard(word, translation, image, wordform)
                cards.append((flashID, card))
        return cards

    def get_card(self, flashID):
        query = "SELECT word, translation, image, wordform FROM flashcard WHERE (flashID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (flashID, ))
        data = cursor.fetchone()
        card = Flashcard(data[0], data[1], data[2], data[3])
        return card
    
    def update_card(self, flashID, card):
        query = "UPDATE flashcard SET word = %s, translation = %s, image = %s, wordform = %s WHERE (flashID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (card.word, card.translation, card.image, card.wordform, flashID))
        self.dbfile.commit()

    def delete_card(self, flashID, deskID):
        query = """DELETE FROM flashcard WHERE (flashID = %s);
                DELETE FROM cardsindesks WHERE (flashID = %s AND deskID = %s);
                DELETE FROM studystats WHERE (flashID = %s) """
        cursor = self.dbfile.cursor()
        cursor.execute(query, (flashID, flashID, deskID, flashID))
        self.dbfile.commit()

    def study_card(self, flashID, userID):
        query = "SELECT repetition FROM studystats WHERE (userID = %s AND flashID = %s)"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (userID, flashID))
        repetition = cursor.fetchone()
        if repetition == None:
            query = "INSERT INTO studystats (userID, flashID, studytimestamp, repetition) VALUES (%s, %s, %s, 1)"
            cursor.execute(query, (userID, flashID, datetime.now()))
        else:
            query = "UPDATE studystats SET studytimestamp = %s, repetition = %s WHERE (userID = %s AND flashID = %s)"
            cursor.execute(query, (datetime.now(), int(repetition[0])+1, userID, flashID))
        self.dbfile.commit()

    def get_words(self, userID):
        words = []
        query = "SELECT word, wordform, studytimestamp, repetition FROM studystats NATURAL JOIN flashcard WHERE (userID = %s) ORDER BY studytimestamp"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (userID, ))
        for word, wordform, studytimestamp, repetition in cursor:
            timepassed = strfdelta( datetime.now() - studytimestamp)
            if timepassed["D"] > 0:
                if timepassed["D"] == 1:
                    timestr = "Yesterday"
                else:
                    timestr = str(timepassed["D"]) + " days ago"
            elif timepassed["H"] > 0:
                if timepassed["H"] == 1:
                    timestr = "1 hour ago"
                else:
                    timestr = str(timepassed["H"]) + " hours ago"
            elif timepassed["M"] > 0:
                if timepassed["M"] == 1:
                    timestr = "1 minute ago"
                else:
                    timestr = str(timepassed["M"]) + " minutes ago"
            else:
                if timepassed["S"] == 1:
                    timestr = "1 second ago"
                else:
                    timestr = str(timepassed["S"]) + " seconds ago"
            words.append((word, wordform, timestr, repetition ))
        return words

    def get_languages(self):
        languages = []
        query = "SELECT languageID, fromLanguage, toLanguage FROM languages"
        cursor = self.dbfile.cursor()
        cursor.execute(query)
        for languageID, fromLanguage, toLanguage in cursor:
                language = Language(languageID, fromLanguage, toLanguage)
                languages.append(language)
        return languages
    
    def get_language(self, languageID):
        query = "SELECT fromLanguage, toLanguage FROM languages WHERE languageID = %s"
        cursor = self.dbfile.cursor()
        cursor.execute(query, (languageID, ))
        temp = cursor.fetchone()
        langstr = temp[0] + " to " + temp[1]
        return langstr