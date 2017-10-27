# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader


# defining item for storing terror data
class TerrorscrapperItem(scrapy.Item):
    state = Field()
    district = Field()
    eventid = Field()
    date = Field()
    metalocation = Field()
    actgroup = Field()
    actor = Field()
    subject = Field()
    indicator1 = Field()
    indicator2 = Field()


# defining separate matching lists and input processors for each indicator
match_list1 = ["Naxal", "naxal", "Peoples' War Group", "Peoples War Group", "MCC", "PWG",
               "Left-Wing", "left-wing", "Left-wing", "Left Wing", "Left wing", "left wing",
               "Maoist", "maoist", "CPI-(ML)", "CPI-M",
               "Marxist", "Leninist", "Communist", "communist"]

match_list2 = ["Lashkar", "Toiba", "Fidayeen", "Mujahideen", "LeT", "Harkat", "HuJI",
               "JeM", "SIMI", "Hizbul", "Qaeda", "Qaida", "Jaish", "Jamaat",  "Islamic",
               "Taliban", "ISIS",  "Jihad", "Dukhtaran-e-Millat", "Deendar Anjuman", "Osama bin Laden"]


def ind1_process(value):
    for l in match_list1:
        if l in value:
            return '1'
    return '0'


def ind2_process(value):
    for l in match_list2:
        if l in value:
            return '1'
    return '0'


class TerrorLoader(ItemLoader):
    # defining default input and output constructors
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    indicator1_in = MapCompose(ind1_process)
    indicator2_in = MapCompose(ind2_process)
