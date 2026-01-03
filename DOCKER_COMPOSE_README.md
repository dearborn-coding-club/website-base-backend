# Docker Compose Setup

This project has been converted from a single Dockerfile to Docker Compose for easier development and production deployment.

## Files Created

- `docker-compose.yml` - Development environment with hot reloading
- `docker-compose.prod.yml` - Production environment with optimizations
- `.env.example` - Template for environment variables

## Quick Start

1. **Copy the environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Update the `.env` file with your values:**
   - Set a secure `DJANGO_SECRET_KEY`
   - Set your `OPENAI_API_KEY` if using OpenAI features
   - Update database passwords for production use

3. **Start the development environment:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Web application: http://localhost:8000
   - PostgreSQL database: localhost:5432

## Development vs Production

### Development (`docker-compose.yml`)
- Uses volume mounting for hot reloading
- Exposes PostgreSQL port for direct database access
- Includes default development values
- Automatically runs migrations on startup

### Production (`docker-compose.prod.yml`)
- Runs migrations and collects static files on startup
- Includes health checks
- Uses restart policies
- Requires proper environment variables

To run production setup:
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## Database Management

The PostgreSQL database data is persisted in a Docker volume named `postgres_data`.

### Accessing the Database
```bash
# Connect to the database container
docker-compose exec db psql -U postgres -d website_backend_db

# Or from your host machine (when port is exposed)
psql -h localhost -U postgres -d website_backend_db
```

### Backup and Restore
```bash
# Backup
docker-compose exec db pg_dump -U postgres website_backend_db > backup.sql

# Restore
docker-compose exec -T db psql -U postgres -d website_backend_db < backup.sql
```

## Useful Commands

```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: This will delete your database)
docker-compose down -v

# Run Django management commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

## Migration from Original Dockerfile

The original Dockerfile installed PostgreSQL client tools but ran the Django app directly. This Docker Compose setup:

1. **Separates concerns** - Web app and database run in separate containers
2. **Improves development** - Hot reloading with volume mounts
3. **Enhances production** - Proper service orchestration and health checks
4. **Adds flexibility** - Easy to scale, backup, and manage services independently

The original Dockerfile is still used as the build context for the web service, but now the PostgreSQL database runs in its own dedicated container.
