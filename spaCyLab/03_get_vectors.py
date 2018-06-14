import json
import spacy

def get_vectors(wordlist):
    tokens = nlp(" ".join(str(s) for s in wordlist))
    pageVec = []
    for token in tokens:
        wordVec = token.vector
        print(type(wordVec))
        pageVec.append(wordVec[0])
    return pageVec

# JSON export of the lemmatized words per each page
wd = "C:\\Users\\bmareddy\\Documents\\PyLab"
inFile = wd+"\\MCG-Archive_tags_tfidf.json"
outFile = wd+"\\MCG-Archive_tags_vectors.json"

try:
    pageTopWords = open(inFile,"r").read().splitlines()
    pageTopWords = [json.loads(ptw) for ptw in pageTopWords]
    nlp = spacy.load("en_core_web_lg") # Load English language LARGE model; there is also another model explicitly for vectors
    for ptw in pageTopWords:
        pass
    print(ptw["words"],get_vectors(ptw["words"]))
except Exception as e:
    print(e)
finally:
    print("The End")