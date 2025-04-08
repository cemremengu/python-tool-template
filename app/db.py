from databases import Database

from app.config import settings

# Create database instance
database = Database(settings.DATABASE_URL)


# SQL Queries - with database-specific variations
class Queries:
    # Oracle specific queries
    ORACLE = {
        "SELECT_ITEMS": "SELECT * FROM {schema}.ITEMS ORDER BY ID OFFSET :skip ROWS FETCH NEXT :limit ROWS ONLY",
        "SELECT_ITEMS_SEARCH": "SELECT * FROM {schema}.ITEMS WHERE UPPER(NAME) LIKE UPPER(:search) ORDER BY ID OFFSET :skip ROWS FETCH NEXT :limit ROWS ONLY",
        "SELECT_ITEM_BY_ID": "SELECT * FROM {schema}.ITEMS WHERE ID = :id",
        "INSERT_ITEM": "INSERT INTO {schema}.ITEMS (NAME, DESCRIPTION, PRICE, IS_ACTIVE) VALUES (:name, :description, :price, :is_active) RETURNING ID INTO :id",
        "UPDATE_ITEM": "UPDATE {schema}.ITEMS SET NAME = :name, DESCRIPTION = :description, PRICE = :price, IS_ACTIVE = :is_active WHERE ID = :id",
        "DELETE_ITEM": "DELETE FROM {schema}.ITEMS WHERE ID = :id",
    }

    # PostgreSQL specific queries
    POSTGRESQL = {
        "SELECT_ITEMS": "SELECT * FROM {schema}.items ORDER BY id OFFSET :skip LIMIT :limit",
        "SELECT_ITEMS_SEARCH": "SELECT * FROM {schema}.items WHERE name ILIKE :search ORDER BY id OFFSET :skip LIMIT :limit",
        "SELECT_ITEM_BY_ID": "SELECT * FROM {schema}.items WHERE id = :id",
        "INSERT_ITEM": "INSERT INTO {schema}.items (name, description, price, is_active) VALUES (:name, :description, :price, :is_active) RETURNING id",
        "UPDATE_ITEM": "UPDATE {schema}.items SET name = :name, description = :description, price = :price, is_active = :is_active WHERE id = :id",
        "DELETE_ITEM": "DELETE FROM {schema}.items WHERE id = :id",
    }


# Select the appropriate query set based on the database type
def get_queries():
    if settings.DB_TYPE == "postgresql":
        return Queries.POSTGRESQL
    else:
        return Queries.ORACLE


# Initialize query with schema and return formatted query
def get_query(query_name):
    queries = get_queries()
    query_template = queries.get(query_name)
    return query_template.format(schema=settings.DB_SCHEMA)
