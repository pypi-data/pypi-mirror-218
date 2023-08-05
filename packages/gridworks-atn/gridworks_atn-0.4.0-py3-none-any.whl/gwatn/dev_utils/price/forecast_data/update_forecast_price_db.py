import csv
import os
import sqlite3

import pendulum
import satn.dev_utils.price.eprt_forecast_sync_100_handler as eprt_forecast_sync_100_handler

from gwatn.types.ps_distprices_gnode.csv_distp_oneprice.csv_distp_oneprice_1_0_0 import (
    Csv_Distp_Oneprice_1_0_0,
)
from gwatn.types.ps_distprices_gnode.csv_distp_sync.csv_distp_sync_1_0_0 import (
    Csv_Distp_Sync_1_0_0,
)
from gwatn.types.ps_electricityprices_gnode.csv_eprt_forecast_sync.csv_eprt_forecast_sync_1_0_0 import (
    Csv_Eprt_Forecast_Sync_1_0_0,
)
from gwatn.types.ps_electricityprices_gnode.csv_eprt_forecast_sync_table.csv_eprt_forecast_sync_table_1_0_0 import (
    Csv_Eprt_Forecast_Sync_Table_1_0_0,
)
from gwatn.types.ps_electricityprices_gnode.csv_eprt_sync.csv_eprt_sync_1_0_0 import (
    Csv_Eprt_Sync_1_0_0,
)
from gwatn.types.ps_regprices_gnode.csv_regp_sync.csv_regp_sync_1_0_0 import (
    Csv_Regp_Sync_1_0_0,
)


DEFAULT_DB_FILE = "src/satn/dev_utils/price/forecast_data/ps_db.sqlite3"
ROOT_INPUT_DIR = "../gridworks-ps/input_data/electricity_prices"


