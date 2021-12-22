# ABX Action to get refresh and bearer tokens as part of ABX Flow: Ultimate Notifications
# Created by Guillermo Martinez and Dennis Gerolymatos 
# Version 1.1 - 22.12.2021

import requests # query the API
import json # API query responses to json.
def handler(context, inputs):
    ## get variables ##
    vraUserName=context.getSecret(inputs["vra_service_account"])            # vRAuserName from inputs
    vraPassword=context.getSecret(inputs["vra_service_account_password"])   # vRApassword from the inputs
    vraUserName=vraUserName.split("@")                                      # Removing the @domain part of username.
    vraUrl=inputs["vra_fqdn"]                                               # vRA url
    #get a refresh token.
    print('Generating Refresh Token...')
    body= {
            "username": vraUserName[0],
            "password": vraPassword
            }
    headers={'Content-Type': 'application/json','accept': 'application/json'}
    response=requests.post('https://' + vraUrl + '/csp/gateway/am/api/login?access_token', headers=headers, data=json.dumps(body), verify=False)
    if response.status_code==200:
        vraRefreshToken=response.json()['refresh_token']
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
    # get a bearer token.
        print('Generating Bearer Token...')    
    body={
     "refreshToken": vraRefreshToken
    }
    response_bearerToken=requests.post('https://' + vraUrl + '/iaas/api/login', data=json.dumps(body), verify=False)
    if response_bearerToken.status_code==200:
        vraBearerToken=response_bearerToken.json()['token']
        bearer="Bearer "
        bearerToken=bearer + vraBearerToken
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response_bearerToken.status_code, response_bearerToken.content))
    outputs={}
    outputs['bearerToken']=bearerToken
    return outputs

