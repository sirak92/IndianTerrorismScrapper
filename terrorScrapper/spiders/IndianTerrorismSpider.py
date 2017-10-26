# -*- coding: utf-8 -*-
import re
import scrapy
from terrorScrapper.items import TerrorscrapperItem, TerrorLoader
from bs4 import BeautifulSoup


class IndianTerrorismSpider(scrapy.Spider):
    name = 'IndianTerrorismSpider'
    allowed_domains = ['southasiaterrorism.trfetzer.com']
    start_urls = ['http://southasiaterrorism.trfetzer.com/countries/IND.html']
    states_by_district = dict()

    def parse(self, response):
        states = response.xpath('//table/tbody/tr/td/a[contains(@href, "states")]')
        for state in states:
            # get the next url to go
            next_state_url = state.css('a::attr("href")').extract_first()
            next_state_url = response.urljoin(next_state_url)
            if next_state_url:
                yield scrapy.Request(url=next_state_url, callback=self.parse_state)

    def parse_state(self, response):
        districts = response.xpath('//table/tbody/tr/td/a[contains(@href, "districts")]')
        for district in districts:
            # get the next url to go
            next_district_url = district.css('a::attr("href")').extract_first()
            next_district_url = response.urljoin(next_district_url)
            if next_district_url:
                yield scrapy.Request(url=next_district_url, callback=self.parse_district)

    def parse_district(self, response):
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
        item = TerrorLoader(TerrorscrapperItem(), response)
        district = response.xpath('//code[@class="knitr inline"]/a/text()').extract_first()
        if not self.states_by_district.get(district):
            # if the given district have not state defined it means that there is some inconsistency
            # e.g for district Wardha(http://southasiaterrorism.trfetzer.com/districts/17509-IND-Wardha.html) the
            # last event id in table(http://southasiaterrorism.trfetzer.com/events/37694-71753-171659.html) have the district name(Bid)
            return None

        item.add_value('state', self.states_by_district.get(district, 'unknown'))
        item.add_value('district', district)
        item.add_xpath('eventid', '//tbody/tr/td/a/text()')
        item.add_xpath('date', '//tbody/tr/td[2]/text()')
        item.add_xpath('metalocation', '//ul/li/code/text()')
        item.add_xpath('actgroup', '//ul/li[3]/code/text()')
        item.add_xpath('actor', '//ul/li[4]/code/text()')
        item.add_xpath('subject', '//ul/li[5]/code/text()')
        item.add_xpath('indicator1', '//p[2]/code/text()')
        item.add_xpath('indicator2', '//p[2]/code/text()')
        yield item.load_item()

    def _add_state(self, s):
        """
        Fetch the state and district info from given string
        """
        # ignore the first part of given string (Incidents in )
        split_list = [it.strip() for it in s[13:].split(',')]
        # index 0 represent district, index of 1: state
        self.states_by_district[split_list[0]] = split_list[1]
