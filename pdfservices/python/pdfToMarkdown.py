# Requires pip install html-to-markdown, https://pypi.org/project/html-to-markdown/
from html_to_markdown import convert_to_markdown

import os
import requests
import sys 
from time import sleep 

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
HOST = os.environ.get('HOST')

def uploadDoc(path, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	with open(path, 'rb') as f:
		files = {'file': f}

		request = requests.post(f"{HOST}/pdf-services/api/documents/upload", files=files, headers=headers)
		return request.json()


def pdfToHTML(doc, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	}

	body = {
		"documentId":doc	
	}

	request = requests.post(f"{HOST}/pdf-services/api/documents/convert/pdf-to-html", json=body, headers=headers)
	return request.json()

def checkTask(task, id, secret):

	headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	}

	done = False
	while done is False:

		request = requests.get(f"{HOST}/pdf-services/api/tasks/{task}", headers=headers)
		status = request.json()
		if status["status"] == "COMPLETED":
			done = True
			# really only need resultDocumentId, will address later
			return status
		elif status["status"] == "FAILED":
			print("Failure. Here is the last status:")
			print(status)
			sys.exit()
		else:
			print(f"Current status, {status['status']}, percentage: {status['progress']}")
			sleep(5)


def getResult(doc, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	return requests.get(f"{HOST}/pdf-services/api/documents/{doc}/download", headers=headers).text

doc = uploadDoc("../../inputfiles/a-midsummer-nights-dream.pdf", CLIENT_ID, CLIENT_SECRET)
print(f"Uploaded doc to Foxit, id is {doc['documentId']}")

task = pdfToHTML(doc["documentId"], CLIENT_ID, CLIENT_SECRET)
print(f"Created task, id is {task['taskId']}")
result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
html = getResult(result["resultDocumentId"], CLIENT_ID, CLIENT_SECRET)
print("Done, converting HTML now...")
md = convert_to_markdown(html)

with open("../../output/output.md", "w") as f:
	f.write(md)

print("Done and saved to: ../../output/output.md")


#downloadResult(result["resultDocumentId"], "../../output/output.html", CLIENT_ID, CLIENT_SECRET)
#print("Done and saved to: ../../output/output.html")