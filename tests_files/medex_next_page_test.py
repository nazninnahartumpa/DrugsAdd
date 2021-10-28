import scrapy
import time
import requests
import json


class MedexSpider(scrapy.Spider):
    name = "medex_next_test"


    allowed_domains = ['medex.com.bd']

    start_urls = ['https://medex.com.bd/brands']

    base_url = 'https://medex.com.bd/'
            

    def parse(self, response):
        page = response.url
        print('page', page)


        #################----------------------------MeDex website codes for sraping-------------#########

        #############---------------------Getting medex website's url-----------------------############
        medex_drug_link_list = response.xpath('//*[@id="ms-block"]/section/div/div[2]/div/a//@href').extract()
        #############---------------------End Getting medex website's url-----------------------############

        #############---------------------Getting medex website's drug name-----------------------############
        medex_drug_names = response.xpath('//*[@class="md-icon-container"]/parent::div//text()[2]').extract()
        medex_drug_name_list = []
        for drug_name in medex_drug_names:
            medex_drug_name_list.append(drug_name.strip())
        #############---------------------End Getting medex website's drug name-----------------------############

      
        #############---------Getting website's drug name and url in a dictionary and then append that's dictionary in a list--------############
        medex_drug_list =[]
        for medex_drug_name in medex_drug_name_list:
            for medex_drug_url in medex_drug_link_list:
                medex_drug_link_list.remove(medex_drug_url)
                break
            yield scrapy.Request(medex_drug_url, callback=self.parse_details)
            # medex_drug_list.append({'name':medex_drug_name, 'url':medex_drug_url})
        #############---------Getting website's drug name and url in a dictionary and then append that's dictionary in a list--------############

        
            


        next_word = response.xpath('//*[@rel="next"]/@href').extract_first()
        if next_word:
            print('next_word', next_word)
            yield scrapy.Request(next_word, callback=self.parse)


    def parse_details(self, response):

        # scrape drug name
        try:
            Name = response.xpath('//h1/span[2]/text()').extract_first()
#             print('Name', Name)
        except:
            Name = ''

        yield Name