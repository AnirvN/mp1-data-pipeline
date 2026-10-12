import logging
import pandas as pd

logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data."""
    rows_before = len(df)

    # Check required columns
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Missing required column: {col}")
            raise ValueError(f"Missing required column: {col}")

    # Check numeric columns
    for col in numeric_columns:
        if col not in df.columns:
            logger.error(f"Missing numeric column: {col}")
            raise ValueError(f"Missing numeric column: {col}")

        invalid_rows = []

        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except (ValueError, TypeError):
                    invalid_rows.append(i)

        if invalid_rows:
            logger.warning(
                f"Removed {len(invalid_rows)} rows with invalid numeric "
                f"values in {col}"
            )
            df = df.drop(index=invalid_rows)

        df[col] = pd.to_numeric(df[col])

    logger.debug(
        f"Validation: {rows_before} → {len(df)} rows"
    )

    return df