def main(
    root_input_dir=ROOT_INPUT_DIR,
    db_file=DEFAULT_DB_FILE,
):
    os.system("cd src/satn/dev_utils/price/forecast_data/ && python init_ps_db.py")
    price_files_by_type_name = {}
    print(f"Updating forecast price database {db_file}...")
    for subdir, dirs, files in os.walk(root_input_dir):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".csv"):
                with open(filepath) as csv_file:
                    reader = csv.reader(csv_file)
                    try:
                        type_name = next(reader)[1].strip()
                    except Exception as e:
                        raise Exception(
                            f"File {filepath} needs to have type_name in Csv 0,1!"
                        )
                    if type_name not in price_files_by_type_name.keys():
                        price_files_by_type_name[type_name] = [filepath]
                    else:
                        price_files_by_type_name[type_name].append(filepath)

    db = sqlite3.connect(db_file)
    cursor = db.cursor()

    if "csv.eprt.forecast.sync.1_0_0" in price_files_by_type_name.keys():
        for price_file in price_files_by_type_name["csv.eprt.forecast.sync.1_0_0"]:
            try:
                core = Csv_Eprt_Forecast_Sync_1_0_0(price_file).payload.Core
            except Exception as e:
                print(f"Problem with forecast file {price_file}: {e}")
                raise Exception(e)
            cmd = f"SELECT file_name, type_name FROM csv_file_by_key WHERE price_uid = '{core.PriceUid}'"
            rows = cursor.execute(cmd).fetchall()
            if len(rows) == 0:
                forecast_start_time_unix_s = pendulum.parse(
                    core.ForecastStartIso8601Utc
                ).int_timestamp
                forecast_generated_time_unix_s = pendulum.parse(
                    core.ForecastGeneratedIso8601Utc
                ).int_timestamp
                try:
                    cmd = f"INSERT INTO eprt_forecast_sync_100 (price_uid, p_node_alias, forecast_generated_time_unix_s, forecast_start_time_unix_s, method_alias, currency_unit, uniform_slice_duration_minutes, total_slices) VALUES ('{core.PriceUid}','{core.PNodeAlias}',{forecast_generated_time_unix_s},{forecast_start_time_unix_s},'{core.MethodAlias}','{core.CurrencyUnit}',{core.UniformSliceDurationMinutes}, {len(core.Prices)})"
                    cursor.execute(cmd)
                    cmd = f"INSERT INTO csv_file_by_key (price_uid, type_name, file_name) VALUES ('{core.PriceUid}', 'csv.eprt.forecast.sync.1_0_0', '{price_file}');\n"
                    cursor.execute(cmd)
                    db.commit()
                except Exception as e:
                    raise Exception(f"{db_file} data integrity issue with {price_file}")
            elif rows[0][1] != "csv.eprt.forecast.sync.1_0_0":
                raise Exception(
                    f"{db_file} integrity error! File {price_file} has type_name csv.eprt.forecast.sync.1_0_0 in file but shows up in csv_file_by_key with type_name {rows[0][1]}"
                )

    if "csv.eprt.sync.1_0_0" in price_files_by_type_name.keys():
        for price_file in price_files_by_type_name["csv.eprt.sync.1_0_0"]:
            try:
                payload = Csv_Eprt_Sync_1_0_0(price_file).paired_rabbit_payload()
            except Exception as e:
                print(f"Problem with forecast file {price_file}: {e}")
                raise Exception(e)
            cmd = f"SELECT file_name, type_name FROM csv_file_by_key WHERE price_uid = '{payload.PriceUid}'"
            rows = cursor.execute(cmd).fetchall()
            if len(rows) == 0:
                slice_duration_hr_string = (
                    f"[{payload.UniformSliceDurationHrs}] * {len(payload.Prices)}"
                )
                try:
                    cmd = f"INSERT INTO eprt_sync_100 (price_uid, p_node_alias, start_year_utc, start_month_utc, start_day_utc, start_hour_utc, start_minute_utc, method_alias, currency_unit, slice_duration_hrs) VALUES ('{payload.PriceUid}','{payload.PNodeAlias}',{payload.StartYearUtc},{payload.StartMonthUtc},{payload.StartDayUtc},{payload.StartHourUtc},{payload.StartMinuteUtc},'{payload.MethodAlias}', '{payload.CurrencyUnit}','{slice_duration_hr_string}');\n"
                    cursor.execute(cmd)
                    cmd = f"INSERT INTO csv_file_by_key (price_uid, type_name, file_name) VALUES ('{payload.PriceUid}', 'csv.eprt.sync.1_0_0', '{price_file}');\n"
                    cursor.execute(cmd)
                    db.commit()
                except Exception as e:
                    raise Exception(f"{db_file} data integrity issue with {price_file}")
            elif rows[0][1] != "csv.eprt.sync.1_0_0":
                raise Exception(
                    f"{db_file} integrity error! File {price_file} has type_name csv.eprt.sync.1_0_0 in file but shows up in csv_file_by_key with type_name {rows[0][1]}"
                )

    if "csv.distp.oneprice.1_0_0" in price_files_by_type_name.keys():
        for price_file in price_files_by_type_name["csv.distp.oneprice.1_0_0"]:
            orig_csv = Csv_Distp_Oneprice_1_0_0(
                distp_electricity_price_csv=price_file
            ).payload
            cmd = f"SELECT file_name, type_name FROM csv_file_by_key WHERE price_uid = '{orig_csv.PriceUid}'"
            rows = cursor.execute(cmd).fetchall()
            if len(rows) == 0:
                slice_duration_hr_string = f"None"
                try:
                    cmd = f"INSERT INTO distp_oneprice_100 (price_uid, p_node_alias, start_year_utc, start_month_utc, start_day_utc, start_hour_utc, start_minute_utc, method_alias, currency_unit, slice_duration_hrs) VALUES ('{orig_csv.PriceUid}','{orig_csv.PNodeAlias}',{orig_csv.StartYearUtc},{orig_csv.StartMonthUtc},{orig_csv.StartDayUtc},{orig_csv.StartHourUtc},{orig_csv.StartMinuteUtc},'{orig_csv.MethodAlias}', '{orig_csv.CurrencyUnit}','{slice_duration_hr_string}');\n"
                    cursor.execute(cmd)
                    cmd = f"INSERT INTO csv_file_by_key (price_uid, type_name, file_name) VALUES ('{orig_csv.PriceUid}', 'csv.distp.oneprice.1_0_0', '{price_file}');\n"
                    cursor.execute(cmd)
                    db.commit()
                except Exception as e:
                    raise Exception(f"{db_file} data integrity issue with {price_file}")
            elif rows[0][1] != "csv.distp.oneprice.1_0_0":
                raise Exception(
                    f"{db_file} integrity error! File {price_file} has type_name csv.distp.oneprice.1_0_0 in file but shows up in csv_file_by_key with type_name {rows[0][1]}"
                )

    if "csv.distp.sync.1_0_0" in price_files_by_type_name.keys():
        for price_file in price_files_by_type_name["csv.distp.sync.1_0_0"]:
            orig_csv = Csv_Distp_Sync_1_0_0(
                distp_electricity_price_csv=price_file
            ).payload
            cmd = f"SELECT file_name, type_name FROM csv_file_by_key WHERE price_uid = '{orig_csv.PriceUid}'"
            rows = cursor.execute(cmd).fetchall()
            if len(rows) == 0:
                slice_duration_hr_string = (
                    f"[{orig_csv.UniformSliceDurationHrs}] * {len(orig_csv.Prices)}"
                )
                try:
                    cmd = f"INSERT INTO distp_sync_100 (price_uid, p_node_alias, start_year_utc, start_month_utc, start_day_utc, start_hour_utc, start_minute_utc, method_alias, currency_unit, slice_duration_hrs) VALUES ('{orig_csv.PriceUid}','{orig_csv.PNodeAlias}',{orig_csv.StartYearUtc},{orig_csv.StartMonthUtc},{orig_csv.StartDayUtc},{orig_csv.StartHourUtc},{orig_csv.StartMinuteUtc},'{orig_csv.MethodAlias}', '{orig_csv.CurrencyUnit}','{slice_duration_hr_string}');\n"
                    cursor.execute(cmd)
                    cmd = f"INSERT INTO csv_file_by_key (price_uid, type_name, file_name) VALUES ('{orig_csv.PriceUid}', 'csv.distp.sync.1_0_0', '{price_file}');\n"
                    cursor.execute(cmd)
                    db.commit()
                except Exception as e:
                    raise Exception(f"{db_file} data integrity issue with {price_file}")
            elif rows[0][1] != "csv.distp.sync.1_0_0":
                raise Exception(
                    f"{db_file} integrity error! File {price_file} has type_name csv.distp.sync.1_0_0 in file but shows up in csv_file_by_key with type_name {rows[0][1]}"
                )

    if "csv.regp.sync.1_0_0" in price_files_by_type_name.keys():
        for price_file in price_files_by_type_name["csv.regp.sync.1_0_0"]:
            orig_csv = Csv_Regp_Sync_1_0_0(reg_price_csv=price_file).payload
            cmd = f"SELECT file_name, type_name FROM csv_file_by_key WHERE price_uid = '{orig_csv.PriceUid}'"
            rows = cursor.execute(cmd).fetchall()
            if len(rows) == 0:
                slice_duration_hr_string = (
                    f"[{orig_csv.UniformSliceDurationHrs}] * {len(orig_csv.Prices)}"
                )
                try:
                    cmd = f"INSERT INTO regp_sync_100 (price_uid, p_node_alias, start_year_utc, start_month_utc, start_day_utc, start_hour_utc, start_minute_utc, method_alias, currency_unit, slice_duration_hrs) VALUES ('{orig_csv.PriceUid}','{orig_csv.PNodeAlias}',{orig_csv.StartYearUtc},{orig_csv.StartMonthUtc},{orig_csv.StartDayUtc},{orig_csv.StartHourUtc},{orig_csv.StartMinuteUtc},'{orig_csv.MethodAlias}', '{orig_csv.CurrencyUnit}','{slice_duration_hr_string}');\n"
                    cursor.execute(cmd)
                    cmd = f"INSERT INTO csv_file_by_key (price_uid, type_name, file_name) VALUES ('{orig_csv.PriceUid}','csv.regp.sync.1_0_0','{price_file}');\n"
                    cursor.execute(cmd)
                    db.commit()
                except Exception as e:
                    raise Exception(f"{db_file} data integrity issue with {price_file}")
            elif rows[0][1] != "csv.regp.sync.1_0_0":
                raise Exception(
                    f"{db_file} integrity error! File {price_file} has type_name csv.regp.sync.1_0_0 in file but shows up in csv_file_by_key with type_name {rows[0][1]}"
                )

    if "csv.eprt.forecast.sync.table.1_0_0" in price_files_by_type_name.keys():
        for price_file in price_files_by_type_name[
            "csv.eprt.forecast.sync.table.1_0_0"
        ]:
            try:
                payload = Csv_Eprt_Forecast_Sync_Table_1_0_0(
                    price_file=price_file
                ).payload
            except Exception as e:
                print(f"Problem with forecast file {price_file}: {e}")
                raise Exception(e)
            for core in payload.CoreList:
                try:
                    eprt_forecast_sync_100_handler.create_if_missing_forecast_sync_csv_from_rabbit_payload(
                        core=core
                    )
                except Exception as e:
                    raise Exception(f"Problem with {price_file}\n{e}")

    db.close()
