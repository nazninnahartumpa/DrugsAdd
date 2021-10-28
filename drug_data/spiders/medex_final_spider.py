### This script is written by Naznin
### Here two helper function is used (bahmni_drug: getting all drug name from bahmni and drug_upload: upload drug and generic name)
### Helper function file name is bahmni_drug_section.py
### Version 01
### Copyrigt by Accelx Inc. 


import scrapy
import time
import requests
import json
from .bahmni_drug_section import bahmni_drug, drug_upload


class MedexSpider(scrapy.Spider):
    name = "medex"

    allowed_domains = ['medex.com.bd']

    start_urls = ['https://medex.com.bd/brands']

    base_url = 'https://medex.com.bd/'



    def parse(self, response):
        page = response.url
        print('page', page)

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
        #####---------getting single medex drug name from medex drug name lists ---------#######
        for medex_drug_name in medex_drug_name_list:
            #####---------getting single medex drug url from medex drug url lists ---------#######
            for medex_drug_url in medex_drug_link_list:
                #####---------getting single medex drug url and remove that url from the loop and break that loop---------#######
                medex_drug_link_list.remove(medex_drug_url)
                break
            medex_drug_list.append({'name':medex_drug_name, 'url':medex_drug_url})
        #############---------Getting website's drug name and url in a dictionary and then append that's dictionary in a list--------############


        #############---------Getting drug name which doesn't match from the bahmni drug lists--------############
        unmatching_drug_url_list = []

       ####-----getting bahmni drug name list---#####
       #####-----------------This bahmni_drug function is from bahmni_drug_section.py-------########
        bahmni_drug_name_list = bahmni_drug()

        for medex_drug in medex_drug_list:
            #####-------match the drug name from bahmni drug lists--------######### 
            if medex_drug['name'] not in bahmni_drug_name_list:
                print('medex_drug', medex_drug['name'])
                ####--------append the unmatched drug in the unmatching_drug_url_list------#######
                unmatching_drug_url_list.append(medex_drug['url'])
         #############---------End of Getting drug name which doesn't match from the bahmni drug lists and append them in a list--------############

        for link in unmatching_drug_url_list:
            yield scrapy.Request(link, callback=self.parse_details)


        ##### If any next page comes then go to the next page and find the drug name ########
        next_page_link = response.xpath('//*[@rel="next"]/@href').extract_first()
        if next_page_link:
            print('next_page_link', next_page_link)
            yield scrapy.Request(next_page_link, callback=self.parse)
        else:
            print('No next page')
        

    def parse_details(self, response):

         # scrape drug name
        try:
            Name = response.xpath('//h1/span[2]/text()').extract_first()
#             print('Name', Name)
        except:
            Name = ''
       
        try:
            Generic_Name = response.xpath('//*[@title="Generic Name"]//a/text()').extract_first().strip()
#             print('Generic Name', Generic_Name)
        except:
            Generic_Name = ''
            
        # scrape Strength
        time.sleep(1)
        try:
            Strength = response.xpath('//*[@title="Strength"]/text()').extract_first().strip()
#             print('Strength', Strength)
        except:
            Strength = ''
            
        # scrape Dosage Form
        try:
            Dosage_Form = response.xpath('//*[@title="Dosage Form"]/text()').extract_first().strip()
#             print('Dosage_Form', Dosage_Form)
        except:
            Dosage_Form = ''
            
        # scrape price
        time.sleep(1)
        try:
            Price = response.xpath('//*[@class="package-container"]/text()').extract_first()
            
#             print('Price', Price)
        except:
            Price = ''
            
        # # scrape Manufactured by
        # Pharmacy = self.response.xpath('//*[@title="Manufactured by"]//a/text()').extract_first()
        # print('Pharmacy', Pharmacy)

        # scrape Manufactured by
        try:
            Pharmacy  = response.xpath('//*[@title="Manufactured by"]//a/text()').extract_first().strip()
#             print('Pharmacy', Pharmacy)
        except:
            Pharmacy = ''
            
        # scrape Indications
        try:
            Indications  = response.xpath('//*[@id="indications"]/following-sibling::div/text()').extract_first()
