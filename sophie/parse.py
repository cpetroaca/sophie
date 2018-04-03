import spacy

class Extractor:
    def __init__(self, model='en_core_web_sm'):
        self.nlp = nlp = spacy.load(model)
        print("Loaded model '%s'" % model)
    
    def getNers(self, text):
        doc = self.nlp(text)
        return doc.ents
