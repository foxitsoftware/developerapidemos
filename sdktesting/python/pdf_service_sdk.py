import requests
from time import sleep

class PDFServiceSDK:

    def __init__(self, client_id, client_secret, host="https://na1.fusion.foxit.com"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.host = host

    def _headers(self, content_type=None):
        headers = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _upload_doc(self, path):
        with open(path, 'rb') as f:
            files = {'file': f}
            r = requests.post(f"{self.host}/pdf-services/api/documents/upload", files=files, headers=self._headers())
            r.raise_for_status()
            return r.json()["documentId"]

    def _check_task(self, task_id):
        while True:
            r = requests.get(f"{self.host}/pdf-services/api/tasks/{task_id}", headers=self._headers("application/json"))
            r.raise_for_status()
            status = r.json()
            if status["status"] == "COMPLETED":
                return status["resultDocumentId"]
            elif status["status"] == "FAILED":
                raise Exception(f"Task failed: {status}")
            sleep(5)

    def _download_result(self, doc_id, output_path):
        r = requests.get(f"{self.host}/pdf-services/api/documents/{doc_id}/download", stream=True, headers=self._headers())
        r.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(r.content)

    def excel_to_pdf(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-excel", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def extract_pdf(self, input_path, output_path, extract_type, page_range=None):
        """
        Extracts content from a PDF using the Extract API.
        extract_type: 'TEXT', 'IMAGE', or 'PAGE'
        page_range: optional, int or list of ints (pages to extract)
        """
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id, "extractType": extract_type}
        if page_range is not None:
            body["pageRange"] = page_range
        r = requests.post(f"{self.host}/pdf-services/api/documents/modify/pdf-extract", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def html_to_pdf(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-html", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def image_to_pdf(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-image", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def pdf_to_excel(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-excel", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def pdf_to_html(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-html", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def pdf_to_image(self, input_path, output_path, page_range=None):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        if page_range is not None:
            body["pageRange"] = page_range
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-image", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def pdf_to_powerpoint(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-ppt", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def pdf_to_text(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-text", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def pdf_to_word(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-word", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def powerpoint_to_pdf(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-ppt", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def text_to_pdf(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-text", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def url_to_pdf(self, url, output_path):
        body = {"url": url}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-url", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)

    def word_to_pdf(self, input_path, output_path):
        doc_id = self._upload_doc(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-word", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self._download_result(result_doc_id, output_path)
