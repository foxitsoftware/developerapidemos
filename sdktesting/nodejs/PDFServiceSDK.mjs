// PDFServiceSDK.mjs
// Node.js ESM version of the PDFServiceSDK
// Requires Node.js 18+ (for global fetch and native async/await)

import { readFile, writeFile } from 'fs/promises';

export class PDFServiceSDK {
    constructor(clientId, clientSecret, host="https://na1.fusion.foxit.com") {
        this.clientId = clientId;
        this.clientSecret = clientSecret;
        this.host = host;
    }

    _headers(contentType) {
        const headers = {
            'client_id': this.clientId,
            'client_secret': this.clientSecret
        };
        if (contentType) headers['Content-Type'] = contentType;
        return headers;
    }

    async _uploadDoc(path) {
        const fileData = await readFile(path);
        const formData = new FormData();
        formData.append('file', new Blob([fileData]), path.split('/').pop());
        const res = await fetch(`${this.host}/pdf-services/api/documents/upload`, {
            method: 'POST',
            headers: this._headers(),
            body: formData
        });
        if (!res.ok) throw new Error(await res.text());
        const json = await res.json();
        return json.documentId;
    }

    async _checkTask(taskId) {
        while (true) {
            const res = await fetch(`${this.host}/pdf-services/api/tasks/${taskId}`, {
                headers: this._headers('application/json')
            });
            if (!res.ok) throw new Error(await res.text());
            const status = await res.json();
            if (status.status === 'COMPLETED') return status.resultDocumentId;
            if (status.status === 'FAILED') throw new Error(`Task failed: ${JSON.stringify(status)}`);
            await new Promise(r => setTimeout(r, 5000));
        }
    }

    async _downloadResult(docId, outputPath) {
        const res = await fetch(`${this.host}/pdf-services/api/documents/${docId}/download`, {
            headers: this._headers()
        });
        if (!res.ok) throw new Error(await res.text());
        const buffer = Buffer.from(await res.arrayBuffer());
        await writeFile(outputPath, buffer);
    }

    async excelToPDF(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/create/pdf-from-excel`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async extractPDF(inputPath, outputPath, extractType, pageRange) {
        const docId = await this._uploadDoc(inputPath);
        const body = { documentId: docId, extractType };
        if (pageRange !== undefined) body.pageRange = pageRange;
        const res = await fetch(`${this.host}/pdf-services/api/documents/modify/pdf-extract`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async htmlToPDF(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/create/pdf-from-html`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async imageToPDF(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/create/pdf-from-image`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async pdfToExcel(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/convert/pdf-to-excel`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async pdfToHTML(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/convert/pdf-to-html`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async pdfToImage(inputPath, outputPath, pageRange) {
        const docId = await this._uploadDoc(inputPath);
        const body = { documentId: docId };
        if (pageRange !== undefined) body.pageRange = pageRange;
        const res = await fetch(`${this.host}/pdf-services/api/documents/convert/pdf-to-image`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async pdfToPowerPoint(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/convert/pdf-to-ppt`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async pdfToText(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/convert/pdf-to-text`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async pdfToWord(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/convert/pdf-to-word`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async powerpointToPDF(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/create/pdf-from-ppt`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async textToPDF(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/create/pdf-from-text`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId, stuff: true })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async urlToPDF(url, outputPath) {
        const res = await fetch(`${this.host}/pdf-services/api/documents/create/pdf-from-url`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ url })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    async wordToPDF(inputPath, outputPath) {
        const docId = await this._uploadDoc(inputPath);
        const res = await fetch(`${this.host}/pdf-services/api/documents/create/pdf-from-word`, {
            method: 'POST',
            headers: this._headers('application/json'),
            body: JSON.stringify({ documentId: docId })
        });
        if (!res.ok) throw new Error(await res.text());
        const { taskId } = await res.json();
        const resultDocId = await this._checkTask(taskId);
        await this._downloadResult(resultDocId, outputPath);
    }

    /**
     * Converts between supported formats using input and output file extensions.
     * @param {string} inputPath - Path to the input file.
     * @param {string} outputPath - Path to the output file.
     */
    async conversion(inputPath, outputPath) {
        const getExt = path => path.split('.').pop().toLowerCase();
        const inputExt = getExt(inputPath);
        const outputExt = getExt(outputPath);

        // To PDF
        if (outputExt === 'pdf') {
            if (["doc", "docx"].includes(inputExt)) {
                return this.wordToPDF(inputPath, outputPath);
            } else if (["xls", "xlsx"].includes(inputExt)) {
                return this.excelToPDF(inputPath, outputPath);
            } else if (["ppt", "pptx"].includes(inputExt)) {
                return this.powerpointToPDF(inputPath, outputPath);
            } else if (["html", "htm"].includes(inputExt)) {
                return this.htmlToPDF(inputPath, outputPath);
            } else if (["txt"].includes(inputExt)) {
                return this.textToPDF(inputPath, outputPath);
            } else if (["png", "jpg", "jpeg", "bmp", "gif"].includes(inputExt)) {
                return this.imageToPDF(inputPath, outputPath);
            } else {
                throw new Error(`Conversion from .${inputExt} to .pdf is not supported.`);
            }
        }
        // From PDF
        else if (inputExt === 'pdf') {
            if (["doc", "docx"].includes(outputExt)) {
                return this.pdfToWord(inputPath, outputPath);
            } else if (["xls", "xlsx"].includes(outputExt)) {
                return this.pdfToExcel(inputPath, outputPath);
            } else if (["ppt", "pptx"].includes(outputExt)) {
                return this.pdfToPowerPoint(inputPath, outputPath);
            } else if (["html", "htm"].includes(outputExt)) {
                return this.pdfToHTML(inputPath, outputPath);
            } else if (["txt"].includes(outputExt)) {
                return this.pdfToText(inputPath, outputPath);
            } else if (["png", "jpg", "jpeg", "bmp", "gif"].includes(outputExt)) {
                return this.pdfToImage(inputPath, outputPath);
            } else {
                throw new Error(`Conversion from .pdf to .${outputExt} is not supported.`);
            }
        } else {
            throw new Error(`Conversion from .pdf to .${outputExt} is not supported.`);
        }
    }
}
