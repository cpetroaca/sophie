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
                            subj_entity = self._create_relation_entity(subj, subj_ner_span)
                            obj_entity = self._create_relation_entity(obj, obj_ner_span)
                            
                            if (subj_entity is not None and obj_entity is not None 
                                and (subj_ner_span is not None or obj_ner_span is not None)):
                                yield Relation(subj_entity, verb, obj_entity)
                            
    def _get_ner_span(self, ents, token):
        for ent in ents:
            if ent.label_ in self.ner_types and token.i >= ent.start and token.i <= ent.end:
                return ent
        return None
    
    def _is_valid_verb(self, token):
        if token.dep_ != 'ROOT' or token.pos_ != 'VERB':
            return False
        
        #no negated or modal verbs
        for left in token.lefts:
            if left.dep_ in constants.NEG or left.tag_ == 'MD':
                return False
        
        return True
    
    def _create_relation_entity(self, token, ner):
        if (ner is not None):
            return Entity(ner.text, ner.label_)
        else:
            if (token.pos_ == 'NOUN'):
                return Entity(token.text, '')
        
        return None
        