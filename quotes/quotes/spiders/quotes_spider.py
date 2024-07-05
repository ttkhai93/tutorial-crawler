from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = "https://quotes.toscrape.com/"
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = url + "tag/" + tag
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            text = quote.css("span.text::text").get()
            author = quote.css("small.author::text").get()
            tags = quote.css("div.tags a.tag::text").getall()
            yield (dict(text=text, author=author, tags=tags))

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            # next_url = response.urljoin(next_page)
            # yield scrapy.Request(next_url, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)

        # for quote in response.css("div.quote"):
        #     yield {
        #         "author": quote.xpath("span/small/text()").get(),
        #         "text": quote.css("span.text::text").get(),
        #     }

        # next_page = response.css("li.next a::attr('href')").get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
