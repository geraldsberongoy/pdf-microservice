import re

def get_doc_id_from_url(url):
    """Extracts the Google Doc ID for cleaner filenames and DB tracking."""
    # Pattern looks for the long string between /d/ and /
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    return match.group(1) if match else "unknown_doc"
