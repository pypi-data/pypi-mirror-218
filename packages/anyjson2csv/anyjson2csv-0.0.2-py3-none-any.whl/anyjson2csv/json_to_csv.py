import json
import pandas as pd
from flatten_json import flatten


def convert_json_to_csv(json_data, csv_filename):
    # Correcting JSON errors
    try:
        parsed_json = json.loads(json_data)
    except json.JSONDecodeError as e:
        print("Invalid JSON:", str(e))
        return

    # Flattening JSON
    try:
        flattened_data = flatten(parsed_json)

    except Exception as e:
        print("Error occurred while flattening JSON:", str(e))
        return

    try:
        df = pd.DataFrame(flattened_data)
        df.to_csv(csv_filename, index=False, encoding="utf-8")

    except:
        print("Error occurred while writing CSV file.")
