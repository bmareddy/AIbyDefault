import math
import json

#static variables
true = True
false = False

#tf-idf functions
#Concept from: https://stevenloria.com/tf-idf/
def tf(word, thisPageWords):
    return thisPageWords.count(word) / len(thisPageWords)

def n_containing(word, allPagesWords):
    return sum(1 for pageWords in allPagesWords if word in pageWords)

def idf(word, allPagesWords):
    return math.log(len(allPagesWords) / (1 + n_containing(word, allPagesWords)))

def tfidf(word, thisPageWords, allPagesWords):
    return tf(word, thisPageWords) * idf(word, allPagesWords)

# JSON export of the lemmatized words per each page
space = "DMT"
wd = "C:\\Users\\bmareddy\\Documents\\PyLab\\data"
inFile = "{}\\{}_allWords_lemma.json".format(wd,space)
outFile = "{}\\{}_tags_tfidf.json".format(wd,space)

tags = open(outFile,"w",newline="\n")
try:
    allPages = open(inFile,"r").read()
    allPages = json.loads(allPages)
    for i in range(len(allPages["pageId"])):
        scores = {word: tfidf(word, allPages["words"][i], allPages["words"]) for word in allPages["words"][i]}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=true)
        topwords = [word for word, score in sorted_words[:10]]
        topscores = [round(score,5) for word, score in sorted_words[:10]]
        if topwords:
            json.dump({"pageId": allPages["pageId"][i], "pageTitle": allPages["pageTitle"][i], "words": topwords, "scores": topscores},tags)
            tags.write("\n")
            #print ({"pageId": allPages["pageId"][i], "words": topwords, "scores": topscores})
except Exception as e:
    print (e)
finally:
    tags.close()