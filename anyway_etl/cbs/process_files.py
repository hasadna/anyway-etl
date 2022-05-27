import os
import shutil
import zipfile
from pprint import pprint
from collections import defaultdict

import pandas as pd
import dataflows as DF

from .config import (
    CBS_EMAILS_DATA_ROOT_PATH, CBS_FILES_ROOT_PATH,
    CBS_YEARLY_DIRECTORIES_ROOT_PATH,
    CBS_PROCESSED_FILES_ROOT_PATH
)


CBS_FILES_HEBREW = {
    "sadot": "Fields",
    "zmatim_ironiim": "IntersectUrban",
    "zmatim_lo_ironiim": "IntersectNonUrban",
    "rehev": "VehData",
    "milon": "Dictionary",
    "meoravim": "InvData",
    "klali": "AccData",
    "rechovot": "DicStreets",
}


def extract_zip_files(row):
    zip_filepath = os.path.join(CBS_FILES_ROOT_PATH, row['filename'])
    row['extracted_path'] = row['filename'].replace('.zip', '')
    extracted_path = os.path.join(CBS_FILES_ROOT_PATH, row['extracted_path'])
    # print("Extracting {} -> {}".format(zip_filepath, extracted_path))
    shutil.rmtree(extracted_path, ignore_errors=True)
    os.makedirs(extracted_path)
    with zipfile.ZipFile(zip_filepath, "r") as zf:
        zf.extractall(extracted_path)


def update_cbs_files_names(row):
    extracted_path = os.path.join(CBS_FILES_ROOT_PATH, row['extracted_path'])
    # print('updating cbs file names {}'.format(extracted_path))
    files = sorted([path for path in os.listdir(extracted_path)])
    for file in files:
        file_path = os.path.join(extracted_path, file)
        for hebrew_file_name, english_file_name in CBS_FILES_HEBREW.items():
            if hebrew_file_name in file.lower() and english_file_name.lower() not in file.lower():
                os.rename(file_path, file_path.replace(".csv", "_" + english_file_name + ".csv"))


def get_accidents_file_data(directory):
    for file_path in os.listdir(directory):
        if file_path.endswith("{0}{1}".format(CBS_FILES_HEBREW["klali"], ".csv")):
            return os.path.join(directory, file_path)


def get_provider_code_and_year(row):
    extracted_path = os.path.join(CBS_FILES_ROOT_PATH, row['extracted_path'])
    file_path = get_accidents_file_data(extracted_path)
    df = pd.read_csv(file_path, encoding="cp1255")
    provider_code = df.iloc[0]["sug_tik"]
    year = df["SHNAT_TEUNA"].mode().values[0]
    row['provider_code'] = int(provider_code)
    row['year'] = int(year)


def save_to_directory_structure(rows):
    updated_year_provider_codes = set()
    for row in rows:
        row['num_saved_files'] = 0
        provider_code = row['provider_code']
        year = row['year']
        if '{}|{}'.format(year, provider_code) not in updated_year_provider_codes:
            updated_year_provider_codes.add('{}|{}'.format(year, provider_code))
            extracted_path = os.path.join(CBS_FILES_ROOT_PATH, row['extracted_path'])
            base_file_path = os.path.join(
                CBS_YEARLY_DIRECTORIES_ROOT_PATH,
                'accidents_type_{}'.format(provider_code),
                str(year)
            )
            print('Saving msgId {} mtime {} to {}'.format(row['msgId'], row['mtime'], base_file_path))
            shutil.rmtree(base_file_path, ignore_errors=True)
            os.makedirs(base_file_path)
            file: os.DirEntry
            for file in os.scandir(extracted_path):
                row['num_saved_files'] += 1
                target_file_path = os.path.join(base_file_path, os.path.basename(file.path))
                shutil.copy(file.path, target_file_path)
        yield row


def main():
    stats = defaultdict(int)
    _, df_stats = DF.Flow(
        DF.load(os.path.join(CBS_EMAILS_DATA_ROOT_PATH, 'datapackage.json')),
        DF.add_field('extracted_path', 'string'),
        extract_zip_files,
        update_cbs_files_names,
        DF.add_field('provider_code', 'integer'),
        DF.add_field('year', 'integer'),
        get_provider_code_and_year,
        DF.sort_rows('{year}|{provider_code}', reverse=True),
        DF.add_field('num_saved_files', 'integer'),
        save_to_directory_structure,
        DF.dump_to_path(CBS_PROCESSED_FILES_ROOT_PATH),
        DF.printer()
    ).process()
    pprint(df_stats)
    pprint(dict(stats))
