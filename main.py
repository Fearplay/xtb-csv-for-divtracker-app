import pandas as pd
import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="Path to XTB csv file")
ap.add_argument("-o", "--output", required=True, help="Path for your output csv file")
args = vars(ap.parse_args())

input_path = args["input"]
output_path = args["output"]

if not os.path.exists(input_path):
    raise FileNotFoundError(f"File {input_path} does not exist")

data_from_xtb = pd.read_csv(input_path, usecols=["Symbol", "Comment", "Time"], sep=";")
data_to_app = data_from_xtb.copy()

new_columns = ["Ticker", "Quantity", "Cost Per Share", "Date"]
data_to_app = data_to_app.reindex(columns=new_columns)

data_to_app["Ticker"] = data_from_xtb["Symbol"]
data_to_app["Quantity"] = data_from_xtb["Comment"].str.split(" ").str[2].str.split("/").str[0]
data_to_app["Cost Per Share"] = data_from_xtb["Comment"].str.split(" ").str[4]
data_to_app["Date"] = pd.to_datetime(data_from_xtb["Time"].str.split(" ").str[0], dayfirst=True)

data_to_app.to_csv(output_path, index=False, sep=";")
