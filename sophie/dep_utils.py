from . import constants

def get_subjects_of_verb(verb):
    if _is_verb_passive(verb):
        deps = verb.rights
    else:
        deps = verb.lefts
    
    subjs = []
    
    for token in deps:
        if token.dep_ in constants.SUBJ_DEPS:
            if token.dep_ == 'agent':
                for token_right in token.rights:
                    if token_right.dep_ == 'pobj':
                        subjs.append(token_right)
                        break
            else:
                subjs.append(token)
    
    # get additional conjunct subjects
    subjs.extend(token for subj in subjs for token in _get_conjuncts(subj))
    return subjs
    
def get_objects_of_verb(verb):
    if _is_verb_passive(verb):
        deps = verb.lefts
    else:
        deps = verb.rights
        
    objs = [token for token in deps
            if token.dep_ in constants.OBJ_DEPS]
    
    # get additional conjunct objects
    objs.extend(token for obj in objs for token in _get_conjuncts(obj))
    return objs

def _get_conjuncts(token):
    return [right for right in token.rights
            if right.dep_ == 'conj']
    
def _is_verb_passive(verb):
    for left in verb.lefts:
        if left.dep_ == 'auxpass':
            return True
    
    return False