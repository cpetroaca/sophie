import spacy
from . import dep_utils
from . import constants
from .relations import Relation
from .relations import Entity

class Extractor:
    def __init__(self, model='en_core_web_sm', ner_types=set(['PERSON', 'NORP', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'MONEY'])):
        self.nlp = spacy.load(model)
        self.ner_types = ner_types
        print("Loaded model '%s'" % model)
    
    def get_relations(self, text):
        doc = self.nlp(text)
        sents = doc.sents
        ents = doc.ents
        
        for sent in sents:
            for token in sent:
                if self._is_valid_verb(token):
                    verb = token.lemma_
                    subjs = dep_utils.get_subjects_of_verb(token)
                    if not subjs:
                        continue
                    objs = dep_utils.get_objects_of_verb(token)
                    if not objs:
                        continue
                    
                    for subj in subjs:
                        for obj in objs:
                            subj_ner_span = self._get_ner_span(ents, subj)
                            obj_ner_span = self._get_ner_span(ents, obj)
                            
                            if (subj_ner_span is not None and obj_ner_span is not None):
                                subj_entity = Entity(subj_ner_span.text, subj_ner_span.label_)
                                obj_entity = Entity(obj_ner_span.text, obj_ner_span.label_)
                                yield Relation(subj_entity, verb, obj_entity)
    
    def _get_ner_span(self, ents, token):
        for ent in ents:
            if ent.label_ in self.ner_types and token.i >= ent.start and token.i <= ent.end:
                return ent
        return None
    
    def _is_valid_verb(self, token):
        if token.dep_ != 'ROOT' or token.pos_ != 'VERB':
            return False
        
        for left in token.lefts:
            if left.dep_ in constants.NEG or left.tag_ == 'MD':
                return False
        
        return True