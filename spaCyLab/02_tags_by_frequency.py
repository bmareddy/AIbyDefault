import json
from bs4 import BeautifulSoup as bs
import spacy
from collections import Counter

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

#Function that takes in a JSON object that has below key-value pair structure
#{"pageId": "12345", "pageTitle":"This is page title", "content":"<p>This is html markup</p>"}
def posWords(objJSON):
    soup = bs(objJSON["content"],"html.parser")
    t = soup.getText() #-- get all text from the html page; mushes text from multiple html tags together; for ex: h1 and p (ObjectiveThe)
    doc = nlp(t)
    words = [cleanString(token.string) for token in doc if not isNoisy(token,pos_exclusions=["ADP","CCONJ","PUNCT","SPACE"])]    
    return words

# JSON export of the confluence space
space = "Key-Terms"
wd = "C:\\Users\\bmareddy\\Documents\\PyLab\\data"
inFile = "{}\\{}.json".format(wd,space)
outFile = "{}\\{}_tags.json".format(wd,space)

#Load and parse JSON object of each confluence page
#For each page that has content, compute 3 most common words
outList = []
with open(inFile,'r') as confSpaceData:
    for pagejson in confSpaceData:
    # for x in range(15):
    #     pagejson = next(confSpaceData)
        if pagejson.startswith("{") and pagejson.endswith("\n"):
            if pagejson[len(pagejson)-2] == ",":
                pagejson = pagejson[:-2]
            parsedpagejson = json.loads(pagejson)
            if parsedpagejson["content"] != "":
                words = posWords(parsedpagejson)
                if words:
                    tags = []
                    tag_list = Counter(words).most_common(3)
                    for t in tag_list:
                        tags.append(t[0])
                    outList.append([("pageId", parsedpagejson["pageId"]),("pageTitle", parsedpagejson["pageTitle"]),("tags", tags)])
confSpaceData.close()

#Write the tag list to a file
with open(outFile,"w") as confSpaceTags:
    json.dump(outList, confSpaceTags)
confSpaceTags.close()
