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

# JSON export of the confluence space
wd = "C:\\Users\\bmareddy\\Documents\\PyLab"
inFile = wd+"\\MCG-Archive_allWords_lemma.json"
outFile = wd+"\\MCG-Archive_tags_tfidf.json"

tags = open(outFile,"w",newline="\n")
try:
    allPages = open(inFile,"r").read()
    allPages = json.loads(allPages)
    for i in range(15): #len(allPages["text"]):
        scores = {word: tfidf(word, allPages["words"][i], allPages["words"]) for word in allPages["words"][i]}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=true)
        topWords = []
        for word, score in sorted_words[:10]:
            topWords = topWords + [(word, round(score,5))]
        json.dump({allPages["pageId"][i]: topWords},tags)
except Exception as e:
    print (e)
finally:
    tags.close()
    print ("End of all things!")