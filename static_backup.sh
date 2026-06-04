#!/bin/bash
# Configuration
APP_DIR="/home/flask/flask_po"
FLAG_FILE="/home/flask/flask_po/data/needs_backup"
TAR_FILE="backup.tar.gz"
DATE=`date "+%Y-%m-%d %H:%M:%S"`


# Only run if the flag file exists
if [ -f "$FLAG_FILE" ]; then
    if tar -czf "$TAR_FILE" -C "$APP_DIR"/data po_backup.json /var/www/html/static/; then
        printf "%s Backup successful\n" "$DATE" >> "$APP_DIR"/logs/backup.log
        rm "$FLAG_FILE"
    else
        printf "%s Backup failed\n" "$DATE" >> "$APP_DIR"/logs/backup.log
    fi
fi