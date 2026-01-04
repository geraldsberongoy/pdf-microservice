from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Limiter with the client's IP address as the identifier
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://", # In-memory storage is faster and sufficient for Cloud Run
)
