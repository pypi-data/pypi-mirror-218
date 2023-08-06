import sys, os

sys.path.append(os.getcwd() + '/..')

from pbxonline.api import PBXOnlineAPI


api = PBXOnlineAPI(api_id='170703api', api_key='ct2g7gxQAiVtLxFN8vBF')

sip_accounts = api.pbx.get_sip_accounts()

if(sip_accounts.has_error):
    print('Error!')
else:
    for account in sip_accounts.iterator():
        print(f'Account: {account.ID} - {account.logicalName} - {account.sipUsername}')