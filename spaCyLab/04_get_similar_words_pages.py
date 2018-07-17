import json
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random as rand

def similar_pages(vsm,page_position,n = 5):
    source_vec = np.asarray(vsm[page_position]["vector"])
    source_vec = source_vec.reshape(1,300)
    compare_vec = [np.asarray(vsm[i]["vector"]) for i in range(len(vsm))]
    sim_page_positions = [(i,cosine_similarity(source_vec,compare_vec[i].reshape(1,300))) for i in range(len(vsm)) if i != page_position]
    sim_page_positions = [(x[0],float(x[1].reshape(1,))) for x in sim_page_positions]
    sim_page_positions.sort(key=lambda x: x[1], reverse = True)
    sim_pages = [(vsm[x[0]]["pageTitle"],x[1]) for x in sim_page_positions[:n]]
    return sim_pages

def similar_words_from_vocab(source_vec,n = 5):
    nlp = spacy.load("en_core_web_lg")
    word_similarity = [(word.text.lower(), np.asscalar(cosine_similarity(source_vec.reshape(1,300),word.vector.reshape(1,300)))) for word in nlp.vocab if word.prob >= -15]
    sorted_word_similarity = sorted(list(set(word_similarity)), key = lambda x: x[1], reverse = True)
    return sorted_word_similarity[:n]

# JSON export of the page, its words and vector
space = "DMT"
wd = "C:\\Users\\bmareddy\\Documents\\PyLab\\data"
inFileVecs = "{}\\{}_tags_vectors.json".format(wd,space)
#outFile = wd+"\\MCG-Archive_tags_vectors.json"

try:
    pageVectors = [json.loads(pv) for pv in open(inFileVecs,"r").read().splitlines()]
    page_pos = rand.randint(0,len(pageVectors))
    source_vec = np.asarray(pageVectors[page_pos]["vector"])
    print ("Finding similar pages for: {}".format(pageVectors[page_pos]["pageTitle"]))
    sp = similar_pages(pageVectors,page_pos)
    for page in sp:
        print ("\t {} ({})".format(page[0],page[1]))
    print ("Finding words representing the page: {}".format(pageVectors[page_pos]["pageTitle"]))
    sw = similar_words_from_vocab(source_vec)
    print (",".join([str(w[0]) for w in sw]))
except Exception as e:
    print (e)
finally:
    pass

    