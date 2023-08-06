"""
The Open Source License Compatibility check API provides access to a wide range of
legal information and resources. It allows developers to retrieve information about
 software licenses, legal documents, legal entities, check license compatibility, 
 and more. The API aims to facilitate the integration of legal information into 
 applications, websites, or other software systems.

"""


import requests

class Compatibility:

    """
    This is a class that consumes the Legalzard API to retrieve information about 
    software licenses, legal documents, legal entities, check license compatibility.
    It has provides methods to interact with a REST 
    API for managing software licenses.
    
    """

    def __init__(self):
        """The base URL of the API."""
        self.base_url = "https://100080.pythonanywhere.com/api/licenses/"

    def create_licence(self, data):
        '''
        Create a new licence
        
        :param data: The json data with format as shown in `README.md`
        :return: Response returns the created licence in json format, with a status 
        message set to True if
          succesful.
        
        '''
        # Make a POST request to the API.
        response = requests.post(self.base_url, json=data, timeout=10)
        if response.status_code == 201:
            return response.json()
        return {"Error code: " : response.status_code}

    def retrieve_a_licence(self, licence_id):
        """
        Retrieve a Licence by ID.
        
        :param id: The licence id for the particular licence being retrieved.
        :return: If ID is not specified, it retrieves all licenses. Otherwise it 
        retrieves the Licence with teh specified ID

        """
        response = requests.get(f"{self.base_url}/{licence_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"Error code: ", response.status_code}

    def retrieve_licences(self):
        """
        Retrieve all Licences.
        
        :param id(optional): The licence id for the particular licence being retrieved.
        :return: If ID is not specified, it retrieves all licenses. Otherwise it 
        retrieves the Licence with teh specified ID

        """
        response = requests.get(self.base_url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"Error code: ", response.status_code}

    def update_licence(self, licence_id, data):
        """
        Update a Licence by ID.
        
        :param id: The id of the licence to be updated.
        :param data: The json data with format as shown in `json_sample.json`
        :return: Response returns a json of the updated licence.
        """
        response = requests.put(f"{self.base_url}/{licence_id}", json=data, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"Error code: " : response.status_code}

    def delete_licence(self, licence_id):
        """
        
        Delete a licence by ID.
        
        :param id: The id of the licence to be deleted.
        :return: Response an event_id of the deleted licence and a status of 
        success if deleted.
        
        """
        response = requests.delete(f"{self.base_url}/{licence_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"Error code: " : response.status_code}

    def search_licence(self, term):
        """
        
        Search for a type of licence
        
        :param term: The is the type of licence to be searched, e.g mit.
        :return: Response returns a json containing a list of the type of licence
         searched

        """
        response = requests.get(f"{self.base_url}/?search_term={term}&action_type=search", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"Error code: " : response.status_code}

    def check_licence_compatibility(self, event_id_one,event_id_two, user_id, organization_id):
        '''
        Checks how compatible two licences are
        
        :param event_id_one: The id of the first licence's event_id
        :param event_id_two: The id of the second licence's event_id
        :param user_id: The user's ID
        :param organization_id: the organization's ID
        :return: Response returns a json that contains percentage_of_compatibility,
         along with other related comparison information of the two licences

        '''
        # Create a dictionary of data to send to the API.
        data = {
            "action_type": "check-compatibility",
            "license_event_id_one": event_id_one,
            "license_event_id_two": event_id_two,
            "user_id": int(user_id),
            "organization_id": organization_id
        }
        response = requests.post(self.base_url, json=data, timeout=10)
        if response.status_code == 201:
            return response.json()
        return {"Error code: " : response.status_code}

    def comparison_history(self, organization_id, user_id):
        '''
        Retrieves the comparison history

        :param organization_id: the organization's ID
        :param user_id: The user's ID
        :return: Response returns a json that contains a history of the comparisons
         done by the organization and the user
        
        '''
        url = f"{self.base_url}/?collection_type=license-compatibility-history"
        response = requests.get(f"{url}&organization_id={organization_id}&user_id={user_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"Error code: " : response.status_code}
    