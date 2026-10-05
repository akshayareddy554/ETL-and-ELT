import psycopg2
from psycopg2.extras import execute_values
from src.config import DB_CONFIG


def get_connection():

    return psycopg2.connect(**DB_CONFIG)


def get_watermark(pipeline_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT last_watermark
        FROM pipeline_watermark
        WHERE pipeline_name = %s
        """,
        (pipeline_name,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]

    return None
def filter_incremental(df, watermark):

    if watermark is None:
        return df

    return df[
        df["updated_at"] > watermark
    ]

def load_data(df):

    if df.empty:
        print("No new records to load")
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO customers
        (
            customer_id,
            name,
            email,
            city,
            updated_at
        )
        VALUES %s
        ON CONFLICT (customer_id)
        DO UPDATE SET
            name = EXCLUDED.name,
            email = EXCLUDED.email,
            city = EXCLUDED.city,
            updated_at = EXCLUDED.updated_at
    """

    records = [
        (
            row.customer_id,
            row.name,
            row.email,
            row.city,
            row.updated_at
        )
        for row in df.itertuples()
    ]

    execute_values(cursor, query, records)

    conn.commit()

    cursor.close()
    conn.close()

    print(f"Loaded {len(records)} records")

    return len(records)

def update_watermark(pipeline_name, watermark):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO pipeline_watermark
        (
            pipeline_name,
            last_watermark
        )
        VALUES (%s, %s)

        ON CONFLICT (pipeline_name)
        DO UPDATE SET
            last_watermark = EXCLUDED.last_watermark
        """,
        (
            pipeline_name,
            watermark
        )
    )

    conn.commit()

    cursor.close()
    conn.close()