#!/bin/bash
# Configuration
APP_DIR="/home/flask/flask_po"
FLAG_FILE="/home/flask/flask_po/data/needs_backup"
TAR_FILE="backup.tar.gz"


# Only run if the flag file exists
if [ -f "$FLAG_FILE" ]; then
    tar -czf "$TAR_FILE" -C "$APP_DIR"/data po_backup.json /var/www/html/static/
    rm "$FLAG_FILE"
fi