class Desk:
    def __init__(self, deskName):
        self.deskName = deskName

class Flashcard:
    def __init__(self, word, translation, image, wordform):
        self.word = word
        self.translation = translation
        self.image = image
        self.wordform = wordform

class Language:
    def __init__(self, id, fromLanguage, toLanguage):
        self.id = id
        self.fromLanguage = fromLanguage
        self. toLanguage = toLanguage
