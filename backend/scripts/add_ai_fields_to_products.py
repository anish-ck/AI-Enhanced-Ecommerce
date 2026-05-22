from sqlalchemy import text

from app.db.database import engine


def add_columns() -> None:
    statements = [
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS ai_title VARCHAR(200)",
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS ai_description TEXT",
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS ai_category VARCHAR(100)",
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS ai_tags TEXT[]",
        "ALTER TABLE products ADD COLUMN IF NOT EXISTS ai_generated BOOLEAN DEFAULT FALSE",
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'products'
                  AND column_name = 'ai_tags'
                  AND data_type = 'text'
            ) THEN
                ALTER TABLE products
                ALTER COLUMN ai_tags TYPE TEXT[]
                USING string_to_array(ai_tags, ',');
            END IF;
        END $$;
        """,
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'products'
                  AND column_name = 'ai_generated'
            ) THEN
                UPDATE products
                SET ai_generated = FALSE
                WHERE ai_generated IS NULL;
            END IF;
        END $$;
        """,
    ]
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


if __name__ == "__main__":
    add_columns()
    print("AI fields added to products table.")
