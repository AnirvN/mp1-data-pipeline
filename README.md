
Pipeline Overview:
This project is a Python created pipeline that loads, validates, cleans, and saves datasets. The pipeline.py file manages the workflow. The data_loaders.py file loads CSV, JSON, and YAML files. The data_validaters.py file checks the required columns and uses that to remove invalid values. The data_processor.py file takes out duplicates, missing values, and outliers using the settings in config/config.yaml. The data_output.py file saves the cleaned data as a CSV file, and the utils.py file handles the logging and file validation. The pipeline then outputs a report showing the amount of rows and columns that were removed.



Example Command:
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose


Output:
The sample dataset(sample_data.csv) contains 100 rows. Validation removes 2 invalid rows, and processing removes 6 more rows.The example command would produce  The final cleaned dataset contains 92 rows and 5 columns, saved to output/clean.csv.

16:40:22 DEBUG    __main__ — Arguments parsed: Namespace(input='fixtures/sample_data.csv', output='output/clean.csv', config='config/config.yaml', verbose=True)
16:40:22 INFO     src.utils — Input file validated: fixtures/sample_data.csv
16:40:22 INFO     src.utils — Input file validated: config/config.yaml
16:40:22 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
16:40:22 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
16:40:22 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
16:40:22 DEBUG    src.data_validator — Validation: 100 → 98 rows
16:40:22 INFO     __main__ — Validation complete: 100 → 98 rows
16:40:22 DEBUG    src.data_processor — remove_duplicates: 98 → 96 rows
16:40:22 DEBUG    src.data_processor — handle_missing: 96 → 94 rows
16:40:22 DEBUG    src.data_processor — rating: lower=43.625, upper=106.625, removed=2
16:40:22 INFO     __main__ — Processing complete: 98 → 92 rows
16:40:22 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
16:40:22 INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}