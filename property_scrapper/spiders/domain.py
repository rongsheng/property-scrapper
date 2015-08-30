# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse, Request
from scrapy.contrib.loader import ItemLoader
from property_scrapper.items import PropertyScrapperItem


class DomainSpider(scrapy.Spider):
    name = 'domain'
    allowed_domains = ['domain.com.au']
    site_url = 'http://www.domain.com.au/'
    start_urls = (
        site_url + 'search/sold/property/types/apartment-unit-flat/duplex/house/townhouse/villa/state/nsw/area/canterbury-bankstown/region/sydney-region/suburb/revesby/?sort=date-asc',
    )
    feature = ('bed', 'bath', 'parking')

    def process(self, item):
        item = self._process_feature(item)
        return item

    def _process_feature(self, item):
        print item
        if item and 'bed' in item:
            features = item['bed'].split(',') # get the feature from bed attribute
            for index, feature in enumerate(features):
                item[self.feature[index]] = int(filter(str.isdigit, feature))
        return item

    def parse(self, response):
        links = response.css('#searchresults li.new-listing>div>a::attr(href)').extract()[:1]
        for link in links:
            url = self.site_url + link
            self.log('Found item link: {}'.format(url))
            yield Request(url, callback=self.parse_property)

    def parse_property(self, response):
        loader = ItemLoader(PropertyScrapperItem(), response=response)
        loader.add_css('address', '.property-address::text')
        loader.add_css('suburb', 'dl.cN-featDetails-extended dd.suburb a::text')
        # loader.add_css('description', 'div.main div.cT-productDescription')
        loader.add_css('sold_date', 'dl.cN-featDetails-extended dd.saleDate::text')
        loader.add_css('sold_price', 'dl.cN-featDetails-extended dd.price::text')
        loader.add_css('property_type', 'dl.cN-featDetails-extended dd.propertytype::text')
        loader.add_css('floorplan_url', '#Content_Content_propertyPhotos_FloorplanLink::attr(href)')
        loader.add_css('photo_url', '#Content_Content_propertyPhotos_lnkPhoto::attr(href)')
        loader.add_css('sales_type', 'dl.cN-featDetails-extended dd.saleType::text')
        
        # domain uses feature to represents bed + bath + parking,
        # we store this feature in bed, and process it later in self.process
        loader.add_css('bed', 'dl.s-featSummary dd p.features span::text')
        yield self.process(loader.load_item())

