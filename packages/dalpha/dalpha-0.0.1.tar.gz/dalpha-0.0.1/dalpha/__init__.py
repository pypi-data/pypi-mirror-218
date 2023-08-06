import requests, json, boto3, io, logging

class Agent:
    def __init__(self, api_id, mock, token='c8c5fd1d3c9f37d47ae42'):
        self.base_url = f'https://api.dalpha.so/inferences/{api_id}/evaluate'
        self.api_id = api_id
        self.token = token
        self.mock = mock
        self.s3 = boto3.client('s3')
        
    def poll(self, mock=True):
        if mock:
            return self.mock
        
        url = f"{self.base_url}/poll"

        headers = {
        'token': self.token
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 422:
            return None
        elif response.status_code != 200:
            raise Exception(f'error from poll / response status_code {response.status_code}')
        
        return response.json()

    def validate(self, evaluate_id, output, mock=True):
        if mock:
            logging.debug(output)
            return
        payload = json.dumps({
            "id": evaluate_id,
            "json": output
        })

        url = f"{self.base_url}/validate"

        headers = {
            'token': self.token,
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise Exception(f'error from validate / response status_code {response.status_code}')
        
    def download_from_url(self, url):
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            raise Exception(f"can't donwload from url")
        else:
            return io.BytesIO(r.content)
            # return Image.open(io.BytesIO(r.content)).convert('RGB')

    def download_from_s3(self, bucket, key, donwload_path):
        try:
            self.s3.download_file(bucket, key, donwload_path)
        except:
            logging.error("failed to download from s3")

    def upload_s3(self, upload_path, bucket, key):
        try:
            self.s3.upload_file(upload_path, bucket, key)
        except:
            logging.error("failed to upload s3")
