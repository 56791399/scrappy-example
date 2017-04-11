
import scrapy
import requests
import json
from scrapy.selector import Selector

class NewsSpider2(scrapy.Spider):
    name = "news2"

    def start_requests(self):
        urls = [
            'https://www.theguardian.com/international'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        dataArray = response.xpath("//div[@class='fc-item__container']").extract()
        toPrint = ""
        for body in dataArray:
            try:
                newsImg = Selector(text=body).xpath("//picture//source/@srcset").extract() # Link to new
                newsImg0 = "noImage"
                if len(newsImg) > 0:
                    newsImg0 = str(newsImg[0])

                newsSummary = Selector(text=body).xpath("//div[@class='fc-item__standfirst']/text()").extract() # Link to new
                newsSummary0 = "noSummary"
                if len(newsSummary) > 0:
                    newsSummary0 = str(newsSummary[0])

                newsTitle = Selector(text=body).xpath("//span[@class='js-headline-text']/text()").extract() # Link to new
                newsTitle0 = "noTitle"
                if len(newsTitle) > 0:
                    newsTitle0 = str(newsTitle[0])

                headers = {'Content-type': 'application/json'}
                if len(newsTitle) > 0 and (len(newsSummary) > 0 or len(newsContainLi) > 0):
                    newsSummary0 = str(newsSummary[0].replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "'").replace(u"\xed", "'").encode('utf8'))
                    data = {"title": newsTitle0, "body": newsSummary0, "likes": '2', "imgUrl": newsImg0}

                data_json = json.dumps(data)
                toPrint = data_json

                url = "http://localhost:9000/v1/news"
                responsePost = requests.post(url, data=data_json, headers=headers)
            except Exception as e:
                print("Exception in the scrapping")
            else:
                pass
            finally:
                pass
        self.log('Spider 2 run')