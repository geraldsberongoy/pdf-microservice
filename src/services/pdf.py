import re
import requests

def fetch_google_doc_pdf(doc_url):
    """
    Fetches the PDF export stream from a Google Doc URL.
    Returns the requests.Response object if successful (status 200),
    otherwise returns the response object (checking needs to be done by caller) or raises error.
    """
    # Clean the URL to get the base part
    # We strip anything after /edit, /view, or /preview
    base_url = re.split(r'/(edit|view|preview)', doc_url)[0]
    export_url = f"{base_url}/export?format=pdf"

    print(f"Fetching PDF from: {export_url}")

    # Fetch the PDF from Google
    # stream=True is efficient for large files
    response = requests.get(export_url, stream=True)
    return response
