import scrapy
import time
import requests
import json


class MedexSpider(scrapy.Spider):
    name = "testmedex"

    def start_requests(self):
        for i in range(5, 6):

            link = f"https://medex.com.bd/brands?page={i}"

            yield scrapy.Request(url=link, callback=self.parse)
            

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
            medex_drug_list.append({'name':medex_drug_name, 'url':medex_drug_url})
        #############---------Getting website's drug name and url in a dictionary and then append that's dictionary in a list--------############


        #########-----------------------Bahmni codes for getting drug list---------------------------#######
        drug_name_list = []
        url = 'https://openemr.accelx.net/openmrs/ws/rest/v1/drug'
        next_text = 'next'

        response = requests.get(url, auth=("superman", "Admin123"), verify=False)

        for drug_name in response.json()['results']:

            drug_name_list.append(drug_name['display'])
            
            while next_text == 'next':
                
                response = requests.get(url, auth=("superman", "Admin123"), verify=False)
                print('url', url)
                for next_drug_name in response.json()['results']:
                    drug_name_list.append(next_drug_name['display'])
                    
                try:
                    if response.json()['links'][0]['rel'] == 'next':
                    
                        next_text = response.json()['links'][0]['rel']
                        url = response.json()['links'][0]['uri']
                    
                    else:
                        next_text = response.json()['links'][0]['rel']
                        print('there is no next url')
                        break
                        
                except:
                    print('End of try catch')
        ########-----------------------End of Bahmni codes for getting drug list---------------------------####### 


        #############---------Getting drug name which doesn't match from the bahmni drug lists--------############
        unmatching_drug_url_list = []
        # print('drug_name_list', drug_name_list)
        for medex_drug in medex_drug_list:
            if medex_drug['name'] not in drug_name_list:
                print('medex_drug', medex_drug['name'])
                unmatching_drug_url_list.append(medex_drug['url'])
         #############---------End of Getting drug name which doesn't match from the bahmni drug lists and append them in a list--------############

        for link in unmatching_drug_url_list:
            yield scrapy.Request(link, callback=self.parse_details)


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


        
        ################-------------Drug and Concept upload in bahmni----------#####################
        url = "https://openemr.accelx.net/openmrs/ws/rest/v1/drug"

        drug_data = {"concept": Generic_Name,
                "combination": False,
                "name": Name,
                "minimumDailyDose": 1,
                "maximumDailyDose": 5,
                "dosageForm": Dosage_Form}

        headers = {"content-type": "application/json"}

        drug_upload_response = requests.post(url, auth=("superman", "Admin123"), data = json.dumps(drug_data), headers=headers, verify=False)
        print('drug_upload_response', drug_upload_response.json())


        try:
            if drug_upload_response.json()['error']:
                print('drug not uploaded')

                url = f"http://openemr.accelx.net/openmrs/ws/rest/v1/concept/{Generic_Name}"
                concept_response = requests.get(url, auth=("superman", "Admin123"), verify=False)
                print('concept_response', concept_response.json())

                try:
                    if concept_response.json()['error']:
                        url = "https://openemr.accelx.net/openmrs/ws/rest/v1/concept"

                        concept_data = {
                            "names": [
                                {
                                    "name": Generic_Name,
                                    "locale": "en",
                                    "localePreferred": True,
                                    "conceptNameType": "FULLY_SPECIFIED"
                                }
                            ],
                            "datatype": "Text",
                            "version": "1.2.2",
                            "conceptClass": "Drug",
                            "mappings": [],
                            "descriptions": [
                                {
                                    "description": Description,
                                    "locale": "en"
                                }
                            ]
                        }

                        headers = {"content-type": "application/json"}

                        concept_upload_response = requests.post(url, auth=("superman", "Admin123"), data = json.dumps(concept_data), headers=headers, verify=False)
                        print('concept_upload_response', concept_upload_response)


                        again_drug_url = "https://openemr.accelx.net/openmrs/ws/rest/v1/drug"

                        drug_data_again = {"concept": Generic_Name,
                                "combination": False,
                                "name": Name,
                                "minimumDailyDose": 1,
                                "maximumDailyDose": 5,
                                "dosageForm": Dosage_Form}

                        headers = {"content-type": "application/json"}

                        drug_upload_response_again = requests.post(again_drug_url, auth=("superman", "Admin123"), data = json.dumps(drug_data_again), headers=headers, verify=False)
                        print('drug_upload_response_again', drug_upload_response_again)
            
                    else:
                        print('concept is in the bahmni!!!!!!!')

                except KeyError:
                    print('In exception part drug_upload_response_again', drug_upload_response_again)
   
            else:
                print('drug uploaded !!!!!!!!')

        except KeyError:
            print('In exception part drug_upload_response', drug_upload_response)

        ################-------------Drug and Concept upload in bahmni----------##################### 


        
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




     

