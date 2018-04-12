import unittest
import spacy
from sophie import Extractor

class TestRelationsExtraction(unittest.TestCase):
    def test_simple_relation(self):
        text = 'Barack Obama visited China'
        nlp = spacy.load('en_core_web_sm')
        extractor = Extractor()
        
        relations = extractor.get_relations(text)
        doc = nlp(text)
        
        for relation in relations:
            self.assertEqual(relation[0], doc[0:2])
            self.assertEqual(relation[1], 'visit')
            self.assertEqual(relation[2], doc[3:4])

if __name__ == '__main__':
    unittest.main()