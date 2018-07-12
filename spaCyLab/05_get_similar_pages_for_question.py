import json
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

#static variables
true = True
false = False

def isNoisy(token, pos_exclusions = [], min_char_length = 3, force_include = []):
    exclude = false
    #default exclusion
    if token.is_stop:
        exclude = true
    if token.pos_ in pos_exclusions:
        exclude = true
    if len(token.string) <= min_char_length:
        exclude = true
    if token.string in force_include:
        exclude = false
    return exclude

def get_vectors(sent):
    tokens = nlp(sent)
    pageVec = np.array([])
    for token in tokens:
        if not isNoisy(token):
            wordVec = token.vector
            wordVec = wordVec.reshape(1,300)
            if pageVec.size == 0:
                pageVec = wordVec
            else:
                pageVec = np.concatenate([pageVec,wordVec],axis = 0)
            #print ("Current word: {0}, vector shape: {1}, word shape: {2}".format(token,pageVec.shape,wordVec.shape))
    pageVecMean = pageVec.mean(axis = 0)
    #print ("Sentence shape: {0}".format(pageVecMean.shape))
    return pageVecMean

def similar_pages(vsm,source_vec):
    source_vec = source_vec.reshape(1,300)
    compare_vec = [np.asarray(vsm[i]["vector"]) for i in range(len(vsm))]
    sim_page_positions = [(i,cosine_similarity(source_vec,compare_vec[i].reshape(1,300))) for i in range(len(vsm))]
    sim_page_positions = [(x[0],float(x[1].reshape(1,))) for x in sim_page_positions]
    sim_page_positions.sort(key=lambda x: x[1], reverse = True)
    sim_pages = [(vsm[x[0]]["pageTitle"],x[1]) for x in sim_page_positions[:10]]
    return sim_pages

# JSON export of the page, its words and vector
space = "DMT"
wd = "C:\\Users\\bmareddy\\Documents\\PyLab\\data"
inFileVecs = "{}\\{}_tags_vectors.json".format(wd,space)
#outFile = wd+"\\MCG-Archive_tags_vectors.json"

try:
    pageVectors = [json.loads(pv) for pv in open(inFileVecs,"r").read().splitlines()]
    sentence = "if i set up an auto roll up from one entity to another (say from CBG to ZIP) and there are two source tables with the CBG entity (one preaggregated at the CBG entity and the other at a TLOG level with all entities including CBG), which source table will the auto-roll up consider given that the metric IDs are the same for both ?"
    print ("Finding similar pages for:")
    nlp = spacy.load("en_vectors_web_lg")
    sent_vec = get_vectors(sentence)
    sp = similar_pages(pageVectors,sent_vec)
    for page in sp:
        print ("\t {} ({})".format(page[0],page[1]))
except Exception as e:
    print (e)
finally:
    pass

    