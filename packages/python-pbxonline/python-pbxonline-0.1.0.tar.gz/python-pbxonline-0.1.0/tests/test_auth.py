import sys, os

sys.path.append(os.getcwd() + '/..')

from pbxonline.api import PBXOnlineAPI


api = PBXOnlineAPI(api_id='170703api', api_key='ct2g7gxQAiVtLxFN8vBF')
cache_handler = api._cache_handler
tokens = api._auth_handler.get_tokens()

print(tokens)