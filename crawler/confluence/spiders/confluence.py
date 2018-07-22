import scrapy
import json

from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from confluence.items import ConfluenceItem
from confluence.credentials import username, password

# download_delay setting
class ConfluenceSpider(Spider):
    name = 'confluence'
    allowed_domains = []

    start_urls = [
        'https://confluence/dologin.action'
    ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'os_username': username, 'os_password': password},
            callback=self.after_login
        )

        ## Bobby : 90972601
        ## Dan : 133204509
        ## NYC office: 94754511s
        ## MCI : 131895457
        ## MCG Archive: 131895487
        ## DMT: 50168843
		## Key Terms : 135451964
    def after_login(self, response):
        return Request(url="https://confluence/rest/api/content/135451964/child/page", callback=self.parse_page)

    def parse_page(self, response):
        jsonData = json.loads(response.body_as_unicode())
        for result in jsonData["results"]:
            childPageId = result["id"]
            # TODO - add error parsing option
            yield Request(url="https://confluence/rest/api/content/" + str(childPageId) +
                          "?expand=space,body.view,container,metadata.labels,ancestors", callback = self.parse_content)
            yield Request(url="https://confluence/rest/api/content/" + str(childPageId) +
                            "/child/page", callback=self.parse_page)

    def parse_content(self, response):
        jsonPage = json.loads(response.body_as_unicode())
        pageId = jsonPage["id"]
        pageTitle = jsonPage["title"]
        content = jsonPage["body"]["view"]["value"]
        labels = jsonPage["metadata"]["labels"]["results"]
        ancestors = jsonPage["ancestors"]
        ancestorList = []
        for ancestor in ancestors:
            ancestorList.append({"id":ancestor["id"], "title":ancestor["title"]})

        item = ConfluenceItem()
        item['pageId'] = pageId
        item['pageTitle'] = pageTitle
        item['content'] = content
        item['labels'] = labels
        item['ancestors'] = ancestorList

        print('Parsed page ' + pageTitle)
        return item