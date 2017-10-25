# -*- coding: utf-8 -*-
import scrapy
from terrorScrapper.items import TerrorscrapperItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import re


class IndianTerrorismSpider(scrapy.Spider):
    name = 'IndianTerrorismSpider'
    allowed_domains = ['southasiaterrorism.trfetzer.com']
    start_urls = ['http://southasiaterrorism.trfetzer.com/countries/IND.html']
    states_by_district = dict()

    def parse(self, response):
        self.log("parse: visiting {}".format(response.url))
        # state = response.xpath('//table/tbody/tr/td/a[contains(@href, "states")]/@href').extract()[1]
        # state = response.urljoin(state)
        # yield scrapy.Request(url=state, callback=self.parse_state)
        states = response.xpath('//table/tbody/tr/td/a[contains(@href, "states")]')
        for state in states:
            self.log('current state: {}'.format(state.css('a::text').extract_first()))
            # get the next url to go
            next_state_url = state.css('a::attr("href")').extract_first()
            next_state_url = response.urljoin(next_state_url)
            if next_state_url:
                yield scrapy.Request(url=next_state_url, callback=self.parse_state)

    def parse_state(self, response):
        self.log("parse_state: visiting {}".format(response.url))
        # district = response.xpath('//table/tbody/tr/td/a[contains(@href, "districts")]/@href').extract_first()
        # district = response.urljoin(district)
        # yield scrapy.Request(url=district, callback=self.parse_district)
        districts = response.xpath('//table/tbody/tr/td/a[contains(@href, "districts")]')
        for district in districts:
            # get the next url to go
            next_district_url = district.css('a::attr("href")').extract_first()
            next_district_url = response.urljoin(next_district_url)
            if next_district_url:
                yield scrapy.Request(url=next_district_url, callback=self.parse_district)

    def parse_district(self, response):
        self.log("parse_district: visiting {}".format(response.url))
        self._add_state(response.css('h1::text').extract_first())
        # parse event id's using BeautifulSoup, as the event urls are wrapped in javascript
        soup = BeautifulSoup(response.text, 'lxml')
        js_text = ''
        for t in soup.findAll('script', type="text/javascript"):
            js_text += t.text
        event_urls = re.findall(r'href=[\'"]?([^\'" >]+)', js_text)

        for event in event_urls:
            yield scrapy.Request(url=response.urljoin(event), callback=self.parse_event)

    def parse_event(self, response):
        self.log("parse_event: visiting {}".format(response.url))
        item = ItemLoader(TerrorscrapperItem(), response)
        district = response.xpath('//code[@class="knitr inline"]/a/text()').extract_first()
        item.add_value('state', self.states_by_district.get(district, 'unknown'))
        item.add_value('district', district)
        item.add_xpath('eventid', '//tbody/tr/td/a/text()')
        item.add_xpath('date', '//tbody/tr/td[2]/text()')
        item.add_xpath('metalocation', '//ul/li/code/text()')
        item.add_xpath('actgroup', '//ul/li[3]/code/text()')
        item.add_xpath('actor', '//ul/li[4]/code/text()')
        item.add_xpath('subject', '//ul/li[5]/code/text()')
        # indicator treatment
        if "Maoist" in response.xpath('//p[2]/code/text()').extract_first():
            item.add_value('indicator', '1')
        else:
            item.add_value('indicator', '0')

        yield item.load_item()

    def _add_state(self, s):
        """
        Fetch the state and district info from given string
        """
        self.log("_add_state: treated string: {}".format(s))
        # ignore the first part of given string (Incidents in )
        split_list = [it.strip() for it in s[13:].split(',')]
        # index 0 represent district, index of 1: state
        self.states_by_district[split_list[0]] = split_list[1]

    def __del__(self):
        # TODO remove at the end
        print(self.states_by_district)
