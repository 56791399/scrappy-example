
import scrapy
import requests
import json
from scrapy.selector import Selector

class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        urls = [
            'https://www.nytimes.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        dataArray = response.xpath("//div[@class='ab-column column']//div[@class='collection']//article").extract()
        for body in dataArray:
            newsLink = Selector(text=body).xpath("//h2[@class='story-heading']//a/@href").extract() # Link to new
            newsTitle = Selector(text=body).xpath("//h2[@class='story-heading']//a/text()").extract() # Title of news
            newsSummary = Selector(text=body).xpath("//p[@class='summary']/text()").extract() # contain of news
            newsContainLi = Selector(text=body).xpath("//li/text()").extract()
            newsTitle0 = str(newsTitle[0].replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "'").replace(u"\xed", "'").encode('utf8'))

            headers = {'Content-type': 'application/json'}
            if len(newsSummary) > 0:
                newsSummary0 = str(newsSummary[0].replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "'").replace(u"\xed", "'").encode('utf8'))
                data = {"title": newsTitle0, "body": newsSummary0, "likes": '2'}
            elif len(newsContainLi) > 0:
                newsContainLi0 = str(newsContainLi[0].replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "'").replace(u"\xed", "'").encode('utf8'))
                data = {"title": newsTitle0, "body": newsContainLi0, "likes": '2'}
            else:
                data = {"title": newsTitle0, "body": "Body Empty", "likes": '2'}
            
            data_json = json.dumps(data)
            url = "http://localhost:9000/v1/news"
            response = requests.post(url, data=data_json, headers=headers)
            print("This is the response \n")
            print(response.text)

        filename = 'news-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(str(dataArray))
        self.log('Saved file %s' % filename)