# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class TerrorscrapperItem(scrapy.Item):
    state = Field()
    district = Field()
    eventId = Field()
    date = Field()
    metaLoc = Field()
    actGrp = Field()
    actor = Field()
    subject = Field()
    indicator = Field()

