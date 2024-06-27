import os
import sys
import math
import numpy as np
import pandas as pd

from dotenv import load_dotenv

# loading .env
load_dotenv()

# Getting .csv file path
path = os.getenv("path")


def get_number_with_any_separator(text):
    text = str(text).replace(" ", "")
    text = text.replace("$", "")
    foundSeparator = ""
    for i in range(-1, -len(text), -1):
        if text[i] == "." or text[i] == ",":
            foundSeparator = text[i]
            break
    if foundSeparator == ".":  # Imperial format xxx,xxx.xx
        text = text.replace(",", "")
    if foundSeparator == ",":  # European format xxx.xxx,xx
        text = text.replace(".", "")
        text = text.replace(",", ".")
    return try_float(text)


def try_float(text):
    try:
        auxValue = float(text)
    except ValueError:
        return None
    if not math.isnan(auxValue):
        return auxValue
    else:
        return None


# Function to check if any word is in the header
def check_header(headers):
    columns = ["date", "amount", "description", "type"]
    new_headers = []

    # Normalize columns for comparison
    normalized_columns = {col.lower(): col for col in columns}

    for header in headers:
        # Split the header into words and normalize
        words = header.lower().split()
        # Check if any word in the header is in columns
        replaced = False
        for word in words:
            if word in normalized_columns:
                # If a match is found, replace the header with the column
                # name preserving the original format from columns
                new_headers.append(normalized_columns[word].capitalize())
                replaced = True
                break
        # If no words matched, keep the original header
        if not replaced:
            new_headers.append(header)

    return new_headers


def format_columns(df):
    my_list = df.columns.tolist()

    # Convert list to set
    unique_items = set(my_list)

    # Check if there are duplicates
    if len(unique_items) < len(my_list):
        index = [
            index for index, value in
            enumerate(df.columns.tolist()) if value == "Date"
        ]

        # Convert DataFrame to a numpy array
        data_array = df.values

        # Index of the column to remove
        index_to_remove = max(index)

        # Delete the column from the array
        modified_array = np.delete(data_array, index_to_remove, axis=1)

        # Convert the array back to a DataFrame
        # We need to handle the column names manually
        new_column_names = [
            col for idx, col in enumerate(df.columns) if idx != index_to_remove
        ]
        new_df = pd.DataFrame(modified_array, columns=new_column_names)

        df = new_df

    # Iterating through rows and then through elements in each row
    for i, (col_name, value) in enumerate(df.iloc[0].items()):
        if "Amount" in col_name:
            df[f"{col_name}"] = (df[f"{col_name}"].
                                 apply(get_number_with_any_separator))
            df[f"{col_name}"] = df[f"{col_name}"].apply(pd.to_numeric)

        if col_name == "Date":
            df[f"{col_name}"] = pd.to_datetime(
                df[f"{col_name}"], infer_datetime_format=True
            )  # format="%m/%d/%Y")

        num_rows = df[col_name].shape[0]
        miss_val_perc = df[col_name].isnull().sum() / num_rows * 100
        if df[col_name].isnull().sum() != 0:
            if miss_val_perc >= 80:
                df.drop(col_name, axis=1, inplace=True)
            else:
                most_common = df[col_name].value_counts().index[0]
                df[col_name].fillna(most_common, inplace=True)

    return df


if __name__ == "__main__":
    if len(sys.argv) == 2:
        file = sys.argv[1]
        df = pd.read_csv(file)

        # Check headers and change columns names
        df.columns = check_header(df.columns)
        df = format_columns(df)
        print(df.info())
    else:
        df = pd.read_csv(path)

        # Check headers and change columns names
        df.columns = check_header(df.columns)
        df = format_columns(df)
        print(df.info())
