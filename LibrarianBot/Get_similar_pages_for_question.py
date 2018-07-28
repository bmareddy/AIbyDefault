import json
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from Utilities import isNoisy
import Constants

# static variables
true = True
false = False

def get_vectors(sent):
    tokens = nlp(sent)
    pageVec = np.array([])
    for token in tokens:
        if not isNoisy(token):
            wordVec = token.vector
            wordVec = wordVec.reshape(1, 300)
            if pageVec.size == 0:
                pageVec = wordVec
            else:
                pageVec = np.concatenate([pageVec, wordVec], axis=0)
    pageVecMean = pageVec.mean(axis = 0)
    return pageVecMean


def similar_pages(vsm, source_vec):
    source_vec = source_vec.reshape(1,300)
    compare_vec = [np.asarray(vsm[i]["vector"]) for i in range(len(vsm))]
    sim_page_positions = [(i,cosine_similarity(source_vec,compare_vec[i].reshape(1, 300))) for i in range(len(vsm))]
    sim_page_positions = [(x[0], float(x[1].reshape(1,))) for x in sim_page_positions]
    sim_page_positions.sort(key=lambda x: x[1], reverse = True)
    sim_pages = [(vsm[x[0]]["pageTitle"], x[1], vsm[x[0]]["pageId"]) for x in sim_page_positions[:10]]
    return sim_pages


# JSON export of the page, its words and vector
wd = Constants.WORKING_DIRECTORY
# space = "mci_"
nlp = spacy.load("en_vectors_web_lg")

def get_similar_pages_for_sentence(space, version, sentence):
    try:
        inFileVecs = "{}\\{}tags_vectors{}.json".format(Constants.WORKING_DIRECTORY, space, version)
        pageVectors = [json.loads(pv) for pv in open(inFileVecs,"r").read().splitlines()]
        print ("Finding similar pages for:" + sentence)
        
        sent_vec = get_vectors(sentence)
        sp = similar_pages(pageVectors, sent_vec)
        output = '\n'.join("{} ({}) - https://confluence/pages/viewpage.action?pageId={}".format(page[0], round(page[1],3), page[2]) for page in sp)
        # print(output)
        return output
    except Exception as e:
        print (e)
    finally:
        pass

# get_similar_pages_for_sentence("I am trying")