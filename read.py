from langchain_core.tools import tool
import io  # it is a inp/op buffer to read pdf
import PyPDF2
import requests


@tool
def read_pdf(url: str) -> str:
    """Read and extract text from a PDF file given its URL.

    Args:
        url: The URL of the PDF file to read

    Returns:
        The extracted text content from the PDF
    """
    try:
        response = requests.get(url)  # access pdf via url
        pdf_file = io.BytesIO(response.content)  # convert to bytes
        pdf_reader = PyPDF2.PdfReader(pdf_file)  # retrieve text from pdf
        num_pages = len(pdf_reader.pages)  # length of pages
        # Extract text from all pages
        text = ""
        for i, page in enumerate(pdf_reader.pages, 1):
            print(f"Extracting text from page {i}/{num_pages}")
            text += page.extract_text() + "\n"

        print(
            f"Successfully extracted {len(text)} characters of text from PDF")
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        raise


# url = "https://arxiv.org/pdf/2508.08244v1"
# print(read_pdf(url))
