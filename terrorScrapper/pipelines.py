# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt


class TerrorscrapperPipeline(object):
    def process_item(self, item, spider):
        return item


def test():
    book = xlwt.Workbook()
    worksheet = book.add_sheet("TerrorismData")

    colnames = ["State", "District", "EventID", "Date", "MetaLocation", "ActGroup", "Actor", "Subject", "Indicator"]

    # add column names
    for colnum, colname in enumerate(colnames):
        worksheet.write(0, colnum, colname)

    for rownum in range(1, 10):
        row = worksheet.row(rownum)
        for i in range(len(colnames)):
            row.write(i, "{} - {}".format(rownum, i))

    book.save("test.xls")

