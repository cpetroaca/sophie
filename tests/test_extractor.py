import unittest
import spacy
from sophie import Extractor
from sophie import Entity

class TestRelationsExtraction(unittest.TestCase):
    def setUp(self):
        self.spacyNlp = spacy.load('en_core_web_sm')
        self.extractor = Extractor()
        
        super(TestRelationsExtraction, self).setUp()
        
    def test_simple_relation(self):
        text = 'Barack Obama visited China.'
        
        relations = self.extractor.get_relations(text)
        doc = self.spacyNlp(text)
        
        for relation in relations:
            self.assertEqual(relation.subj, Entity('Barack Obama', 'PERSON'))
            self.assertEqual(relation.type, 'visit')
            self.assertEqual(relation.obj, Entity('China', 'GPE'))

    def test_negation(self):
        text = 'Barack Obama did not visit China.'
        
        relations = self.extractor.get_relations(text)
        relation_number = 0
        
        for relation in relations:
            relation_number += 1
            
        self.assertEqual(relation_number, 0)
    
    def test_modal_verb(self):
        text = 'Barack Obama should visit China.'
        
        relations = self.extractor.get_relations(text)
        relation_number = 0
        
        for relation in relations:
            relation_number += 1
            
        self.assertEqual(relation_number, 0)
    
    def test_no_ners(self):
        text = 'I visited another country.'
        
        relations = self.extractor.get_relations(text)
        relation_number = 0
        
        for relation in relations:
            relation_number += 1
            
        self.assertEqual(relation_number, 0)
    
    def test_multiple_sentences(self):
        text = 'Barack Obama visited China. Microsoft bought Intel.'
        
        relations = self.extractor.get_relations(text)
        doc = self.spacyNlp(text)
        relation_cnt = 0
        for relation in relations:
            relation_cnt += 1
            
            if relation_cnt == 1:
                self.assertEqual(relation.subj, Entity('Barack Obama', 'PERSON'))
                self.assertEqual(relation.type, 'visit')
                self.assertEqual(relation.obj, Entity('China', 'GPE'))
            
            if relation_cnt == 2:
                self.assertEqual(relation.subj, Entity('Microsoft', 'ORG'))
                self.assertEqual(relation.type, 'buy')
                self.assertEqual(relation.obj, Entity('Intel', 'ORG'))
    
    def test_passive_verb(self):
        text = 'Microsoft was bought by Intel.'
        
        relations = self.extractor.get_relations(text)
        
        doc = self.spacyNlp(text)
        
        for relation in relations:
            self.assertEqual(relation.subj, Entity('Intel', 'ORG'))
            self.assertEqual(relation.type, 'buy')
            self.assertEqual(relation.obj, Entity('Microsoft', 'ORG'))
    
    def test_conjuncts(self):
        text = 'Barack Obama and Angela Merkel visited China and South Korea.'
        
        relations = self.extractor.get_relations(text)
        doc = self.spacyNlp(text)
        
        cnt = 0
        for relation in relations:
            cnt += 1
            
            if cnt == 1:
                self.assertEqual(relation.subj, Entity('Barack Obama', 'PERSON'))
                self.assertEqual(relation.type, 'visit')
                self.assertEqual(relation.obj, Entity('China', 'GPE'))
            elif cnt == 2:
                self.assertEqual(relation.subj, Entity('Barack Obama', 'PERSON'))
                self.assertEqual(relation.type, 'visit')
                self.assertEqual(relation.obj, Entity('South Korea', 'GPE'))
            elif cnt == 3:
                self.assertEqual(relation.subj, Entity('Angela Merkel', 'PERSON'))
                self.assertEqual(relation.type, 'visit')
                self.assertEqual(relation.obj, Entity('China', 'GPE'))
            elif cnt == 4:
                self.assertEqual(relation.subj, Entity('Angela Merkel', 'PERSON'))
                self.assertEqual(relation.type, 'visit')
                self.assertEqual(relation.obj, Entity('South Korea', 'GPE'))

    def test_only_one_ner_in_subj(self):
        text = 'Barack Obama greeted the chancellor.'
        
        relations = self.extractor.get_relations(text)
        doc = self.spacyNlp(text)
        
        for relation in relations:
            self.assertEqual(relation.subj, Entity('Barack Obama', 'PERSON'))
            self.assertEqual(relation.type, 'greet')
            self.assertEqual(relation.obj, Entity('chancellor', ''))
            
    def test_only_one_ner_in_obj(self):
        text = 'The chancellor greeted Barack Obama.'
        
        relations = self.extractor.get_relations(text)
        doc = self.spacyNlp(text)
        
        for relation in relations:
            self.assertEqual(relation.subj, Entity('chancellor', ''))
            self.assertEqual(relation.type, 'greet')
            self.assertEqual(relation.obj, Entity('Barack Obama', 'PERSON'))

if __name__ == '__main__':
    unittest.main()