import sys, os

sys.path.append(os.getcwd() + '/..')

from pbxonline.api import PBXOnlineAPI


api = PBXOnlineAPI(api_id='170703api', api_key='ct2g7gxQAiVtLxFN8vBF')

call_id = 3901969
call = api.action.end_call(call_id)

print(vars(call))

if call.has_error:
    print('Error!')
    print(call.error.error_message)