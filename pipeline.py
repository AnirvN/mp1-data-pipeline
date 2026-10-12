"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)

'''
def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )
'''

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run the data processing pipeline."
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the input file"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to the output file"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the YAML configuration file"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    return parser.parse_args()

'''
def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if Path(filepath).is_file():
        logger.info(f"Input file validated: {filepath}")
        return True

    logger.error(f"Input file not found: {filepath}")
    return False
'''

def main():
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(f"Arguments parsed: {args}")

    # Validate file paths
    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    # Load data and configuration
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # Read validation settings
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    # Validate the dataset
    rows_before = len(data)

    try:
        validated_data = validate_dataframe(
            data, required_columns, numeric_columns
        )
    except ValueError:
        sys.exit(1)

    logger.info(
        f"Validation complete: {rows_before} → {len(validated_data)} rows"
    )

    # Keep a copy before cleaning
    original_data = validated_data.copy()

    # Process the dataset
    try:
        cleaned_data = process_data(validated_data, config)
    except ValueError:
        sys.exit(1)

    logger.info(
        f"Processing complete: {len(original_data)} → {len(cleaned_data)} rows"
    )

    # Save the cleaned dataset
    output_path = save_data(cleaned_data, args.output)
    logger.info(f"Saved cleaned data to {output_path}")

    # Print the cleaning report
    report = create_cleaning_report(original_data, cleaned_data)
    print("\nCleaning report:")
    print(report)


if __name__ == "__main__":
    main()