# -*- coding: utf-8 -*-
import scrapy
from terrorScrapper.items import TerrorscrapperItem
from scrapy.loader import ItemLoader


class IndianTerrorismSpider(scrapy.Spider):
    name = 'IndianTerrorismSpider'
    allowed_domains = ['http://southasiaterrorism.trfetzer.com/countries/IND.html']
    start_urls = ['http://http://southasiaterrorism.trfetzer.com/countries/IND.html/']

    def parse(self, response):
        item = ItemLoader(TerrorscrapperItem, response)
        next_page_url = response.urljoin(response.css('li.next > a::attr(href)').extract_first())
