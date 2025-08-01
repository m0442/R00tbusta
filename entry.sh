#!/bin/bash
set -e

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
  echo "❌ No domain provided"
  exit 1
fi

echo "🌐 Using domain: $DOMAIN"

# Install Python dependencies
echo "📦 Installing requirements..."
pip install -r subdomain/requirements.txt

# Run Python script
echo "🚀 Running Subdomain Enumeration script..."
python subdomain/main.py "$DOMAIN" -o json --save

echo "✅ Done."