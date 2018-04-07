from . import constants

def getSubjectsOfVerb(verb):
    subjs = [token for token in verb.lefts
             if token.dep_ in constants.SUBJ_DEPS]
    # get additional conjunct subjects
    subjs.extend(token for subj in subjs for token in getConjuncts(subj))
    return subjs
    
def getObjectsOfVerb(verb):
    objs = [token for token in verb.rights
            if token.dep_ in constants.OBJ_DEPS]
    # get open clausal complements (xcomp)
    objs.extend(token for token in verb.rights
                if token.dep_ == 'xcomp')
    # get additional conjunct objects
    objs.extend(token for obj in objs for token in getConjuncts(obj))
    return objs

def getConjuncts(token):
    return [right for right in token.rights
            if right.dep_ == 'conj']