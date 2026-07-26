#!/bin/bash

# NetMedix v2.0.0 - Deployment Package Builder
# Script ini membuat zip file untuk deployment ke server

set -e

# Colors untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
VERSION="2.0.0"
OUTPUT_FILE="netmedix-v${VERSION}-deploy.zip"
TEMP_DIR="netmedix-deploy"

echo -e "${GREEN}NetMedix v${VERSION} - Deployment Package Builder${NC}"
echo "================================================"

# Clean up previous build
if [ -d "$TEMP_DIR" ]; then
    echo -e "${YELLOW}Membersihkan build sebelumnya...${NC}"
    rm -rf "$TEMP_DIR"
fi

# Create temporary directory
echo -e "${GREEN}Membuat struktur deployment...${NC}"
mkdir -p "$TEMP_DIR/nginx"

# Copy essential files
echo "Copying core files..."
cp app.py requirements.txt "$TEMP_DIR/"

echo "Copying inference engine..."
cp -r inference/ "$TEMP_DIR/"

echo "Copying knowledge base..."
cp -r data/ "$TEMP_DIR/"

echo "Copying templates..."
cp -r templates/ "$TEMP_DIR/"

echo "Copying static assets..."
cp -r static/ "$TEMP_DIR/"

echo "Copying Docker files..."
cp Dockerfile docker-compose.prod.yml .dockerignore .env.example "$TEMP_DIR/"

echo "Copying Nginx configuration..."
cp nginx/nginx.conf "$TEMP_DIR/nginx/"

# Create zip file
echo -e "${GREEN}Membuat deployment zip...${NC}"
zip -r "$OUTPUT_FILE" "$TEMP_DIR/" -q

# Get file size
FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)

# Cleanup
echo -e "${YELLOW}Membersihkan temporary files...${NC}"
rm -rf "$TEMP_DIR"

# Summary
echo ""
echo -e "${GREEN}✓ Deployment package berhasil dibuat!${NC}"
echo ""
echo "File: $OUTPUT_FILE"
echo "Size: $FILE_SIZE"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Upload ke server: scp $OUTPUT_FILE user@yourserver.com:/home/user/"
echo "2. Extract di server: unzip $OUTPUT_FILE"
echo "3. Setup .env dan run: docker compose -f docker-compose.prod.yml up -d --build"
echo ""
echo -e "${GREEN}Happy deploying! 🚀${NC}"
