# AIbyDefault
Code for the AIbyDefault program
Authors: Daniel Kang, Bobby Mareddy
Date: July 31st, 2018

## Description

This project attempts to provide an application to tag, search, classify and summarize documentation.

This code utilizes the following platforms/libraries:
1. [Scrapy](https://scrapy.org/)
2. [Spacy](https://spacy.io/)
3. [Confluence REST API](https://developer.atlassian.com/server/confluence/confluence-server-rest-api/)
4. [Slack App API](https://api.slack.com/)

The overall steps are as follows:


## Project Structure

This project includes several different folders. The main folder is *LibrarianBot*.
### LibrarianBot
This directory is the implementation of the Slack Application that utilizes nlp to tag and search similar pages for confluence pages. 

### Crawler
This directory utilizes Scrapy to crawl given spaces in confluence and download the child pages.

### Classifiers
This directory looks at ways to utilize our identified document vectors and perform classification

### spaCyLab
This directory performs NLP operations on crawled data. Note that most of the implementations here are also included in LibrarianBot directory.

## Notes
License: MIT



