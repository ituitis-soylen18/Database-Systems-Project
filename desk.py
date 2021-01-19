class Desk:
    def __init__(self, deskName):
        self.deskName = deskName

class Flashcard:
    def __init__(self, word, translation, image):
        self.word = word
        self.translation = translation
        self.image = image

class Language:
    def __init__(self, id, fromLanguage, toLanguage):
        self.id = id
        self.fromLanguage = fromLanguage
        self. toLanguage = toLanguage
