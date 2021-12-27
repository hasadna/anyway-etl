import os
import math
import datetime
from pprint import pprint
from collections import defaultdict

import dataflows as DF

from .get_files import get_files
from ..itm_to_wgs84 import ItmToWGS84
from .config import CBS_YEARLY_DIRECTORIES_ROOT_PATH


coordinates_converter = ItmToWGS84()


def get_data_value(value):
    """
    :returns: value for parameters which are not mandatory in an accident data
    OR -1 if the parameter value does not exist
    """
    return None if value is None or math.isnan(value) else int(value)


def common_get_data_iterator(load_start_year, stats, get_data_iterator):
    for provider_code in [1, 3]:
        for year in range(load_start_year, datetime.datetime.now().year + 1):
            cbs_files_dir = os.path.join(
                CBS_YEARLY_DIRECTORIES_ROOT_PATH,
                'accidents_type_{}'.format(provider_code),
                str(year)
            )
            print("cbs_files_dir={}".format(cbs_files_dir))
            files_from_cbs = get_files(cbs_files_dir)
            if len(files_from_cbs) == 0:
                stats['invalid_directories_without_cbs_files'] += 1
                print('invalid directory (no cbs files): {}'.format(cbs_files_dir))
                continue
            stats['valid_directories'] += 1
            for row in get_data_iterator(stats, files_from_cbs):
                yield {
                    '__provider_code': provider_code,
                    '__year': year,
                    **row
                }


def common_main(load_start_year, output_path, get_data_iterator):
    load_start_year = int(load_start_year) if load_start_year else datetime.datetime.now().year - 1
    print("load_start_year={} output_path={}".format(load_start_year, output_path))
    stats = defaultdict(int)
    _, df_stats = DF.Flow(
        common_get_data_iterator(load_start_year, stats, get_data_iterator),
        DF.dump_to_path(output_path)
    ).process()
    pprint(df_stats)
    pprint(dict(stats))


def get_saved_data(datapackage_filename, provider_code, year):
    provider_code, year = int(provider_code), int(year)
    return DF.Flow(
        DF.load(datapackage_filename),
        DF.filter_rows(lambda row: int(row['__provider_code']) == provider_code and int(row['__year']) == year),
        DF.delete_fields(['__provider_code', '__year'])
    ).results()[0][0]
