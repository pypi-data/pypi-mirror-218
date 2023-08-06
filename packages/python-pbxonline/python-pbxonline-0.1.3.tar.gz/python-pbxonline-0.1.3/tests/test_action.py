import sys, os

sys.path.append(os.getcwd() + '/..')

from pbxonline.api import PBXOnlineAPI


api = PBXOnlineAPI(api_id='170703api', api_key='ct2g7gxQAiVtLxFN8vBF')

# start_conversation = api.action.start_call(
#     2502,
#     '+32469234966'
# )

# print('Conversation started - ID: ' + str(start_conversation.ID))

api.action.end_call('3866342')