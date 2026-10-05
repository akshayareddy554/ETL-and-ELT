from datetime import datetime
from src.load import get_connection


def write_audit(
    pipeline_name,
    run_id,
    start_time,
    status,
    records_read=0,
    records_inserted=0,
    records_updated=0,
    error_message=None
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO audit_log
        (
            pipeline_name,
            run_id,
            start_time,
            end_time,
            status,
            records_read,
            records_inserted,
            records_updated,
            error_message
        )
        VALUES
        (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        """,
        (
            pipeline_name,
            run_id,
            start_time,
            datetime.now(),
            status,
            records_read,
            records_inserted,
            records_updated,
            error_message
        )
    )

    conn.commit()

    cursor.close()
    conn.close()