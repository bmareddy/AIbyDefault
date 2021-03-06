import json
from bs4 import BeautifulSoup as bs
import spacy

# static variables
true = True
false = False


# utility functions
def cleanString(s, lower=true, trim=true):
    if lower:
        s = s.lower()
    if trim:
        s = s.strip()
    return s


# Function to determine is a given token is "noisy"
# Concept from: https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/
def isNoisy(token, pos_exclusions=[], min_char_length=3, force_include=["aid", "mcg", "bi", "pi", "mi"]):
    exclude = false
    # default exclusion
    if token.is_stop:
        exclude = true
    if token.pos_ in pos_exclusions:
        exclude = true
    if len(token.string) <= min_char_length:
        exclude = true
    if token.string in force_include:
        exclude = false
    return exclude


# Function that takes in text and returns a list of words
def posWords(t):
    doc = nlp(t)
    words = [cleanString(token.lemma_) for token in doc if not isNoisy(token, pos_exclusions=["ADP", "CCONJ", "PUNCT", "SPACE"])] 
    return words


def getAncestorPageId(pages):
    if(len(pages) > 1):
        return pages[1]['id']
    return None


def parsePage(pagejson):
    if pagejson.startswith("{") and pagejson.endswith("\n"):
        if pagejson[len(pagejson) - 2] == ",":
            pagejson = pagejson[:-2]
        parsedpagejson = json.loads(pagejson)
        if parsedpagejson["content"] != "":
            soup = bs(parsedpagejson["content"], "html.parser")
            # get all text from the html page; mushes text from multiple html tags together;
            # for ex: h1 and p (ObjectiveThe)
            t = soup.getText(separator=" ")
            w = posWords(t)
            ancestorId = getAncestorPageId(parsedpagejson["ancestors"]) or parsedpagejson["pageId"]
            thisPage = {"pageId": parsedpagejson["pageId"], "pageTitle": parsedpagejson["pageTitle"],
                        "words": w, "ancestorId": ancestorId, "space": parsedpagejson["space"]}
            return thisPage
    return None


# Load English language model
nlp = spacy.load("en_core_web_lg")


def main():
    # JSON export of the confluence space
    spaces = ["KeyTerms", "MCI", "DMT"]
    # spaces = ["sample"]
    wd = "C:\\Users\\dkang\\Documents\\Python Scripts\\aibydefault\\AiByDefault\\LibrarianBot\\Crawler\\data"

    # Load and parse JSON object of each confluence page
    # Clean and prepare a dictoinay of all pages

    allPages = {"pageId": [], "pageTitle": [], "words": [], "ancestorId": [], "space": []}

    # Read all data
    for space in spaces:
        print("Reading " + space)
        try:
            inFile = "{}\\{}.json".format(wd, space)
            with open(inFile, 'r') as confSpaceData:
                for pagejson in confSpaceData:
                    thisPage = parsePage(pagejson)
                    if thisPage is not None:
                        for key in allPages.keys():
                            allPages[key].append(thisPage[key])
            confSpaceData.close()
        except Exception as e:
            print (e)
        finally:
            if not confSpaceData.closed:
                confSpaceData.close()

    # write results to a json file
    try:
        # Write the words list to a file for use by tf-idf
        output = "{}\\allWords_lemma.json".format(wd)
        with open(output, "w") as confSpacePageWords:
            json.dump(allPages, confSpacePageWords)
        confSpacePageWords.close()
    except Exception as e:
        print (e)
    finally:
        if not confSpacePageWords.closed:
                confSpacePageWords.close()


if __name__ == "__main__":
    main()
