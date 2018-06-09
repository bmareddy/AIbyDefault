import json
from bs4 import BeautifulSoup as bs
import spacy

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
    words = [cleanString(token.lemma_) for token in doc if not isNoisy(token,pos_exclusions=["ADP","CCONJ","PUNCT","SPACE"])]  
    return words

# JSON export of the confluence space
wd = "C:\\Users\\bmareddy\\Documents\\PyLab"
inFile = wd+"\\MCG-Archive.json"
outFile = wd+"\\MCG-Archive_tags.json"
wordsFile = wd+"\\MCG-Archive_allWords_lemma.json"

#Load and parse JSON object of each confluence page
#Clean and prepare a dictoinay of all pages
allPages = {"pageId":[],"pageTitle":[],"words":[]}
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
                thisPage = {"pageId": parsedpagejson["pageId"],"pageTitle": parsedpagejson["pageTitle"], "words": w}
                for key in allPages.keys():
                    allPages[key].append(thisPage[key])
confSpaceData.close()

# Write the words list to a file for use by tf-idf
with open(wordsFile,"w") as confSpacePageWords:
    json.dump(allPages, confSpacePageWords)
confSpacePageWords.close()