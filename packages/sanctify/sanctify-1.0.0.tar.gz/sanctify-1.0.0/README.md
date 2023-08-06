# Sanctify

Sanctify is a Python package designed to facilitate data cleansing and validation operations on pandas DataFrames. It provides a set of predefined transformations and validations that can be applied to different columns of a DataFrame based on a column mapping schema. The package allows you to define data types, transformations, and validations for each column, making it easy to clean and validate your data.

## Features

- Cleansing and validation of data in pandas DataFrames.
- Support for custom transformations and validations.
- Configurable column mapping schema to define data types and operations for each column.
- Built-in transformations for common data cleaning tasks.
- Validation functions for common data validation checks.
- Flexibility to handle various data types and formats.
- Ability to handle missing or malformed data gracefully.

## Installation

You can install Sanctify using pip:

```shell
pip install sanctify
```

## Usage
```python
import pandas as pd
from frozendict import frozendict
from sanctify.cleanser import Cleanser
from sanctify.main import process_cleansed_df

# Define the column mapping schema
column_mapping_schema = frozendict({
    "first_name": {
        "standard_column": "First Name",
        "data_type": "name"
    },
    "last_name": {
        "standard_column": "Last Name",
        "data_type": "name"
    },
    "dob": {
        "standard_column": "DOB",
        "data_type": "date"
    },
    "phone": {
        "standard_column": "Phone",
        "data_type": "phone"
    }
})

# Define the data type schema
data_type_schema = frozendict({
    "name": {
        "transformations": [
            "strip",
            ("replace", {"old": ".", "new": ""}),
            "title"
        ]
    },
    "date": {
        "transformations": [
            ("parse_date", {"format": "%m-%d-%Y"})
        ],
        "validations": [
            ("validate_age", {"min_age": 18})
        ]
    },
    "phone": {
        "transformations": [
            ("remove_characters", {"characters": "+()-"})
        ],
        "validations": [
            ("validate_phone", {"country_code": "US"})
        ]
    }
})

# Read the input DataFrame
input_data = [
    {
        "first_name": "John. A ii jr.",
        "last_name": "Doe",
        "dob": "01-03-1996",
        "phone": "+1-123-456-7890"
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "dob": "12-15-2000",
        "phone": "+1-987-654-3210"
    }
]
input_df = pd.DataFrame(input_data)

# Initialize the Cleanser object
cleanser = Cleanser(input_df, column_mapping_schema)

# Perform cleansing operations
cleanser.remove_trailing_spaces_from_column_headers()
cleanser.drop_unmapped_columns()
cleanser.drop_fully_empty_rows()
cleanser.remove_trailing_spaces_from_each_cell_value()
cleanser.replace_column_headers()

# Process the cleansed DataFrame
processed_df = process_cleansed_df(cleanser.df, column_mapping_schema, data_type_schema)

# Output the processed DataFrame
print(processed_df)
```

## Contributing
Contributions to Sanctify are welcome! If you find any bugs, have feature requests, or want to contribute code, please open an issue or submit a pull request on the [GitHub repository](https://github.com/skit-ai/sanctify/).
