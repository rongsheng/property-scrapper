# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PropertyScrapperItem(scrapy.Item):
    address = scrapy.Field()
    suburb = scrapy.Field()
    description = scrapy.Field()
    sold_date = scrapy.Field()
    sold_price = scrapy.Field()
    bed = scrapy.Field()
    bath = scrapy.Field()
    parking = scrapy.Field()
    property_type = scrapy.Field()
    floorplan_url = scrapy.Field()
    photo_url = scrapy.Field()
    sales_type = scrapy.Field()





    
