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



#utility functions
def cleanString(s, lower = True, trim = True):
    if lower:
        s = s.lower()
    if trim:
        s = s.strip()
    return s


#Function to determine is a given token is "noisy"
#Concept from: https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/
def isNoisy(token, pos_exclusions = [], min_char_length = 3, force_include = ["aid","mcg","bi","pi","mi"]):
    exclude = False
    #default exclusion
    if token.is_stop:
        exclude = True
    if token.pos_ in pos_exclusions:
        exclude = True
    if len(token.string) <= min_char_length:
        exclude = True
    if token.string in force_include:
        exclude = True
    return exclude


#Function that takes in text and returns a list of words
def posWords(t):
    doc = nlp(t)
    words = [cleanString(token.lemma_) for token in doc if not isNoisy(token,pos_exclusions=["ADP","CCONJ","PUNCT","SPACE"])]  
    return words

def get_vocab_without_shared_stems(candidates, words_as_sentence, n=5):
    tokens = posWords(words_as_sentence)

    results = []
    lemmas = []
    for i in range(len(tokens)):
        if tokens[i] not in lemmas:
            results.append(candidates[i])
            lemmas.append(tokens[i])
        if(len(results) == n):
            break

    return results


def similar_words_from_vocab(source_vec, n=5):
    nlp = spacy.load("en_core_web_lg")
    word_similarity = [(word.text.lower(), np.asscalar(cosine_similarity(source_vec.reshape(1,300),word.vector.reshape(1, 300)))) for word in nlp.vocab if word.prob >= -15 and not word.is_stop]
    sorted_word_similarity = sorted(list(set(word_similarity)), key=lambda x: x[1], reverse=True)

    candidates = sorted_word_similarity[:50]
    words_as_sentence = ' '.join("{}".format(candidate[0]) for candidate in candidates)
    result = get_vocab_without_shared_stems(candidates, words_as_sentence, n)

    return result


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
        output = '\n'.join("{} ({}) - https://confluence/pages/viewpage.action?pageId={}".format(page[0], round(page[1], 3), page[2]) for page in sp)
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

        print ("Finding words representing the page: {}".format(pageVectors[page_pos]["pageTitle"]))

        # get high tf-idf scored vocabs
        words = pageVectors[page_pos]["words"]
        words_as_sentence = ' '.join("{}".format(word) for word in words)
        output1_words = get_vocab_without_shared_stems(words, words_as_sentence)

        output0 = "Finding words representing the page: {}".format(pageVectors[page_pos]["pageTitle"])
        output1 = "Words with high tf-idf scores: " + ", ".join([word for word in output1_words])

        # get similar vectors for the document vector
        source_vec = np.asarray(pageVectors[page_pos]["vector"])
        sw = similar_words_from_vocab(source_vec)

        output2 = "Words similar to document vector: " + ", ".join([str(w[0]) for w in sw])

        output = output0 + "\n" + output1 + "\n" + output2
        return output
    except Exception as e:
        print (e)
    finally:
        pass

    