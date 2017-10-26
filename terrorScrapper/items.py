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


# defining separate input processors for each indicator
indicator1_list = ["Naxalite", "Naxalites", "Naxal", "Left-Wing", "naxalite", "naxal", "left-wing", "Left-wing",
                   "PWG", "M aoist", "Peoples ' War Group", "Peoples War Group", "Maoist Communist Center", "MCC",
                   "CPI-M aoist", "Maoists", "Communist Party of India (Marxist–Leninist)", "CPI-(ML)", "Maoist"]


indicator2_list = ["Lashkar", "Toiba", "Fidayeen", "Osama bin Laden", "Hizbul Mujahideen", "Lashkar - e - Toiba",
                   "LeT", "Harkat - ul - Jehadi - e - Islami", "HuJI", "JeM", "Indian Mujahideen", "SIMI",
                   "Islamic", "Al-Qaeda", "Al-Qaida", "Taliban", "ISIS", "Jaish-e-Mohammed", "Mujahideen",
                   "Jihad", "Harkat", "Dukhtaran-e-Millat", "Deendar Anjuman", "Jamaat-ul-Mujahideen",
                   "Students Islamic Movement of India"]


def ind1_process(value):
    for l in indicator1_list:
        if l in value:
            return '1'
    return '0'


def ind2_process(value):
    for l in indicator2_list:
        if l in value:
            return '1'
    return '0'


class TerrorLoader(ItemLoader):
    # defining default input and output constructors
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    indicator1_in = MapCompose(ind1_process)
    indicator2_in = MapCompose(ind2_process)
