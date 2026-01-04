# 1. Use python-slim for better compatibility with C-extensions (like grpcio in firebase-admin)
FROM python:3.11-slim

# 2. Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Ensures python output is sent straight to terminal (logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory in the container
WORKDIR /app

# 4. Copy the dependencies file
COPY requirements.txt .

# 5. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code
COPY . .

# 7. Expose the port (Cloud Run sets this env var automatically, but good for local)
ENV PORT=8080
EXPOSE 8080

# 8. Run using Gunicorn (Production WSGI Server)
# Logic: "run:app" means file "run.py", object "app"
CMD echo "Starting Gunicorn on port $PORT..." && exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 run:app