import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def save_data(df, filepath):
    """Save a DataFrame as a CSV file."""

    path = Path(filepath)

    # Create the output folder if needed
    path.parent.mkdir(parents=True, exist_ok=True)

    # Save the cleaned data
    df.to_csv(path, index=False)

    # Log the results
    logger.debug(f"Saved {len(df)} rows to {path}")

    return path