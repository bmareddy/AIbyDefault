import json
from bs4 import BeautifulSoup as bs
import spacy
import math

#Load English language model
nlp = spacy.load("en_core_web_sm")

#static variables
true = True
false = False

#utility functions
def cleanString(s, lower = true, trim = true):
    if lower:
        s = s.lower()
    if trim:
        s = s.strip()
    return s

#Function to determine is a given token is "noisy"
#Concept from: https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/
def isNoisy(token, pos_exclusions = [], min_char_length = 3, force_include = ["aid","mcg","bi","pi","mi"]):
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

#Function that takes in text and returns a list of words
def posWords(t):
    doc = nlp(t)
    words = [cleanString(token.string) for token in doc if not isNoisy(token,pos_exclusions=["ADP","CCONJ","PUNCT","SPACE"])]    
    return words

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
inFile = wd+"\\MCG-Archive.json"
outFile = wd+"\\MCG-Archive_tags.json"

#Load and parse JSON object of each confluence page
#Clean and prepare a dictoinay of all pages
allPages = {"pageId":[],"pageTitle":[],"text":[],"words":[]}
with open(inFile,'r') as confSpaceData:
    for pagejson in confSpaceData:
        if pagejson.startswith("{") and pagejson.endswith("\n"):
            if pagejson[len(pagejson)-2] == ",":
                pagejson = pagejson[:-2]
            parsedpagejson = json.loads(pagejson)
            if parsedpagejson["content"] != "":
                soup = bs(parsedpagejson["content"],"html.parser")
                t = soup.getText(separator=" ") #-- get all text from the html page; mushes text from multiple html tags together; for ex: h1 and p (ObjectiveThe)
                w = posWords(t)
                thisPage = {"pageId": parsedpagejson["pageId"],"pageTitle": parsedpagejson["pageTitle"],"text": t, "words": w}
                for key in allPages.keys():
                    allPages[key].append(thisPage[key])
confSpaceData.close()

for i in range(15): #len(allPages["text"]):
    print ("Top words in page: {}".format(allPages["pageTitle"][i]))
    scores = {word: tfidf(word, allPages["words"][i], allPages["words"]) for word in allPages["words"][i]}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=true)
    for word, score in sorted_words[:3]:
        print ("\tWord: {}, TF-IDF: {}".format(word, round(score,5)))

#Write the tag list to a file
# with open(outFile,"w") as confSpaceTags:
#     json.dump(allPages, confSpaceTags)
# confSpaceTags.close()
