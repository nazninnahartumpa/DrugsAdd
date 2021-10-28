import requests
import json


def bahmni_drug():
        ###-----getting bahmni drug name list for matching the drugs which we should scrape------####### 
        drug_name_list = []
        ###----drug url of bahmni---####
        url = 'https://openemr.accelx.net/openmrs/ws/rest/v1/drug'
        ##----next_text flug variable for ---####
        next_text = 'next'

        ####---taking response for the first page----####
        response = requests.get(url, auth=("superman", "Admin123"), verify=False)

        ###----taking the drug name from the first page drug list response---####
        for drug_name in response.json()['results']:

            ####-----add the drug_name to the drug name list----####
            drug_name_list.append(drug_name['display'])
            
            ####-----Giving condition for the next page that if next page comes then go to the next page----####
            while next_text == 'next':
                
                ######------getting response from the first next page------#########
                response = requests.get(url, auth=("superman", "Admin123"), verify=False)
                print('url', url)
                #######-----getting drug_name from the first next page----######
                for next_drug_name in response.json()['results']:
                    #####------adding drug_name to the list of drug_name_list-----#######
                    drug_name_list.append(next_drug_name['display'])
                    
                try:
                    #####------giving condition that if next page comes it will go to the next page-----#######
                    if response.json()['links'][0]['rel'] == 'next':
                    
                        ######------change the value of next_text variable and fill it with next text----#####
                        next_text = response.json()['links'][0]['rel']
                        #######----change the url to the next page url----#######
                        url = response.json()['links'][0]['uri']
                    
                    else:
                        next_text = response.json()['links'][0]['rel']
                        print('there is no next url')
                        break
                        
                except:
                    print('End of try catch')

        return drug_name_list






def drug_upload(Generic_Name, Name, Dosage_Form, Description):

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

 
    