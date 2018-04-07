from . import constants

def get_subjects_of_verb(verb):
    subjs = [token for token in verb.lefts
             if token.dep_ in constants.SUBJ_DEPS]
    # get additional conjunct subjects
    subjs.extend(token for subj in subjs for token in _get_conjuncts(subj))
    return subjs
    
def get_objects_of_verb(verb):
    objs = [token for token in verb.rights
            if token.dep_ in constants.OBJ_DEPS]
    # get open clausal complements (xcomp)
    objs.extend(token for token in verb.rights
                if token.dep_ == 'xcomp')
    # get additional conjunct objects
    objs.extend(token for obj in objs for token in _get_conjuncts(obj))
    return objs

def _get_conjuncts(token):
    return [right for right in token.rights
            if right.dep_ == 'conj']