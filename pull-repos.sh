#!/bin/bash

# Simple script to pull the auth and frontend repositories
# Usage: ./pull-repos.sh

set -e

# Repository URLs
AUTH_REPO="https://github.com/dearborn-coding-club/website-base-auth"
FRONTEND_REPO="https://github.com/dearborn-coding-club/website-base-frontend"

echo "🔄 Pulling Dearborn Coding Club repositories..."

# Clone auth repository
if [ -d "website-base-auth" ]; then
    echo "📝 Updating auth repository..."
    cd website-base-auth
    git pull
    cd ..
else
    echo "📝 Cloning auth repository..."
    git clone $AUTH_REPO
fi

# Clone frontend repository  
if [ -d "website-base-frontend" ]; then
    echo "🎨 Updating frontend repository..."
    cd website-base-frontend
    git pull
    cd ..
else
    echo "🎨 Cloning frontend repository..."
    git clone $FRONTEND_REPO
fi

echo "✅ All repositories updated!"
echo ""
echo "Repository structure:"
echo "├── website-base-backend/ (current - Django API)"
echo "├── website-base-auth/ (authentication service)"
echo "└── website-base-frontend/ (frontend application)"
echo ""
echo "Run './setup.sh' for full development environment setup."
