import os
import requests 
import sys 
from time import sleep 
import zipfile 
import io

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
HOST = os.environ.get('HOST')

NUM_PAGES_FOR_PREVIEW = 5
SOURCE_PDF = "a-midsummer-nights-dream.pdf"

def uploadDoc(path, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	with open(path, 'rb') as f:
		files = {'file': f}

		request = requests.post(f"{HOST}/pdf-services/api/documents/upload", files=files, headers=headers)
		return request.json()


def splitPDF(doc, count, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	}

	body = {
		"documentId":doc,
		"pageCount":count
	}

	request = requests.post(f"{HOST}/pdf-services/api/documents/modify/pdf-split", json=body, headers=headers)
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

	return requests.get(f"{HOST}/pdf-services/api/documents/{doc}/download", headers=headers).content


doc = uploadDoc(f"../../inputfiles/{SOURCE_PDF}", CLIENT_ID, CLIENT_SECRET)
print(f"Uploaded pdf to Foxit")

task = splitPDF(doc["documentId"], NUM_PAGES_FOR_PREVIEW, CLIENT_ID, CLIENT_SECRET)
print(f"Started split operation")

result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
print(f"Done with split")

bits = getResult(result["resultDocumentId"],  CLIENT_ID, CLIENT_SECRET)
zf = zipfile.ZipFile(io.BytesIO(bits), "r")

firstEntry = zf.infolist()[0]

with zf.open(firstEntry) as pdf:
	with open(f"preview/{SOURCE_PDF}", "wb") as output:
		output.write(pdf.read())

print("Done")
		
