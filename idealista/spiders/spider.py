# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import datetime

class SpiderSpider(scrapy.Spider):
	contador = 0
	name = 'spider'
	allowed_domains = ['https://www.idealista.com/venta-viviendas/rivas-vaciamadrid-madrid/', 'idealista.com']
	start_urls = ['https://www.idealista.com/venta-viviendas/rivas-vaciamadrid-madrid/pagina-1.htm']

	def parse(self, response):
		urls = response.css('div.item-info-container > a::attr(href)').extract()
		for url in urls:
			url = "https://www.idealista.com" + url
			yield scrapy.Request(url=url, callback=self.parse_details)

		siguiente = response.css('li.next a::attr(href)').extract_first()
		if siguiente:
			siguiente = response.urljoin(siguiente)
			yield scrapy.Request(url=siguiente, callback=self.parse)

	def parse_details(self, response):
	
		#if self.contador > 5:
		#	raise CloseSpider('item_exceeded')
		yield {
	
			'fecha':datetime.datetime.now(),
			'titulo':response.css('h1 > span::text').extract_first(),
			#precio = response.css('div.info-data > span > span::text').extract_first()
			'precio':response.css('div.info-data  span:nth-child(1)  span::text').extract_first(),
			'metros':response.css('div.info-data  span:nth-child(2)  span::text').extract_first(),
			'habitaciones':response.css('div.info-data  span:nth-child(3)  span::text').extract_first(),
			'telefono':response.css('div.phone p::text').extract_first(),
			'profesional':response.css('p.professional-name::text').extract_first(),
			'descripcion':response.css('div.adCommentsLanguage::text').extract(),
			'ubicacion':response.xpath('//*/div[@id="addressPromo"]/ul/li/text()').extract(),
			'cuota':response.css('p + p.price::text').extract_first(),
			'caracteristicas':response.css('h2 + ul li::text').extract(),
			'localizacion':response.xpath('//*/a[@class="showMap"]/img/@src').extract(),
			'url':response.url,

		}
    	

