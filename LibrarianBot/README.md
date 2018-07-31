# AIbyDefault
Code for the AIbyDefault program
Authors: Daniel Kang, Bobby Mareddy
Date: July 31st, 2018

## Description

This directory implements the slack application that utilizes nlp library to perform tagging and provide documents that are similar to given input pages.


## Setup
1. Use crawler to download a specific space from confluence page. Make sure you change Constants.Working_Directory accordingly to point to the part you have the data.
2. Use files in spacy subdirectory to parse the json data files and get tf-idf scores as well as document vectors.
3. One should have appropriate slack token defined in Constants.py. Once identified, try `python SlackApiTest.py` and verify it returns successful response.
4. Invoke `python LibrarianBot.py`. Wait until the terminal prints "Librarian connected and running!"
5. Now you are ready to test the methods. 

## Slack API
Currently, the interaction is very limited. You should directly talk to the LibrarianBot app, and tag the app as well. Hence, enter the following: 
```@Librarian {command} {input}```

1. command = `switch to`, input = name of the space we want to use. Note that this should match the prefix of the file names.
2. command = `use`, input = "weighted" or "normal". If `weighted`, we use the version of document vector that was computed by taking weighted average of word vectors, where the weights are tf-idf scores. Otherwise, we just use regular document vectors which are simple averages of word vectors. Note that this should match the suffix of the filenames.
3. command = `tag`, input = page id. Provides the vocabulary that could be used as tags for this page. It provides two lists: first is the list of words that appear in the page and have the highest tf-idf scores. Secondly, it also provides a list of vocab that are in our whole corpus and are closest to the document vector of the provided input.
4. command = `similar`, input = page id. Provides the list of pages in the space that are closest to the given page. The similarity is determined by taking cosine distance betweent the vectors.
5. command = `answer`, input = any sentence. Provides the list of pages in the space that are closest to the given sentence. The sentence is tokenized and lemmatized, and its highest tf-idf scored words are averaged to create one vector, which is then compared with other vectors of the space using cosine similarity.

## Notes
JSON data files are not included in this repo due to privacy issues as well as size constraints.