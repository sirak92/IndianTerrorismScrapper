# -*- coding: utf-8 -*-
import scrapy
from terrorScrapper.items import TerrorscrapperItem
from scrapy.loader import ItemLoader


class IndianTerrorismSpider(scrapy.Spider):
    name = 'IndianTerrorismSpider'
    allowed_domains = ['http://southasiaterrorism.trfetzer.com/countries/IND.html']
    start_urls = ['http://southasiaterrorism.trfetzer.com/countries/IND.html']

    def parse(self, response):
        self.log("visiting {}".format(response.url))
        states = response.xpath('//table/tbody/tr/td/a[contains(@href, "states")]')
        for state in states:
            self.log('current state: {}'.format(state.css('a::text').extract_first()))
            # get the next url to go
            next_state_url = state.css('a::attr("href")').extract_first()
            next_state_url = response.urljoin(next_state_url)
            if next_state_url:
                yield scrapy.Request(url=next_state_url, callback=self.parse_state)

    def parse_state(self, response):
        self.log("visiting {}".format(response.url))
        districts = response.xpath('//table/tbody/tr/td/a[contains(@href, "districts")]')
        for district in districts:
            # get the next url to go
            next_district_url = district.css('a::attr("href")').extract_first()
            next_district_url = response.urljoin(next_district_url)
            if next_district_url:
                yield scrapy.Request(url=next_district_url, callback=self.parse_district)

    def parse_district(self, response):
        self.log("visiting {}".format(response.url))
        # TODO get the correct events table and iterate over it
        events = response.xpath('//table/tbody/tr/td/a[contains(@href, "districts")]')
        for event in events:
            # get the next url to go
            next_event_url = event.css('a::attr("href")').extract_first()
            next_event_url = response.urljoin(next_event_url)
            if next_event_url:
                yield scrapy.Request(url=next_event_url, callback=self.parse_event)

    def parse_event(self, response):
        self.log("visiting {}".format(response.url))
        # TODO use own created item and item loader fill up fields
