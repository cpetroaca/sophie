import spacy
from . import dep_utils

class Extractor:
    def __init__(self, model='en_core_web_sm'):
        self.nlp = spacy.load(model)
        print("Loaded model '%s'" % model)
    
    def getRelations(self, text):
        doc = self.nlp(text)
        sents = doc.sents
        ents = doc.ents
        
        for sent in sents:
            for token in sent:
                if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                    verb = token.lemma_
                    subjs = dep_utils.getSubjectsOfVerb(token)
                    if not subjs:
                        continue
                    objs = dep_utils.getObjectsOfVerb(token)
                    if not objs:
                        continue
                    
                    for subj in subjs:
                        for obj in objs:
                            subjNerSpan = self.getNerSpan(ents, subj)
                            objNerSpan = self.getNerSpan(ents, obj)
                            
                            if (subjNerSpan is not None and objNerSpan is not None):
                                yield (subjNerSpan, verb, objNerSpan)
    
    def getNerSpan(self, ents, token):
        for ent in ents:
            if token.i >= ent.start and token.i <= ent.end:
                return ent
        return None