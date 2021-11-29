'''
https://spacy.io/usage/
https://spacy.io/usage/linguistic-features
https://spacy.io/models/

https://textminingonline.com/getting-started-with-spacy
https://stackoverflow.com/questions/38763007/how-to-use-spacy-lemmatizer-to-get-a-word-into-basic-form
'''

'''
preparation:
>>> python3 -m spacy download en
'''

import spacy

nlp = spacy.load('en_core_web_sm')
msg = 'Apple is looking at buying U.K. startup for $1 billion.'
print('=>', msg)
doc = nlp(msg)
for tok in doc:
    print('{:<10s}'.format(tok.text), '|lemma', tok.lemma_, '|pos', tok.pos_,
            '|tag', tok.tag_)
    print(' '*10, '|dep', tok.dep_, '|shape', tok.shape_, '|alpha', tok.is_alpha,
            '|stop', tok.is_stop, '|')
