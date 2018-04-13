import unittest
import spacy
from sophie import Extractor

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
            self.assertEqual(relation[0], doc[0:2])
            self.assertEqual(relation[1], 'visit')
            self.assertEqual(relation[2], doc[3:4])

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
    
if __name__ == '__main__':
    unittest.main()