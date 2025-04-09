from databases import Database

from app.config import settings

# Create database instance
database = Database(settings.DATABASE_URL)
