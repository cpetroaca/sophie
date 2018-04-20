class Entity:
    def __init__(self, text, type):
        self._text = text
        self._type = type
    
    @property
    def text(self):
        return self._text
    
    @property
    def type(self):
        return self._type
    
    def __eq__(self, other):
        return self._text == other._text and self._type == other._type
    
class Relation:
    def __init__(self, subj, type, obj):
        self._subj = subj
        self._type = type
        self._obj = obj
        
    @property
    def subj(self):
        return self._subj
    
    @property
    def type(self):
        return self._type
    
    @property
    def obj(self):
        return self._obj
    
    def __eq__(self, other):
        return self._subj == other._subj and self._type == other._type and self._obj == other._obj