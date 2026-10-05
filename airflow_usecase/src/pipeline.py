from datetime import datetime
import uuid

from src.extract import extract_data
from src.validate import validate_data
from src.transform import transform_data
from src.load import (
    get_watermark,
    filter_incremental,
    load_data,
    update_watermark
)
from src.audit import write_audit


PIPELINE_NAME = "customer_incremental_pipeline"


def run_pipeline():

    run_id = str(uuid.uuid4())

    start_time = datetime.now()

    try:

        # Extract
        df = extract_data(
            "data/raw/customers.csv"
        )

        records_read = len(df)

        # Validate
        validate_data(df)

        # Transform
        df = transform_data(df)

        # Get watermark
        watermark = get_watermark(
            PIPELINE_NAME
        )

        # Incremental filtering
        df = filter_incremental(
            df,
            watermark
        )

        # Load
        records_loaded = load_data(df)

        # Update watermark only after successful load
        if not df.empty:

            new_watermark = df["updated_at"].max()

            update_watermark(
                PIPELINE_NAME,
                new_watermark
            )

        # Audit success
        write_audit(
            PIPELINE_NAME,
            run_id,
            start_time,
            "SUCCESS",
            records_read,
            records_loaded
        )

        print("Pipeline completed successfully")

    except Exception as e:

        write_audit(
            PIPELINE_NAME,
            run_id,
            start_time,
            "FAILED",
            error_message=str(e)
        )

        print(f"Pipeline failed: {e}")

        raise