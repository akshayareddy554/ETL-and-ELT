def validate_data(df):

    required_columns = [
        "customer_id",
        "name",
        "email",
        "city",
        "updated_at"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    if df["customer_id"].isnull().any():
        raise ValueError("customer_id contains NULL values")

    if df["email"].isnull().any():
        raise ValueError("email contains NULL values")

    if df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer_id found")

    print("Data validation successful")

    return True