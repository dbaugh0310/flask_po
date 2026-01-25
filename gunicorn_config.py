workers = 3  # Number of worker processes
bind = "localhost:8000"  # Bind Gunicorn to localhost on port 8000
forwarded_allow_ips = "*"  # Allow requests from Nginx
proxy_protocol = True  # Enable proxy support

# Logging Settings
accesslog = "logs/gunicorn_access.log"  # Log HTTP requests to a file
errorlog = "logs/gunicorn_error.log"  # Log errors to a file
loglevel = "info"  # Set log verbosity (debug, info, warning, error, critical)

import os
from dotenv import load_dotenv

for env_file in ('.env', '.flaskenv'):
    env = os.path.join(os.getcwd(), env_file)
    if os.path.exists(env):
        load_dotenv(env)