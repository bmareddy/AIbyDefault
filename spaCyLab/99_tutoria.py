import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(u'My name is Bobby Mareddy')
# for token in doc:
#     print(token.text)

for ent in doc.ents:
    print(ent.text,ent.label_)
