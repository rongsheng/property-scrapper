from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class PropertyLoader(ItemLoader):

	default_output_processor = TakeFirst()
	name_in = Map