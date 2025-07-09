"""
Demonstrates making a thumbnail for a PDF - which consists of converting the PDF to an image, taking the first page, 
and shrinking it to a good size.
"""

import os
import io
import requests
import sys 
from time import sleep 
import zipfile 
from PIL import Image


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


def pdfToImage(doc, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	}

	body = {
		"documentId":doc,
		"pageRange":1	
	}

	request = requests.post(f"{HOST}/pdf-services/api/documents/convert/pdf-to-image", json=body, headers=headers)
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


def downloadResult(doc, path, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	with open(path, "wb") as output:
		
		bits = requests.get(f"{HOST}/pdf-services/api/documents/{doc}/download", stream=True, headers=headers).content 
		output.write(bits)

def getResult(doc, id, secret):
	
	headers = {
		"client_id":id,
		"client_secret":secret
	}

	return requests.get(f"{HOST}/pdf-services/api/documents/{doc}/download", headers=headers).content

doc = uploadDoc("../../inputfiles/input.pdf", CLIENT_ID, CLIENT_SECRET)
print(f"Uploaded doc to Foxit, id is {doc['documentId']}")

task = pdfToImage(doc["documentId"], CLIENT_ID, CLIENT_SECRET)
result = checkTask(task["taskId"], CLIENT_ID, CLIENT_SECRET)
print("Done converting PDF to image.")

bits = getResult(result["resultDocumentId"],  CLIENT_ID, CLIENT_SECRET)
zf = zipfile.ZipFile(io.BytesIO(bits), "r")

with zf.open("/1.jpg") as image:
	imageData = image.read()
	with Image.open(io.BytesIO(imageData)) as img:
		img.thumbnail([250,250])
		img.save("../../output/pdfthumbnail.jpg")
		print("../../output/pdfthumbnail.jpg")




