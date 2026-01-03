#!/bin/bash

# Quick fix for Docker Compose frontend build issue
# This script provides multiple solutions for the frontend Docker build problem

set -e

echo "🔧 Frontend Docker Build Fix"
echo "============================"
echo ""

# Check if frontend directory exists
if [ ! -d "website-base-frontend" ]; then
    echo "❌ Frontend repository not found. Run './pull-repos.sh' first."
    exit 1
fi

echo "Problem: Frontend Dockerfile expects ./dist/ folder that doesn't exist"
echo "This happens because the production Dockerfile expects pre-built assets."
echo ""
echo "Choose a solution:"
echo ""
echo "1. 🛠️  Create development Dockerfile (Recommended for development)"
echo "2. 🏗️  Build frontend assets first (For production-like setup)"
echo "3. 📝 Use alternative Docker Compose configuration"
echo "4. ℹ️  Show manual fix instructions"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "Creating development Dockerfile..."
        
        # Create Dockerfile.dev in frontend directory
        cat > website-base-frontend/Dockerfile.dev << 'EOF'
FROM node:18-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose development server port
EXPOSE 3000

# Start development server (adjust command based on your package.json)
CMD ["npm", "run", "dev"]
EOF

        echo "✅ Created website-base-frontend/Dockerfile.dev"
        echo ""
        echo "Now update your docker-compose.yml frontend service:"
        echo "  frontend:"
        echo "    build:"
        echo "      context: ./website-base-frontend"
        echo "      dockerfile: Dockerfile.dev"
        echo "    # ... rest of your config"
        echo ""
        echo "Or use: docker-compose -f docker-compose.full.yml up --build"
        ;;
        
    2)
        echo "Building frontend assets..."
        
        cd website-base-frontend
        
        # Check if package.json exists
        if [ ! -f "package.json" ]; then
            echo "❌ No package.json found in frontend directory"
            exit 1
        fi
        
        # Install dependencies and build
        echo "📦 Installing dependencies..."
        npm install
        
        echo "🏗️ Building frontend..."
        npm run build
        
        if [ -d "dist" ]; then
            echo "✅ Frontend built successfully! dist/ directory created."
            echo "You can now run: docker-compose up --build"
        else
            echo "❌ Build completed but no dist/ directory found."
            echo "Check your build script in package.json"
        fi
        
        cd ..
        ;;
        
    3)
        echo "Using production Docker Compose configuration..."
        echo "This setup builds the frontend as part of the Docker process."
        echo ""
        echo "Run: docker-compose -f docker-compose.production.yml up --build"
        echo ""
        echo "This configuration:"
        echo "- Builds frontend assets in a separate container"
        echo "- Serves static files with gostatic"
        echo "- Works with the existing Dockerfile"
        ;;
        
    4)
        echo "Manual Fix Instructions:"
        echo "======================="
        echo ""
        echo "Option A: Modify docker-compose.yml"
        echo "1. Change the frontend service build configuration:"
        echo "   build:"
        echo "     context: ./website-base-frontend"
        echo "     dockerfile: Dockerfile.dev"
        echo "   command: npm run dev"
        echo ""
        echo "Option B: Pre-build frontend"
        echo "1. cd website-base-frontend"
        echo "2. npm install"
        echo "3. npm run build"
        echo "4. cd .. && docker-compose up --build"
        echo ""
        echo "Option C: Use multi-stage build"
        echo "1. Modify the frontend Dockerfile to include build stage:"
        echo "   FROM node:18-alpine as builder"
        echo "   WORKDIR /app"
        echo "   COPY package*.json ./"
        echo "   RUN npm install"
        echo "   COPY . ."
        echo "   RUN npm run build"
        echo ""
        echo "   FROM pierrezemb/gostatic"
        echo "   COPY --from=builder /app/dist/ /srv/http/"
        echo "   CMD [\"-fallback\", \"index.html\"]"
        ;;
        
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Fix applied! Try running Docker Compose now."
