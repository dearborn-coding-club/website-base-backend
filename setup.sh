#!/bin/bash

# Setup script for Dearborn Coding Club Website Base
# This script pulls in the auth and frontend repositories and sets up the complete development environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Project configuration
BACKEND_DIR="$(pwd)"
AUTH_REPO="https://github.com/dearborn-coding-club/website-base-auth"
FRONTEND_REPO="https://github.com/dearborn-coding-club/website-base-frontend"
AUTH_DIR="website-base-auth"
FRONTEND_DIR="website-base-frontend"

print_status "Starting Dearborn Coding Club Website Base setup..."
print_status "Backend directory: $BACKEND_DIR"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    print_error "This script must be run from the website-base-backend directory"
    print_error "Please cd to the backend directory and run this script again"
    exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is required but not installed. Please install git first."
    exit 1
fi

# Function to clone or update repository
clone_or_update_repo() {
    local repo_url=$1
    local target_dir=$2
    local repo_name=$(basename $repo_url .git)
    
    if [ -d "$target_dir" ]; then
        print_warning "$repo_name already exists. Updating..."
        cd "$target_dir"
        if [ -d ".git" ]; then
            git pull origin main || git pull origin master
            print_success "Updated $repo_name"
        else
            print_warning "$target_dir exists but is not a git repository. Skipping update."
        fi
        cd "$BACKEND_DIR"
    else
        print_status "Cloning $repo_name..."
        git clone "$repo_url" "$target_dir"
        print_success "Cloned $repo_name"
    fi
}

# Clone or update the repositories
print_status "Setting up auth repository..."
clone_or_update_repo "$AUTH_REPO" "$AUTH_DIR"

print_status "Setting up frontend repository..."
clone_or_update_repo "$FRONTEND_REPO" "$FRONTEND_DIR"

# Setup environment files if they don't exist
print_status "Setting up environment configuration..."

