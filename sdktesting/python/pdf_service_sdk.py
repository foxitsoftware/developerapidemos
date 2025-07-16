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

    def upload(self, path):
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

    def download(self, doc_id, output_path):
        r = requests.get(f"{self.host}/pdf-services/api/documents/{doc_id}/download", stream=True, headers=self._headers())
        r.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(r.content)

    def compress(self, input_path, output_path, level="LOW"):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id, "compressionLevel":level}
        r = requests.post(f"{self.host}/pdf-services/api/documents/modify/pdf-compress", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def excel_to_pdf(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-excel", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def extract_pdf(self, input_path, output_path, extract_type, page_range=None):
        """
        Extracts content from a PDF using the Extract API.
        extract_type: 'TEXT', 'IMAGE', or 'PAGE'
        page_range: optional, int or list of ints (pages to extract)
        """
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id, "extractType": extract_type}
        if page_range is not None:
            body["pageRange"] = page_range
        r = requests.post(f"{self.host}/pdf-services/api/documents/modify/pdf-extract", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def flatten(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/modify/pdf-flatten", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def html_to_pdf(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-html", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def image_to_pdf(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-image", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def linearize(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/optimize/pdf-linearize", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def pdf_to_excel(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-excel", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def pdf_to_html(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-html", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def pdf_to_image(self, input_path, output_path, page_range=None):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        if page_range is not None:
            body["pageRange"] = page_range
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-image", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def pdf_to_powerpoint(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-ppt", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def pdf_to_text(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-text", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def pdf_to_word(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/convert/pdf-to-word", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def powerpoint_to_pdf(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-ppt", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def text_to_pdf(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-text", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def url_to_pdf(self, url, output_path):
        body = {"url": url}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-url", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def word_to_pdf(self, input_path, output_path):
        doc_id = self.upload(input_path)
        body = {"documentId": doc_id}
        r = requests.post(f"{self.host}/pdf-services/api/documents/create/pdf-from-word", json=body, headers=self._headers("application/json"))
        r.raise_for_status()
        task_id = r.json()["taskId"]
        result_doc_id = self._check_task(task_id)
        self.download(result_doc_id, output_path)

    def conversion(self, input_path, output_path):
        """
        Converts between supported formats using input and output file extensions.
        :param input_path: Path to the input file.
        :param output_path: Path to the output file.
        """
        def get_ext(path):
            return path.split('.')[-1].lower()
        input_ext = get_ext(input_path)
        output_ext = get_ext(output_path)

        # To PDF
        if output_ext == 'pdf':
            if input_ext in ("doc", "docx"):
                return self.word_to_pdf(input_path, output_path)
            elif input_ext in ("xls", "xlsx"):
                return self.excel_to_pdf(input_path, output_path)
            elif input_ext in ("ppt", "pptx"):
                return self.powerpoint_to_pdf(input_path, output_path)
            elif input_ext in ("html", "htm"):
                return self.html_to_pdf(input_path, output_path)
            elif input_ext == "txt":
                return self.text_to_pdf(input_path, output_path)
            elif input_ext in ("png", "jpg", "jpeg", "bmp", "gif"):
                return self.image_to_pdf(input_path, output_path)
            else:
                raise Exception(f"Conversion from .{input_ext} to .pdf is not supported.")
        # From PDF
        elif input_ext == 'pdf':
            if output_ext in ("doc", "docx"):
                return self.pdf_to_word(input_path, output_path)
            elif output_ext in ("xls", "xlsx"):
                return self.pdf_to_excel(input_path, output_path)
            elif output_ext in ("ppt", "pptx"):
                return self.pdf_to_powerpoint(input_path, output_path)
            elif output_ext in ("html", "htm"):
                return self.pdf_to_html(input_path, output_path)
            elif output_ext == "txt":
                return self.pdf_to_text(input_path, output_path)
            elif output_ext in ("png", "jpg", "jpeg", "bmp", "gif"):
                return self.pdf_to_image(input_path, output_path)
            else:
                raise Exception(f"Conversion from .pdf to .{output_ext} is not supported.")
        else:
            raise Exception(f"Conversion from .pdf to .{output_ext} is not supported.")
