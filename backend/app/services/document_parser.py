from io import BytesIO
from pathlib import Path

from docx import Document
from pypdf import PdfReader


class DocumentParser:
    def extract_text(self, file_name: str, content: bytes) -> str:
        extension = Path(file_name).suffix.lower()
        if extension == ".pdf":
            return self._extract_pdf(content)
        if extension == ".docx":
            return self._extract_docx(content)
        if extension in {".txt", ".md"}:
            return content.decode("utf-8", errors="ignore").strip()
        raise ValueError("Unsupported file type. Upload PDF or DOCX.")

    def _extract_pdf(self, content: bytes) -> str:
        reader = PdfReader(BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()

    def _extract_docx(self, content: bytes) -> str:
        document = Document(BytesIO(content))
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
        return "\n".join(paragraphs).strip()