if [ ! -f ".env" ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_success "Created .env file. Please update it with your actual values."
else
    print_warning ".env file already exists. Skipping creation."
fi

# Check if Docker and Docker Compose are available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    print_status "Docker and Docker Compose found."
    
    read -p "Do you want to start the development environment with Docker Compose? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Starting Docker Compose development environment..."
        docker-compose up --build -d
        print_success "Development environment started!"
        print_status "Backend API: http://localhost:8000"
        print_status "Database: localhost:5432"
        
        # Wait a moment for services to start
        sleep 3
        
        # Show service status
        print_status "Service status:"
        docker-compose ps
    fi
else
    print_warning "Docker or Docker Compose not found. You can install them to use the containerized development environment."
fi

# Setup frontend if Node.js is available
if [ -d "$FRONTEND_DIR" ]; then
    print_status "Checking frontend setup..."
    cd "$FRONTEND_DIR"
    
    if command -v node &> /dev/null && command -v npm &> /dev/null; then
        print_status "Node.js and npm found. Setting up frontend dependencies..."
        
        if [ -f "package.json" ]; then
            npm install
            print_success "Frontend dependencies installed."
            
            # Check for common frontend scripts
            if npm run --silent 2>/dev/null | grep -q "dev"; then
                print_status "Frontend dev server available. You can run 'npm run dev' in the $FRONTEND_DIR directory."
            elif npm run --silent 2>/dev/null | grep -q "start"; then
                print_status "Frontend server available. You can run 'npm start' in the $FRONTEND_DIR directory."
            fi
        else
            print_warning "No package.json found in frontend directory."
        fi
    else
        print_warning "Node.js and npm not found. You'll need them to run the frontend."
        print_status "Install Node.js from: https://nodejs.org/"
    fi
    
    cd "$BACKEND_DIR"
fi

# Setup auth repository if it has specific setup requirements
if [ -d "$AUTH_DIR" ]; then
    print_status "Checking auth repository setup..."
    cd "$AUTH_DIR"
    
    # Check if it's a Python project
    if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
        print_status "Auth repository appears to be a Python project."
        print_status "You may need to integrate it with the main backend or run it separately."
    fi
    
    # Check if it's a Node.js project  
    if [ -f "package.json" ]; then
        print_status "Auth repository appears to be a Node.js project."
        if command -v npm &> /dev/null; then
            print_status "Installing auth dependencies..."
            npm install
            print_success "Auth dependencies installed."
        fi
    fi
    
    cd "$BACKEND_DIR"
fi

# Setup frontend development Dockerfile if needed
if [ -d "$FRONTEND_DIR" ]; then
    print_status "Configuring frontend for Docker development..."
    
    # Create development Dockerfile if it doesn't exist
    if [ ! -f "$FRONTEND_DIR/Dockerfile.dev" ]; then
        print_status "Creating development Dockerfile for frontend..."
        cp Dockerfile.frontend.dev "$FRONTEND_DIR/Dockerfile.dev"
        print_success "Created Dockerfile.dev in frontend repository"
    fi
    
    # Check if the main Dockerfile exists and suggests the issue
    if [ -f "$FRONTEND_DIR/Dockerfile" ]; then
        if grep -q "COPY ./dist/" "$FRONTEND_DIR/Dockerfile"; then
            print_warning "Frontend Dockerfile expects pre-built dist/ folder."
            print_status "Using Dockerfile.dev for development environment."
        fi
    fi
fi

# Create a development guide
print_status "Creating development guide..."
cat > DEVELOPMENT_SETUP.md << EOF
# Development Setup Guide

This guide was generated by the setup script on $(date).

## Repository Structure

- **Backend (Django)**: Current directory (\`website-base-backend\`)
- **Auth**: \`$AUTH_DIR/\` - Authentication service/module
- **Frontend**: \`$FRONTEND_DIR/\` - Frontend application

## Quick Start

### Using Docker (Recommended)
\`\`\`bash
# Start all services
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
\`\`\`

### Manual Setup

#### Backend (Django)
\`\`\`bash
# Activate virtual environment (if using venv)
source bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
\`\`\`

#### Frontend
\`\`\`bash
cd $FRONTEND_DIR
npm install
npm run dev  # or npm start
\`\`\`

#### Auth Service
\`\`\`bash
cd $AUTH_DIR
# Follow the README in the auth repository for specific setup instructions
\`\`\`

## Services

- **Backend API**: http://localhost:8000
- **Frontend**: Check the frontend README for the port (usually 3000 or 5173)
- **Database**: localhost:5432 (PostgreSQL)

## Environment Configuration

Make sure to update your \`.env\` file with the correct values for:
- DJANGO_SECRET_KEY
- Database credentials
- API keys (OpenAI, etc.)

## Useful Commands

\`\`\`bash
# Django management
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# Docker Compose
docker-compose logs -f web
docker-compose exec web python manage.py shell
docker-compose exec db psql -U postgres -d website_backend_db

# Git workflow
git status
git add .
git commit -m "Your commit message"
git push
\`\`\`

EOF

print_success "Created DEVELOPMENT_SETUP.md with helpful commands and information."

# Summary
print_success "Setup complete!"
print_status "Summary:"
print_status "- Auth repository: $AUTH_DIR/"
print_status "- Frontend repository: $FRONTEND_DIR/"
print_status "- Environment file: .env (update with your values)"
print_status "- Development guide: DEVELOPMENT_SETUP.md"

if command -v docker-compose &> /dev/null; then
    print_status ""
    print_status "Next steps:"
    print_status "1. Update .env with your actual configuration values"
    print_status "2. Run 'docker-compose up --build' to start the development environment"
    print_status "3. Check DEVELOPMENT_SETUP.md for detailed instructions"
else
    print_status ""
    print_status "Next steps:"
    print_status "1. Install Docker and Docker Compose for the best development experience"
    print_status "2. Update .env with your actual configuration values"
    print_status "3. Check DEVELOPMENT_SETUP.md for manual setup instructions"
fi

print_success "Happy coding! 🚀"
