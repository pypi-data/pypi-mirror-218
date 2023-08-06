import os, requests, json
from .ms_graph import generate_access_token, GRAPH_API_ENDPOINT

class OneDriveAPI:
    
    def __init__ (self, client_ID):
        self.client_ID = client_ID;
    
    def authenticate(self, permissions):
        access_token = generate_access_token(self.client_ID, permissions)
        return {
            'Authorization': 'Bearer ' + access_token['access_token']
        }

    def write_file(self, folder_id, file_path):
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
        permissions = ['Files.Read.All']
        headers = self.authenticate(permissions);

        response = requests.get(
            GRAPH_API_ENDPOINT + f'/me/drive/items/{folder_id}/children',
            headers=headers
        )
        with open(output_name, "w") as json_file:
            json.dump(response.json(), json_file, indent=4)
    
    def search_files(self, search_text, output_name):
        permissions = ['Files.Read.All']
        headers = self.authenticate(permissions);

        response = requests.get(
            GRAPH_API_ENDPOINT + f"/me/drive/root/search(q='{search_text}')",
            headers=headers
        )
        with open(output_name, "w") as json_file:
            json.dump(response.json(), json_file, indent=4)





    