#             print('Indications', Indications)
        except:
            Indications = ''
            
        # scrape Description
        time.sleep(1)
        try:
            Description  = response.xpath('//*[@id="description"]//following-sibling::div/text()').extract_first()
#             print('Description', Description)
        except:
            Description = ''

        # scrape Pharmacology
        try:
            Pharmacology  = response.xpath('//*[@id="mode_of_action"]/following-sibling::div/text()').extract_first()
#             print('Pharmacology', Pharmacology)
        except:
            Pharmacology = ''

        # scrape Dosage & Administration
        try:
            Dosage_Administration  = response.xpath('//*[@id="dosage"]/following-sibling::div/text()').extract_first()
#             print('Dosage_Administration', Dosage_Administration)
        except:
            Dosage_Administration = ''

        # scrape Interaction
        time.sleep(1)
        try:
            Interaction  = response.xpath('//*[@id="interaction"]/following-sibling::div/text()').extract_first()
#             print('Interaction', Interaction)
        except:
            Interaction = ''

        # scrape Contraindications
        try:
            Contraindications  = response.xpath('//*[@id="contraindications"]/following-sibling::div/text()').extract_first()
#             print('Contraindications', Contraindications)
        except:
            Contraindications = ''
            
        # scrape Side_Effects
        try:
            Side_Effects  = response.xpath('//*[@id="side_effects"]/following-sibling::div/text()').extract_first()
#             print('Side_Effects', Side_Effects)
        except:
            Side_Effects = ''
            
        # scrape Pregnancy_Lactation
        time.sleep(1)
        try:
            Pregnancy_Lactation  = response.xpath('//*[@id="pregnancy_cat"]/following-sibling::div/text()').extract_first()
#             print('Pregnancy_Lactation', Pregnancy_Lactation)
        except:
            Pregnancy_Lactation = ''

        # scrape Precautions_Warnings
        try:
            Precautions_Warnings  = response.xpath('//*[@id="precautions"]/following-sibling::div/text()').extract_first()
#             print('Precautions_Warnings', Precautions_Warnings)
        except:
            Precautions_Warnings = ''
        
        # scrape Therapeutic_Class
        try:
            Therapeutic_Class  = response.xpath('//*[@id="drug_classes"]/following-sibling::div/text()').extract_first()
#             print('Therapeutic_Class', Therapeutic_Class)
        except:
            Therapeutic_Class = ''

        # scrape Storage_Conditions
        try:
            Storage_Conditions  = response.xpath('//*[@id="storage_conditions"]/following-sibling::div/text()').extract_first()
            Storage_Conditions = Storage_Conditions.encode("ascii", "ignore")
            Storage_Conditions = Storage_Conditions.decode()
#             print('Storage_Conditions', Storage_Conditions)
        except:
            Storage_Conditions = ''

        #####-----------------Drug Upload in bahmni--------------############
        #####-----------------This drug_upload function is from bahmni_drug_section.py-------########
        bahmni_drug_upload = drug_upload(Generic_Name, Name, Dosage_Form, Description)
        print(bahmni_drug_upload)

        #####-----------------Drug Upload in bahmni--------------############

        item = {'Name' : Name,
                'Generic_Name' : Generic_Name,
                'Strength':Strength,
                'Dosage_Form': Dosage_Form,
                'Price': Price,
                'Pharmacy' : Pharmacy,
                'Indications' : Indications,
                'Description' : Description,
                'Pharmacology' : Pharmacology,
                'Dosage_Administration': Dosage_Administration,
                'Interaction' : Interaction,
                'Contraindications' : Contraindications,
                'Side_Effects' : Side_Effects,
                'Pregnancy_Lactation' : Pregnancy_Lactation,
                'Precautions_Warnings' : Precautions_Warnings,
                'Therapeutic_Class' : Therapeutic_Class,
                'Storage_Conditions' : Storage_Conditions
               }
        # print('item', item)

        yield item
     






     

