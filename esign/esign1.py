"""
This script handles sending out a template for signing (using a hard coded template ID you should tweak of course)
"""

import requests 
import json 
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

def sendForSigning(template_id, first_name, last_name, email, token):
	url = "https://na1.foxitesign.foxit.com/api/templates/createFolder"
	body = {
		"folderName":"Sending for Signing",
		"templateIds":[template_id],
		"parties":[
		{
			"permission":"FILL_FIELDS_AND_SIGN",
			"firstName":first_name,
			"lastName":last_name,
			"emailId":email,
			"sequence":1
		}
		],
		"senderEmail":"raymond_camden@foxitsoftware.com"
	}

	headers = {
		'Authorization': f'Bearer {token}',
	}

	response = requests.request("POST", url, headers=headers, json=body)
	return response.json()

access_token = getAccessToken(CLIENT_ID, CLIENT_SECRET)

# Hard coded template id
tid = "392230"

sendForSigningResponse = sendForSigning(tid, "Raymond", "Camden", "raymondcamden@gmail.com", access_token)
# don't need the entire result, but you can uncomment this to see
# print(json.dumps(sendForSigningResponse, indent=4))

envelopeId = sendForSigningResponse['folder']['folderId']
print(f"ID of the envelope created: {envelopeId}")
