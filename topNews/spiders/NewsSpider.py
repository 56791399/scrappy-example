import scrapy

# //div[@class='ab-column column']//div[@class='collection']//h2[@class='story-heading']
class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        urls = [
            'https://www.nytimes.com'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        data = str(response.xpath("//div[@class='ab-column column']//div[@class='collection']//h2[@class='story-heading']//a").extract())
        filename = 'news-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(data)
        self.log('Saved file %s' % filename)