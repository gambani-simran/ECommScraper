# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class FlipkartSpider(scrapy.Spider):
    name = 'flipkart'
    allowed_domains = ['www.flipkart.com/search?q=laptop']
    start_urls = ['http://www.flipkart.com/search?q=laptop/']

    def parse(self, response):
        #Extracting the content using css selectors
        desc = response.css('._3wU53n::text').extract()
        price = response.css('._1vC4OE._2rQ-NK::text').extract()
        rating = response.css('.hGSR34._2beYZw::text').extract()
       
        #Give the extracted content row wise
        for item in zip(desc,price,rating):
            #create a dictionary to store the scraped info
            scraped_info = {
                'desc' : item[0],
                'price' : item[1],
                'rating' : item[2],  
            }
            #yield or give the scraped info to scrapy
            yield scraped_info
        
        next_page_url = response.css('div._2kUstJ > a::attr(href)').extract_first()
        print next_page_url
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            print next_page_url
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)
