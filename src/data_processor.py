import logging
import pandas as pd


logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    rows_before = len(df)
    df = df.drop_duplicates()
    rows_after = len(df)

    logger.debug(
        f"remove_duplicates: {rows_before} → {rows_after} rows"
    )

    return df


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        before = len(df)
        df = df.dropna()
        after = len(df)
        logger.debug(f"handle_missing: {before} → {after} rows")

    elif axis == "columns":
        before = len(df.columns)
        df = df.dropna(axis=1)
        after = len(df.columns)
        logger.debug(f"handle_missing: {before} → {after} columns")

    else:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupported axis: {axis}")

    return df


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ["iqr", "zscore"]:
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")

    for column in columns:
        if column not in df.columns:
            logger.warning(f"Column not found: {column}")
            continue

        if not pd.api.types.is_numeric_dtype(df[column]):
            logger.warning(f"Column is not numeric: {column}")
            continue

        before = len(df)

        if method == "iqr":
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1

            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr

            df = df[
                (df[column] >= lower) &
                (df[column] <= upper)
            ]

            removed = before - len(df)

            logger.debug(
                f"{column}: lower={lower}, upper={upper}, removed={removed}"
            )

        elif method == "zscore":
            mean = df[column].mean()
            std = df[column].std()

            if std == 0:
                removed = 0
            else:
                z_scores = (df[column] - mean).abs() / std
                df = df[z_scores <= threshold]
                removed = before - len(df)

            logger.debug(
                f"{column}: method=zscore, threshold={threshold}, "
                f"removed={removed}"
            )

    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    settings = config["processing"]

    if settings["remove_duplicates"]:
        df = remove_duplicates(df)

    if settings["missing"]["enabled"]:
        df = handle_missing(
            df,
            settings["missing"]["axis"]
        )

    if settings["outliers"]["enabled"]:
        df = remove_outliers(
            df,
            settings["outliers"]["columns"],
            settings["outliers"]["method"],
            settings["outliers"]["threshold"]
        )

    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    report = {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "columns_removed": len(df_before.columns) - len(df_after.columns)
    }

    return report