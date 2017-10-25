# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt


class TerrorscrapperPipeline(object):
    def __init__(self):
        object.__init__(self)
        self.book = xlwt.Workbook()
        self.worksheet = self.book.add_sheet("TerrorismData")
        self.col_names = ["State", "District", "EventID", "Date", "MetaLocation", "ActGroup", "Actor", "Subject", "Indicator"]
        self.add_column_headers()
        # store the current row in excel
        self.current_row_id = 1

    def process_item(self, item, spider):
        spider.log("Got the item from spider")
        self.store_item_to_excel(item)

    def store_item_to_excel(self, item):
        current_row = self.worksheet.row(self.current_row_id)
        for index, col_name in enumerate(self.col_names):
            current_row.write(index, item.get(col_name.lower(), ""))

        self.current_row_id += 1

    def add_column_headers(self):
        # add column header names to excel
        for col_num, col_name in enumerate(self.col_names):
            self.worksheet.write(0, col_num, col_name)

    def __del__(self):
        self.book.save("TerrorismData.xls")
