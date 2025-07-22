"""
This checks the envelope status
"""

import requests 
import json 
import sys
import os

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

def getAccessToken(id, secret):
	url = "https://na1.foxitesign.foxit.com/api/oauth2/access_token"
	payload=f"client_id={id}&client_secret={secret}&grant_type=client_credentials&scope=read-write"
	headers = {
	'Content-Type': 'application/x-www-form-urlencoded'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	token = (response.json())["access_token"]
	return token

def getStatus(envelope_id, token):	
	url = f"https://na1.foxitesign.foxit.com/api/folders/myfolder?folderId={envelope_id}"

	headers = {
		'Authorization': f'Bearer {token}',
	}

	response = requests.request("GET", url, headers=headers)
	result = response.json()
	return result

envelope_id = int(sys.argv[1])
access_token = getAccessToken(CLIENT_ID, CLIENT_SECRET)
result = getStatus(envelope_id, access_token)
# don't need the entire result, but you can uncomment this to see
#print(json.dumps(result, indent=4))

print(f"Envelope status: {result['folder']['folderStatus']}")
