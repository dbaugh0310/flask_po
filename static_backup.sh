#!/bin/bash
# Configuration
APP_DIR="/home/flask/flask_po"
FLAG_FILE="$APP_DIR/data/needs_backup"
TAR_FILE="/var/www/html/static/static.tar.gz"

# Only run if the flag file exists
if [ -f "$FLAG_FILE" ]; then
    tar -czf "$TAR_FILE" -C "$APP_DIR" data/po_backup.json static/images/
    rm "$FLAG_FILE"
fi