# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy.loader.processors import Join, TakeFirst


class TerrorscrapperItem(scrapy.Item):
    state = Field(output_processor=Join())
    district = Field(output_processor=Join())
    eventid = Field(input_processor=TakeFirst(), output_processor=Join())
    date = Field(input_processor=TakeFirst(), output_processor=Join())
    metalocation = Field(input_processor=TakeFirst(), output_processor=Join())
    actgroup = Field(input_processor=TakeFirst(), output_processor=Join())
    actor = Field(input_processor=TakeFirst(), output_processor=Join())
    subject = Field(input_processor=TakeFirst(), output_processor=Join())
    indicator = Field(output_processor=Join())

