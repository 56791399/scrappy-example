
import scrapy
import requests
import json
from scrapy.selector import Selector

class NewsSpider4(scrapy.Spider):
    name = "news4"

    def start_requests(self):
        urls = [
            'http://www.marca.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        dataArray = response.xpath("//li[@class='content-item ']").extract()
        toPrint = ""
        for body in dataArray:
            print("this will scrap (" + str(len(dataArray)) + ") Items")
            try:
                newsImg = Selector(text=body).xpath("//img/@src").extract() # Link to new
                newsImg0 = "noImage"
                if len(newsImg) > 0:
                    newsImg0 = str(newsImg[0].replace(u"\u2018", "").replace(u"\u2019", "").replace(u"\u201c", "E").replace(u"\xed", "i").replace(u"\xf3", "o").replace(u"\xf1", "n").replace(u"\xe1", "a").encode('utf8'))

                newsSummary = Selector(text=body).xpath("//h3[@class='mod-title']//a/text()").extract() # Link to new
                newsSummary0 = "noSummary"
                if len(newsSummary) > 0:
                    newsSummary0 = str(newsSummary[0].replace(u"\u2018", "").replace(u"\u2019", "").replace(u"\u201c", "E").replace(u"\xed", "i").replace(u"\xf3", "o").replace(u"\xf1", "n").replace(u"\xe1", "a").encode('utf8'))

                newsTitle = Selector(text=body).xpath("//h3[@class='mod-title']//a/text()").extract() # Link to new
                newsTitle0 = "noTitle"
                if len(newsTitle) > 0:
                    newsTitle0 = str(newsTitle[0].replace(u"\u2018", "").replace(u"\u2019", "").replace(u"\u201c", "E").replace(u"\xed", "i").replace(u"\xf3", "o").replace(u"\xf1", "n").replace(u"\xe1", "a").encode('utf8'))

                headers = {'Content-type': 'application/json'}
                if len(newsTitle) > 0 and (len(newsSummary) > 0 or len(newsContainLi) > 0):
                    newsSummary0 = str(newsSummary[0].replace(u"\u2018", "").replace(u"\u2019", "").replace(u"\u201c", "E").replace(u"\xed", "i").replace(u"\xf3", "o").replace(u"\xf1", "n").replace(u"\xe1", "a").encode('utf8'))
                    data = {"title": newsTitle0, "body": newsSummary0, "likes": '2', "imgUrl": newsImg0, "source": "http://www.marca.com/"}
                
                data_json = json.dumps(data)
                url = "http://localhost:9000/v1/news"
                responsePost = requests.post(url, data=data_json, headers=headers)
            except Exception as e:
                print(str(e))
                print("Exception in the scrapping")
            else:
                pass
            finally:
                pass
        
        self.log('Spider 3 run')