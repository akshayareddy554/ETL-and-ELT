CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    city VARCHAR(100),
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_watermark (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    last_watermark TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_log (
    audit_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100),
    run_id VARCHAR(100),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(30),
    records_read INTEGER,
    records_inserted INTEGER,
    records_updated INTEGER,
    error_message TEXT
);