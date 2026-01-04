# Google Doc to PDF Microservice

A high-performance Flask microservice designed to convert public Google Docs into PDF files on the fly. It features a modular architecture, robust error handling, and integrated Firebase analytics to track document download statistics.

## Features

- **Instant Conversion**: streams PDF content directly from Google's servers to the client without persistent storage.
- **Analytics Tracking**: Automatically increments download counts in Firebase Firestore for every requested document.
- **Production Ready**: Uses **Gunicorn** with multi-threaded workers for high concurrency.
- **Microservice Architecture**: Clean separation of concerns (Controllers, Services, Routes).
- **Dockerized**: specific optimization (`python-slim`) for minimal footprint and maximum compatibility.
- **CORS Support**: Ready to be consumed by frontend applications (e.g., Next.js, React).

## Tech Stack

- **Framework**: Flask (Python 3.11)
- **Database**: Firebase Firestore (for analytics)
- **Server**: Gunicorn (WSGI)
- **Containerization**: Docker
- **Environment Management**: `python-dotenv`

## Project Structure

```text
/pdf-microservice
├── run.py                 # Application entry point
├── Dockerfile             # Production-ready Docker configuration
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
└── src/
    ├── app.py             # App factory
    ├── config/            # Configuration (Firebase credentials)
    ├── controllers/       # Request handlers
    ├── services/          # Business logic (PDF fetching, Analytics)
    ├── routes/            # API Route definitions
    └── utils/             # Helper functions
```

## Getting Started

### Prerequisites
- Python 3.11+
- A Google Cloud/Firebase Service Account

### Local Development

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd pdf-microservice
    ```

2.  **Create a Virtual Environment**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Create a `.env` file in the root directory (copy `.env.example`) and add your Firebase credentials:
    ```ini
    FIREBASE_PROJECT_ID="your-project-id"
    FIREBASE_CLIENT_EMAIL="your-service-account-email"
    FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n..."
    ```

5.  **Run the Server**
    ```bash
    python run.py
    ```
    The app will start at `http://localhost:8080`.

---

## Docker Setup

Build and run the container locally to simulate the production environment.

1.  **Build the Image**
    ```bash
    docker build -t pdf-service .
    ```

2.  **Run the Container**
    *Note: You must pass your environment variables to the container.*
    ```bash
    docker run -p 8080:8080 --env-file .env pdf-service
    ```

---

## API Reference

### 1. Generate PDF
Converts a Google Doc to PDF.

- **URL**: `/generate-pdf`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "url": "https://docs.google.com/document/d/YOUR_DOC_ID/edit"
  }
  ```
- **Response**: Binary PDF Stream.
- **Error (403)**: If the Google Doc is restricted (must be "Anyone with the link can view").

### 2. Get Download Stats
Retrieve how many times a document has been downloaded.

- **URL**: `/stats`
- **Method**: `GET`
- **Query Params**:
  - `url`: The full Google Doc URL.
- **Example**:
  ```text
  GET /stats?url=https://docs.google.com/document/d/YOUR_DOC_ID
  ```
- **Response**:
  ```json
  {
    "doc_id": "YOUR_DOC_ID",
    "stats": {
      "download_count": 42,
      "last_downloaded": "2026-01-04T09:41:00Z"
    }
  }
  ```

### 3. Health Check
Check if the service is running.

- **URL**: `/health`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": "ok",
    "service": "pdf-converter"
  }
  ```

## Deployment (Cloud Run)

This service is optimized for **Google Cloud Run**.
1.  Deploy using the source code or built image.
2.  Set the environment variables (`FIREBASE_PRIVATE_KEY`, etc.) in the Cloud Run console settings.
3.  **Authentication**: If using a Service Account attached to the Cloud Run instance, the app automatically detects credentials without needing environment variables (via Application Default Credentials).
