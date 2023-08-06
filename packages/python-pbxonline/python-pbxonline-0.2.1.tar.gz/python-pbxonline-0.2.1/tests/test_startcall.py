import sys, os

sys.path.append(os.getcwd() + '/..')

from pbxonline.api import PBXOnlineAPI


api = PBXOnlineAPI(api_id='170703api', api_key='ct2g7gxQAiVtLxFN8vBF')

conversation = api.action.start_call(2502, '+32469234966')
print(f'Conversation: {conversation.ID}')

conversations = api.action.get_ongoing_calls()

print('----')
print('Ongoing calls:')
for conversation in conversations.iterator():
    print(f'Conversation: {conversation.ID} - {conversation.origin} - {conversation.destination}')
