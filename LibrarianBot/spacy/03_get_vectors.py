import json
import spacy
import numpy as np

nlp = spacy.load("en_vectors_web_lg")


def get_vectors(wordlist):
    tokens = nlp(" ".join(str(s) for s in wordlist))
    pageVec = np.array([])
    for token in tokens:
        wordVec = token.vector
        wordVec = wordVec.reshape(1, 300)
        if pageVec.size == 0:
            pageVec = wordVec
        else:
            pageVec = np.concatenate([pageVec, wordVec], axis=0)
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


def main():
    # JSON export of the tfidf words & scores per each page
    wd = "C:\\Users\\dkang\\Documents\\Python Scripts\\aibydefault\\AiByDefault\\LibrarianBot\\Crawler\\data"
    inFile = "{}\\tags_tfidf.json".format(wd)
    outFile = "{}\\tags_vectors_weighted.json".format(wd)

    vecs = open(outFile, "w", newline="\n")
    try:
        pageTopWords = open(inFile, "r").read().splitlines()
        pageTopWords = [json.loads(ptw) for ptw in pageTopWords]
        docVector = {}

        # Load English language LARGE model; there is also another model explicitly for vectors
        for ptw in pageTopWords:
            # pageVec = get_vectors(ptw["words"])
            # pageVecMean = pageVec.mean(axis=0)
            pageVec_weighted = get_weighted_vectors(ptw["words"], ptw["scores"])
            weight = sum(score for score in ptw["scores"])
            pageVecMean = np.divide(np.sum(pageVec_weighted,axis = 0), np.asarray(weight))
            docVector = {"pageId": ptw["pageId"], "pageTitle": ptw["pageTitle"], "words": ptw["words"],
                         "vector": pageVecMean.tolist(), "ancestorId": ptw["ancestorId"]}
            vecs.write(json.dumps(docVector))
            vecs.write("\n")
    except Exception as e:
        print(e)
    finally:
        pass


if __name__ == "__main__":
    main()
