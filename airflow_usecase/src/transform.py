import pandas as pd

def transform_data(df):

    df["name"] = df["name"].str.strip()
    df["email"] = df["email"].str.lower()
    df["city"] = df["city"].str.strip()

    df["updated_at"] = pd.to_datetime(
        df["updated_at"]
    )

    return df