from flask import request, jsonify, send_file
from src.utils.helpers import get_doc_id_from_url
from src.services.pdf import fetch_google_doc_pdf
from src.services.analytics import update_counter, get_document_stats

def health_check():
    return jsonify({"status": "ok", "service": "pdf-converter"}), 200

def get_pdf_stats():
    """Returns the download statistics for a given Google Doc URL."""
    doc_url = request.args.get('url')
    if not doc_url:
        return jsonify({"error": "Missing 'url' query parameter"}), 400

    doc_id = get_doc_id_from_url(doc_url)
    stats = get_document_stats(doc_id)

    if stats is None:
        return jsonify({"error": "Analytics service unavailable or database error"}), 503

    return jsonify({
        "doc_id": doc_id,
        "stats": stats
    }), 200

def generate_pdf():
    data = request.json
    doc_url = data.get('url')

    if not doc_url or "docs.google.com" not in doc_url:
        return jsonify({"error": "Invalid URL provided. Must be a Google Doc link."}), 400

    # 1. Extract ID
    doc_id = get_doc_id_from_url(doc_url)
    
    print(f"Processing Request for Doc ID: {doc_id}")

    try:
        # 2. Fetch the PDF from Google
        google_response = fetch_google_doc_pdf(doc_url)

        # Check if Google allowed the download (Permission check)
        if google_response.status_code != 200:
            # Usually means the doc is not set to "Anyone with the link"
            return jsonify({
                "error": "Google refused access. Ensure the doc is shared as 'Anyone with the link can view'.",
                "details": f"Status Code: {google_response.status_code}"
            }), 403

        # 3. Update Firebase Analytics (Fire and forget-ish)
        update_counter(doc_id)

        # 4. Stream the file directly to the client
        # This prevents loading the whole file into RAM
        return send_file(
            google_response.raw,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{doc_id}.pdf"
        )

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
