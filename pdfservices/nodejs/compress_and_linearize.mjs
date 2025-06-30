import fs from 'fs';
import { Readable } from 'stream';
import { finished } from 'stream/promises';
import path from 'node:path';

const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const HOST = process.env.HOST;

async function uploadDoc(filepath, id, secret) {
	let filename = path.basename(filepath);
	let data = new FormData();
	let blob = await fs.openAsBlob(filepath);
	data.append('file', blob, filename);

	let req = await fetch(`${HOST}/pdf-services/api/documents/upload`, {
		method:'POST',
		headers: {
			client_id: id, 
			client_secret: secret
		},
		body: data
	});

	return await req.json();

}

async function compressPDF(doc, id, secret, level="MEDIUM") {

	let headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	};

	let body = {
		"documentId":doc,
		"compressionLevel":level 	
	};

	let resp = await fetch(`${HOST}/pdf-services/api/documents/modify/pdf-compress`, {
		method:"POST",
		headers, 
		body:JSON.stringify(body)
	});

	return await resp.json();

}

async function linearizePDF(doc, id, secret, level="MEDIUM") {

	let headers = {
		"client_id":id,
		"client_secret":secret,
		"Content-Type":"application/json"
	};

	let body = {
		"documentId":doc,
		"compressionLevel":level 	
	};

	let resp = await fetch(`${HOST}/pdf-services/api/documents/optimize/pdf-linearize`, {
		method:"POST",
		headers, 
		body:JSON.stringify(body)
	});

	return await resp.json();

}

async function checkTask(task, id, secret) {

	while(true) {
		let req = await fetch(`${HOST}/pdf-services/api/tasks/${task}`, {
			method:'GET',		
			headers: {
				client_id: id, 
				client_secret: secret,
				'Content-Type':'application/json'
			}
		});

		let result = await req.json();

		if(result['status'] === 'COMPLETED') {
			return result;
		} else if(result['status'] === 'FAILED') {
			console.log('Failure. Here is the last status:');
			console.log(result);
			process.exit(1);
		} else {
			console.log(`Current status, ${result['status']}, percentage: ${result['progress']}`);
			await delay(5);
		}

	}
}

// Lame function to add a delay to my polling calls
async function delay(x) {
	return new Promise(resolve => {
		setTimeout(() => resolve(), x * 1000);
	});
}

async function downloadResult(doc, filePath, id, secret) {
	let headers = {
		"client_id":id,
		"client_secret":secret
	}

	let res = await fetch(`${HOST}/pdf-services/api/documents/${doc}/download`, {
		headers
	});

	const body = Readable.fromWeb(res.body);
	const download_write_stream = fs.createWriteStream(filePath);
	return await finished(body.pipe(download_write_stream));

}

let input = "../../inputfiles/input.pdf";
console.log(`File size of input: ${fs.statSync(input).size}`)

let doc = await uploadDoc(input, CLIENT_ID, CLIENT_SECRET);
console.log(`Uploaded doc to Foxit, id is ${doc['documentId']}`);

let task = await compressPDF(doc.documentId, CLIENT_ID, CLIENT_SECRET, "HIGH");
console.log(`Created task, id is ${task['taskId']}`);

let result = await checkTask(task.taskId, CLIENT_ID, CLIENT_SECRET);
console.log("Done converting to PDF. Now doing linearize.")

task = await linearizePDF(result.resultDocumentId, CLIENT_ID, CLIENT_SECRET, "HIGH");
console.log(`Created task, id is ${task['taskId']}`);

result = await checkTask(task.taskId, CLIENT_ID, CLIENT_SECRET);
console.log("Done with linearize task.");


let output = "../../output/node_really_optimized.pdf";
downloadResult(result["resultDocumentId"], output , CLIENT_ID, CLIENT_SECRET);
console.log(`Done and saved to: ${output}.`)
console.log(`File size of output: ${fs.statSync(output).size}`)
