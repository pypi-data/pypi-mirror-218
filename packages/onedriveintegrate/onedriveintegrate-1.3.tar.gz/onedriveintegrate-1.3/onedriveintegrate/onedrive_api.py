# Import the os, requests, and json modules
import os, requests, json

# Import generate_access_token, GRAPH_API_ENDPOINT from ms_graph.py
from .ms_graph import generate_access_token, GRAPH_API_ENDPOINT

class OneDriveAPI:
    """The OneDriveAPi class provides OneDrive file management capabilities"""
    
    def __init__ (self, client_ID):
        """
        __init__() initializes the OneDriveAPI class

        :param client_ID: the user's client_ID
        """
        self.client_ID = client_ID;
    
    def authenticate(self, permissions):
        """
        authenticate() authenticates the user and generates an access token

        :param permissions: list of permissions to request
        :return: a dictionary containing the authorization headers
        """
        access_token = generate_access_token(self.client_ID, permissions)
        return {
            'Authorization': 'Bearer ' + access_token['access_token']
        }

    def write_file(self, folder_id, file_path):
        """
        write_file() uploads a provided file into a specific folder

        :param folder_id: the id of the folder to wite the file into
        :param file_path: the relative path of the file to input
        """
        permissions = ['Files.ReadWrite']
        headers = self.authenticate(permissions);

        file_name = os.path.basename(file_path);
        with open(file_path, 'rb') as upload:
            file_content = upload.read()
            response = requests.put(
                GRAPH_API_ENDPOINT + f'/me/drive/items/{folder_id}:/{file_name}:/content',
                headers = headers,
                data = file_content
            )
    
    def read_file(self, file_id):
        """
        read_file() downloads a user-specified file

        :param file_id: the id of the file to download
        """
        permissions = ['Files.Read.All']
        headers = self.authenticate(permissions);
        save_location = os.getcwd()

        file_data = requests.get(
            GRAPH_API_ENDPOINT + f'/me/drive/items/{file_id}',
            headers=headers,
            params={'select': 'name'}
        )
        file_name = file_data.json().get('name')

        response = requests.get(
            GRAPH_API_ENDPOINT + f'/me/drive/items/{file_id}/content', 
            headers=headers
        )
        with open(os.path.join(save_location, file_name), 'wb') as new_file:
            new_file.write(response.content)
    
    def list_folder(self, folder_id, output_name):
        """
        list_folder() gives a list of files in the provided folder

        :param folder_id: the id of the folder to retrieve its contents
        :param output_name: the name of the JSON file to output
        """
        permissions = ['Files.Read.All']
        headers = self.authenticate(permissions);

        response = requests.get(
            GRAPH_API_ENDPOINT + f'/me/drive/items/{folder_id}/children',
            headers=headers
        )
        with open(output_name, "w") as json_file:
            json.dump(response.json(), json_file, indent=4)
    
    def search_text(self, search_text, output_name):
        """
        search_files() searches for a file containing the specified search text

        :param search_text: the text to search
        :param output_name: the name of the JSON file to output
        """
        permissions = ['Files.Read.All']
        headers = self.authenticate(permissions);

        response = requests.get(
            GRAPH_API_ENDPOINT + f"/me/drive/root/search(q='{search_text}')",
            headers=headers
        )
        with open(output_name, "w") as json_file:
            json.dump(response.json(), json_file, indent=4)

    def search_id(self, search_id, output_name):
        """
        search_id() searches for a file containing the specified id

        :param search_text: the id to search
        :param output_name: the name of the JSON file to output
        """
        permissions = ['Files.Read.All']
        headers = self.authenticate(permissions);

        response = requests.get(
            GRAPH_API_ENDPOINT + f"/me/drive/items/{search_id}",
            headers=headers
        )
        with open(output_name, "w") as json_file:
            json.dump(response.json(), json_file, indent=4)