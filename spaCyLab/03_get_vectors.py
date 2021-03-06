import sys, os
import traceback
import json
import spacy
import numpy as np

def get_vectors(wordlist):
    tokens = nlp(" ".join(str(s) for s in wordlist))
    pageVec = np.array([])
    for token in tokens:
        wordVec = token.vector
        wordVec = wordVec.reshape(1,300)
        if pageVec.size == 0:
            pageVec = wordVec
        else:
            pageVec = np.concatenate([pageVec,wordVec],axis = 0)
    return pageVec

def get_weighted_vectors(wordlist, scores):
    tokens = nlp(" ".join(str(s) for s in wordlist))
    pageVec = np.array([])
    for token, score in zip(tokens, scores):
        wordVec = np.multiply(token.vector,np.asarray(score))
        wordVec = wordVec.reshape(1,300)
        if pageVec.size == 0:
            pageVec = wordVec
        else:
            pageVec = np.concatenate([pageVec,wordVec],axis = 0)
        
    return pageVec

# JSON export of the tfidf words & scores per each page
space = "MCG-Archive"
wd = "C:\\Users\\bmareddy\\Documents\\PyLab\\data"
inFile = "{}\\{}_tags_tfidf.json".format(wd,space)
outFile = "{}\\{}_tags_vectors_weighted.json".format(wd,space)

vecs = open(outFile,"w",newline = "\n")
try:
    pageTopWords = open(inFile,"r").read().splitlines()
    pageTopWords = [json.loads(ptw) for ptw in pageTopWords]
    docVector = {}
    nlp = spacy.load("en_vectors_web_lg") # Load English language LARGE model; there is also another model explicitly for vectors
    for ptw in pageTopWords:
        #pageVec = get_vectors(ptw["words"])
        #pageVecMean = pageVec.mean(axis = 0)
        pageVec_weighted = get_weighted_vectors(ptw["words"],ptw["scores"])
        weight = sum(score for score in ptw["scores"])
        pageVecMean = np.divide(np.sum(pageVec_weighted,axis = 0),np.asarray(weight))
        docVector = {"pageId": ptw["pageId"], "pageTitle": ptw["pageTitle"], "words": ptw["words"], "vector": pageVecMean.tolist()}
        vecs.write(json.dumps(docVector))
        vecs.write("\n")
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    traceback.print_exc()
finally:
    pass