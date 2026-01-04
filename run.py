from dotenv import load_dotenv
from src.app import create_app

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
