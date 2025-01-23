# Production Deployment Settings

from socket import gethostbyname, gethostname


# Include core app settings
from app.settings import *

# Add env specific settings
RUNTIME_ENVIRONMENT = "prod"
DEBUG = False

# Step 5.1)
# Security Setup
CORS_EXPOSE_HEADERS = ["authorization", "content-type", "content-length"]
CORS_ALLOW_HEADERS = CORS_EXPOSE_HEADERS
CORS_ALLOWED_ORIGINS = [
    'https://www.morriswa.org',
]
ALLOWED_HOSTS = [
    'www.morriswa.org',
    gethostbyname(gethostname())
]
CORS_ALLOW_METHODS = (
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
)
