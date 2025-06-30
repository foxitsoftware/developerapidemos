import fs from 'fs';

const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const HOST = process.env.HOST;

async function docGen(doc, data, id, secret) {

	let headers = {
		"client_id":id, 
		"client_secret":secret, 
		"Content-Type":"application/json"
	};

	let body = {
		"outputFormat":"pdf",
		"documentValues": data,  
		"base64FileString":doc
	};

	let req = await fetch(`${HOST}/document-generation/api/GenerateDocumentBase64`, {
		method:'POST', 
		headers, 
		body: JSON.stringify(body)
	});

	return await req.json();
}

let buffer = fs.readFileSync('../../inputfiles/docgen_sample.docx');
let b64 = buffer.toString('base64');

let data = {
	"name":"Raymond Camden", 
	"food": "sushi",
	"favoriteMovie": "Star Wars",
	"cats": [
		{"name":"Elise", "gender":"female", "age":14 },
		{"name":"Luna", "gender":"female", "age":13 },
		{"name":"Crackers", "gender":"male", "age":13 },
		{"name":"Gracie", "gender":"female", "age":12 },
		{"name":"Pig", "gender":"female", "age":10 },
		{"name":"Zelda", "gender":"female", "age":2 },
		{"name":"Wednesday", "gender":"female", "age":1 },
	],
}

let result = await docGen(b64, data, CLIENT_ID, CLIENT_SECRET);

let binaryData = Buffer.from(result.base64FileString, 'base64');
fs.writeFileSync('../../output/node_docgen_sample.pdf', binaryData);
console.log('Done and stored to ../../output/node_docgen_sample.pdf');
