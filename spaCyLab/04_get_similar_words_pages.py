import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random as rand

def similar_pages(vsm,page_position):
    source_vec = np.asarray(vsm[page_position]["vector"])
    source_vec = source_vec.reshape(1,300)
    compare_vec = [np.asarray(vsm[i]["vector"]) for i in range(len(vsm))]
    sim_page_positions = [(i,cosine_similarity(source_vec,compare_vec[i].reshape(1,300))) for i in range(len(vsm)) if i != page_position]
    sim_page_positions = [(x[0],float(x[1].reshape(1,))) for x in sim_page_positions]
    sim_page_positions.sort(key=lambda x: x[1], reverse = True)
    sim_pages = [(vsm[x[0]]["pageTitle"],x[1]) for x in sim_page_positions[:5]]
    return sim_pages

# JSON export of the page, its words and vector
wd = "C:\\Users\\bmareddy\\Documents\\PyLab"
inFileVecs = wd+"\\MCG-Archive_tags_vectors.json"
#outFile = wd+"\\MCG-Archive_tags_vectors.json"

try:
    pageVectors = [json.loads(pv) for pv in open(inFileVecs,"r").read().splitlines()]
    page_pos = rand.randint(0,len(pageVectors))
    print ("Finding similar pages for: {}".format(pageVectors[page_pos]["pageTitle"]))
    sp = similar_pages(pageVectors,page_pos)
    for page in sp:
        print ("\t {} ({})".format(page[0],page[1]))
except Exception as e:
    print (e)
finally:
    pass

    