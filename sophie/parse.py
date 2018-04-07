import spacy
from . import dep_utils

class Extractor:
    def __init__(self, model='en_core_web_sm'):
        self.nlp = spacy.load(model)
        print("Loaded model '%s'" % model)
    
    def get_relations(self, text):
        doc = self.nlp(text)
        sents = doc.sents
        ents = doc.ents
        
        for sent in sents:
            for token in sent:
                if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                    verb = token.lemma_
                    subjs = dep_utils.get_subjects_of_verb(token)
                    if not subjs:
                        continue
                    objs = dep_utils.get_objects_of_verb(token)
                    if not objs:
                        continue
                    
                    for subj in subjs:
                        for obj in objs:
                            subj_ner_span = self.get_ner_span(ents, subj)
                            obj_ner_span = self.get_ner_span(ents, obj)
                            
                            if (subj_ner_span is not None and obj_ner_span is not None):
                                yield (subj_ner_span, verb, obj_ner_span)
    
    def get_ner_span(self, ents, token):
        for ent in ents:
            if token.i >= ent.start and token.i <= ent.end:
                return ent
        return None