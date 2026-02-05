"""
Resume Parser Module
Extracts text content from PDF and DOCX resume files
"""

import PyPDF2
from docx import Document
from typing import Optional


class ResumeParser:
    """Parse resume files and extract text content"""

    @staticmethod
    def parse_pdf(file_path: str) -> Optional[str]:
        """
        Extract text from PDF file

        Args:
            file_path: Path to PDF file

        Returns:
            Extracted text content or None if error
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"

                return text.strip()
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return None

    @staticmethod
    def parse_docx(file_path: str) -> Optional[str]:
        """
        Extract text from DOCX file

        Args:
            file_path: Path to DOCX file

        Returns:
            Extracted text content or None if error
        """
        try:
            doc = Document(file_path)
            text = ""

            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

            return text.strip()
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return None

    @staticmethod
    def parse_resume(file_path: str, file_type: str) -> Optional[str]:
        """
        Parse resume based on file type

        Args:
            file_path: Path to resume file
            file_type: Type of file ('pdf' or 'docx')

        Returns:
            Extracted text content or None if error
        """
        if file_type.lower() == 'pdf':
            return ResumeParser.parse_pdf(file_path)
        elif file_type.lower() in ['docx', 'doc']:
            return ResumeParser.parse_docx(file_path)
        else:
            print(f"Unsupported file type: {file_type}")
            return None
