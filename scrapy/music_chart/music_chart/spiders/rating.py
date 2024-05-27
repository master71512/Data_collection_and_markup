import scrapy


class RatingSpider(scrapy.Spider):
    name = "rating"
    allowed_domains = ["music.yandex.ru"]
    start_urls = ["https://music.yandex.ru/"]

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parse_page, meta={'scroll_to_end': True})

    def parse_page(self, response):
        rows = response.xpath(
            '//div[contains(@class, "d-track__name")]')
        for row in rows:
            rate = rows.index(row) + 1
            artist = row.xpath(
                './/span[@class="d-track__artists"]/a/text()').get()
            track_name = row.xpath(
                './/div[@class="d-track__name"]/a/text()').get().strip()
            link = response.url[:-1] + \
                row.xpath('.//div[@class="d-track__name"]/a/@href').get()
            yield {'rate': rate,
                   'artist': artist,
                   'track_name': track_name,
                   'link': link}
