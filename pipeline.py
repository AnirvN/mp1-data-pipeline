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
from pathlib import Path
from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )


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


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if Path(filepath).is_file():
        logger.info(f"Input file validated: {filepath}")
        return True

    logger.error(f"Input file not found: {filepath}")
    return False


def main():
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(f"Arguments parsed: {args}")

    # Validate input and config files
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

    # Save a copy of the original data
    original_data = data.copy()

    # Process the data
    try:
        cleaned_data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    # Create and print cleaning report
    report = create_cleaning_report(original_data, cleaned_data)
    print(report)

    # Log results
    logger.info(
        f"Processing complete: {len(original_data)} → {len(cleaned_data)} rows"
    )

    # Save cleaned data
    cleaned_data.to_csv(args.output, index=False)
    logger.info(f"Saved cleaned data to {args.output}")


if __name__ == "__main__":
    main()