import json
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import Constants
import random as rand


def similar_pages(vsm, page_position, n=5):
    source_vec = np.asarray(vsm[page_position]["vector"])
    source_vec = source_vec.reshape(1, 300)
    compare_vec = [np.asarray(vsm[i]["vector"]) for i in range(len(vsm))]
    sim_page_positions = [(i, cosine_similarity(source_vec,compare_vec[i].reshape(1,300))) for i in range(len(vsm)) if i != page_position]
    sim_page_positions = [(x[0], float(x[1].reshape(1, ))) for x in sim_page_positions]
    sim_page_positions.sort(key=lambda x: x[1], reverse=True)
    sim_pages = [(vsm[x[0]]["pageTitle"], x[1], vsm[x[0]]["pageId"]) for x in sim_page_positions[:n]]
    return sim_pages


def similar_words_from_vocab(source_vec, n=5):
    nlp = spacy.load("en_core_web_lg")
    word_similarity = [(word.text.lower(), np.asscalar(cosine_similarity(source_vec.reshape(1,300),word.vector.reshape(1, 300)))) for word in nlp.vocab if word.prob >= -15 and not word.is_stop]
    sorted_word_similarity = sorted(list(set(word_similarity)), key=lambda x: x[1], reverse=True)
    return sorted_word_similarity[:n]


# JSON export of the page, its words and vector
wd = Constants.WORKING_DIRECTORY
# space = "mci_"
nlp = spacy.load("en_vectors_web_lg")


def get_similar_pages(space, version, pageId):
    try:
        inFileVecs = "{}\\{}tags_vectors{}.json".format(Constants.WORKING_DIRECTORY, space, version)
        pageVectors = [json.loads(pv) for pv in open(inFileVecs, "r").read().splitlines()]

        page_pos = next((idx for idx, item in enumerate(pageVectors) if item["pageId"] == pageId), None)
        if page_pos is None:
            return "PageId {} was not found in our data".format(pageId)

        print ("Finding similar pages for: {}".format(pageVectors[page_pos]["pageTitle"]))

        sp = similar_pages(pageVectors, page_pos)
        output = '\n'.join("{} ({})".format(page[0], round(page[1], 3)) for page in sp)
        for page in sp:
            print ("\t {} ({})".format(page[0], page[1]))

        return output
    except Exception as e:
        print (e)
    finally:
        pass


def get_tags_for_page(space, version, pageId):
    try:
        inFileVecs = "{}\\{}tags_vectors{}.json".format(Constants.WORKING_DIRECTORY, space, version)
        pageVectors = [json.loads(pv) for pv in open(inFileVecs, "r").read().splitlines()]

        page_pos = next((idx for idx, item in enumerate(pageVectors) if item["pageId"] == pageId), None)
        if page_pos is None:
            return "PageId {} was not found in our data".format(pageId)

        source_vec = np.asarray(pageVectors[page_pos]["vector"])

        print ("Finding words representing the page: {}".format(pageVectors[page_pos]["pageTitle"]))

        sw = similar_words_from_vocab(source_vec)
        output = ", ".join([str(w[0]) for w in sw])
        return output
    except Exception as e:
        print (e)
    finally:
        pass

    