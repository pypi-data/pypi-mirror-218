import sys, os

sys.path.append(os.getcwd() + '/..')

from pbxonline.api import PBXOnlineAPI


api = PBXOnlineAPI(api_id='170703api', api_key='ct2g7gxQAiVtLxFN8vBF')

# conversation = api.action.start_call(2502, '+32469234966')

# conversations = api.action.get_ongoing_calls()

# for conversation in conversations.iterator():
#     print(vars(conversation))
#     print(f'Conversation: {conversation.ID} - {conversation.origin} - {conversation.destination}')

did_numbers = api.pbx.get_did_numbers()

for number in did_numbers.iterator():
    print(f'DID: {number.did} - {number.logicalName}')