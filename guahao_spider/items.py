# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class HospitalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # query
    hospital_name = Field()
    hospital_grade = Field()

    num_appointments = Field()
    num_comments = Field()

class CommentItem(scrapy.Item):
    hospital_name = Field()
    hospital_grade = Field()

    disease = Field()
    score = Field()
    text = Field()
    doctor = Field()
    date = Field()

class CommentList(scrapy.Item):
    items = Field()
