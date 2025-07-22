"""
This is an example of sign reminding - use gently!
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

def sendReminder(envelope_id, token):	
	url = "https://na1.foxitesign.foxit.com/api/folders/signaturereminder"
	body = {
		"folderId":envelope_id
	}
	headers = {
		'Authorization': f'Bearer {token}',
	}

	response = requests.request("POST", url, headers=headers, json=body)
	result = response.json()
	return result

envelope_id = int(sys.argv[1])
access_token = getAccessToken(CLIENT_ID, CLIENT_SECRET)
result = sendReminder(envelope_id, access_token)
# don't need the entire result, but you can uncomment this to see
#print(json.dumps(result, indent=4))

print("Reminder sent.")