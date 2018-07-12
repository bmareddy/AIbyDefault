import spacy

nlp = spacy.load('en_core_web_lg')
doc = nlp(u"what is the overall spend in Switzerland last month?")

for token in doc:
    print(token.text, token.)

for ent in doc.ents:
    print(ent.text,ent.label_)
