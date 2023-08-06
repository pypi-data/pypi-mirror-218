# import base64
# from typing import Optional


# class Api:
#     def __init__(self, public_key: str, secret_key: str, base_url: Optional[str]):
        
#         self.base_url = base_url if base_url is not None else 'https://cloud.langfuse.com'

#         auth = base64.b64encode(f"{public_key}:{'secret_key'}".encode()).decode()
#         headers = {
#             'Authorization': 'Basic ' + auth,
#             'X-Langfuse-Sdk-Name': 'langfuse-js',
#             'X-Langfuse-Sdk-Version': 'version',
#             'X-Langfuse-Sdk-Variant': 'Server',
#         }
#         self.client = self.create_client(self.base_url, headers)



# class Langfuse:

#     promises = []

#     def __init__(self, public_key: str, secret_key: str, base_url: Optional[str]):
#         self.api = Api(public_key, secret_key, base_url)


#     def trace(body: )