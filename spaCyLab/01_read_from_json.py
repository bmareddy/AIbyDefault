import json
# from html.parser import HTMLParser
from bs4 import BeautifulSoup as bs
import spacy

# JSON export of the confluence space
wd = "C:\\Users\\bmareddy\\Documents\\PyLab"
dataFile = wd+"\\MCG-Archive.json"

nlp = spacy.load("en_core_web_sm")

# class MyHTMLParser(HTMLParser):
#     def handle_data(self, data):
#         print("Encountered some data  :", data)

#htmlparser = MyHTMLParser()

# Load and parse JSON object of each confluence page
allPages = {"pageId":[],"pageTitle":[],"text":[]}
with open(dataFile,'r') as confSpaceData:
#    for pagejson in confSpaceData:
    for x in range(10):
        pagejson = next(confSpaceData)
        if pagejson.startswith("{") and pagejson.endswith("\n"):
            if pagejson[len(pagejson)-2] == ",":
                pagejson = pagejson[:-2]
            parsedpagejson = json.loads(pagejson)
            if parsedpagejson["content"] != "":
                #print(parsedpagejson["pageId"],parsedpagejson["pageTitle"])
                soup = bs(parsedpagejson["content"],"html.parser")
                t = soup.getText() #-- get all text from the html page
                thisPage = {'pageId': parsedpagejson["pageId"], 'pageTitle': parsedpagejson["pageTitle"], 'text': t}
                for key in allPages.keys():
                    allPages[key].append(thisPage[key])
                # doc = nlp(t)
                # for token in doc:
                #     if token.is_alpha and not token.is_stop:
                #         print (token.text)
            #else:
                #print("<No content on this page>. Skipping...")
confSpaceData.close()
print (allPages.items())