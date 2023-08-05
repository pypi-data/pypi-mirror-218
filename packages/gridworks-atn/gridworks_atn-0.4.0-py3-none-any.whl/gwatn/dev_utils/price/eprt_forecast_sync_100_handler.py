import os
import sqlite3
import uuid

import pendulum

import gwatn.types.hack_test_dummy as test_dummy
from gwatn.types.eprt.gt_eprt_forecast_sync_1_0_0 import Gt_Eprt_Forecast_Sync_1_0_0
from gwatn.types.eprt.gt_eprt_forecast_sync_1_0_0 import GtEprtForecastSync100

# Message payloads for messages received
from gwatn.types.gnode_eprequest_ps.r_get_eprt_forecast_sync.r_get_eprt_forecast_sync_1_0_0 import (
    Payload as RGetEprtForecastSync100,
)
from gwatn.types.ps_electricityprices_gnode.csv_eprt_forecast_sync.csv_eprt_forecast_sync_1_0_0 import (
    Csv_Eprt_Forecast_Sync_1_0_0,
)
from gwatn.types.ps_electricityprices_gnode.r_eprt_forecast_sync.r_eprt_forecast_sync_1_0_0 import (
    Payload as REprtForecastSync100Payload,
)


# MessageMakers for reading eprt (electricity price real time) from csvs


DB_FILE = "src/satn/dev_utils/price/forecast_data/ps_db.sqlite3"
GITIGNORED_FILE_DIR_ROOT = "input_data/gitignored/electricity_prices"


def csv_file_by_uid(price_uid: str) -> str:
    db_file = DB_FILE
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cmd = f"SELECT file_name FROM csv_file_by_key WHERE type_name = 'csv.eprt.forecast.sync.1_0_0' AND price_uid = '{price_uid}'"
    rows = cursor.execute(cmd).fetchall()
    if len(rows) == 0:
        raise Exception(
            f"PriceUid {price_uid} is not associated with any csv.eprt.forecast.sync.1_0_0 files!!"
        )
        # TODO: turn this into sending back an error message
    cursor.close()
    db.close()
    file = rows[0][0]
    return file


def response_to_gnode_eprt_sync_request(
    req: RGetEprtForecastSync100, agent: test_dummy.TEST_DUMMY_AGENT
) -> REprtForecastSync100Payload:
    db_file = DB_FILE
    forecast_start_utc = pendulum.datetime(
        year=req.StartYearUtc,
        month=req.StartMonthUtc,
        day=req.StartDayUtc,
        hour=req.StartHourUtc,
        minute=req.StartMinuteUtc,
    )
    forecast_start_unix_s = forecast_start_utc.int_timestamp
    if agent == test_dummy.TEST_DUMMY_AGENT:
        request_received_unix_s = forecast_start_unix_s - 250
    else:
        request_received_unix_s = agent.latest_time_unix_s
    uniform_slice_duration_minutes = int(req.UniformSliceDurationHrs * 60)
    real_p_node_alias = ".".join(["w"] + req.PNodeAlias.split(".")[1:])
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cmd = (
        f"SELECT price_uid, forecast_generated_time_unix_s FROM eprt_forecast_sync_100 WHERE p_node_alias = '{real_p_node_alias}' AND method_alias = '{req.MethodAlias}' "
        + f"AND uniform_slice_duration_minutes = {uniform_slice_duration_minutes} AND  total_slices = {req.TotalSlices} and forecast_start_time_unix_s = {forecast_start_unix_s} AND forecast_generated_time_unix_s < {request_received_unix_s}"
    )
    rows = cursor.execute(cmd).fetchall()
    if len(rows) == 0:
        return None
    latest_prediction_uid = sorted(rows, key=lambda x: -x[1])[0][0]
    cmd = f"SELECT file_name FROM csv_file_by_key WHERE type_name = 'csv.eprt.forecast.sync.1_0_0' AND price_uid = '{latest_prediction_uid }'"
    files = cursor.execute(cmd).fetchall()
    if len(files) != 1:
        raise Exception(f"Database problem with price_uid {latest_prediction_uid}")
    file = files[0][0]
    response = Csv_Eprt_Forecast_Sync_1_0_0(
        real_time_electricity_price_csv=file
    ).payload
    if len(response.Core.Prices) == req.TotalSlices:
        return response
    elif len(response.Core.Prices) < req.TotalSlices:
        raise NotImplementedError(
            f"file has {len(response.Core.Prices)} prices and request asked for {req.TotalSlices}"
        )
    else:
        new_prices = response.Core.Prices[0 : len(req.TotalSlices)]
        new_price_uid = str(uuid.uuid4())
        new_comment = (
            response.Core.Comment + f" from beginning of {response.Core.PriceUid}"
        )
        core = Gt_Eprt_Forecast_Sync_1_0_0(
            prices=new_prices,
            method_alias=response.Core.MethodAlias,
            p_node_alias=response.Core.PNodeAlias,
            timezone_string=response.Core.TimezoneString,
            currency_unit=response.Core.TimezoneString,
            uniform_slice_duration_minutes=response.Core.UniformSliceDurationMinutes,
            forecast_start_iso8601_utc=response.Core.ForecastStartIso8601Utc,
            forecast_generated_iso8601_utc=response.Core.ForecastGeneratedIso8601Utc,
            price_uid=new_price_uid,
            comment=new_comment,
        ).payload
        create_if_missing_forecast_sync_csv_from_rabbit_payload(core=core)


def create_if_missing_forecast_sync_csv_from_rabbit_payload(
    core: GtEprtForecastSync100,
) -> GtEprtForecastSync100:
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cmd = f"SELECT file_name, type_name, price_uid FROM csv_file_by_key WHERE price_uid = '{core.PriceUid}'"
    price_uid_rows = cursor.execute(cmd).fetchall()
    cmd = (
        f"SELECT price_uid FROM eprt_forecast_sync_100 WHERE p_node_alias = '{core.PNodeAlias}'"
        + f" AND forecast_generated_time_unix_s = {pendulum.parse(core.ForecastGeneratedIso8601Utc).int_timestamp}"
        + f" AND forecast_start_time_unix_s = {pendulum.parse(core.ForecastStartIso8601Utc).int_timestamp}"
        + f" AND method_alias = '{core.MethodAlias}'"
        + f" AND total_slices = {len(core.Prices)}"
        + f" AND uniform_slice_duration_minutes = {core.UniformSliceDurationMinutes}"
    )
    eprt_forecast_rows = cursor.execute(cmd).fetchall()
    if len(eprt_forecast_rows) > 0:
        # this forecast already exists. Populate the core and return it.
        price_uid = eprt_forecast_rows[0][0]
        cmd = f"SELECT file_name from csv_file_by_key WHERE price_uid = '{price_uid}'"
        file_rows = cursor.execute(cmd).fetchall()
        if len(file_rows) == 0:
            raise Exception(
                f"db integrity error with {price_uid} between tables csv_file_by_key and file_name from csv_file_by_key\n check {DB_FILE}"
            )
        price_file = file_rows[0][0]
        existing_core = Csv_Eprt_Forecast_Sync_1_0_0(price_file=price_file).payload.Core
        return existing_core
    if len(price_uid_rows) > 0:
        if price_uid_rows[0][1] != "csv.eprt.forecast.sync.1_0_0":
            raise Exception(
                f"{DB_FILE} integrity error! Expecting type_name csv.eprt.forecast.sync.1_0_0 for {price_file} but file but shows up in csv_file_by_key with type_name {rows[0][1]}"
            )
        if len(eprt_forecast_rows) == 0:
            raise Exception(
                f"Data integrity error with eprt_forecast_sync_100 table! \nprice_uid exists but does not match msg .... try  SELECT type_name, file_name FROM csv_file_by_key WHERE price_uid = '{core.PriceUid}'; \n {core} \n db location: {DB_FILE}"
            )

    forecast_start_utc = pendulum.parse(core.ForecastStartIso8601Utc)
    iso = core.PNodeAlias.split(".")[1]
    real_p_node_alias = ".".join(["w"] + core.PNodeAlias.split(".")[1:])
    hours = int(core.UniformSliceDurationMinutes * len(core.Prices) / 60)
    uid_pre = core.PriceUid.split("-")[0]
    price_file = f'{GITIGNORED_FILE_DIR_ROOT}/{iso}/eprt__{forecast_start_utc.strftime("%Y%m%dT%H%M")}__{real_p_node_alias}___{hours}__{core.MethodAlias}__{uid_pre}.csv'
    lines = [
        f"MpAlias,csv.eprt.forecast.sync.1_0_0\n",
        f"PNodeAlias,{core.PNodeAlias}\n",
        f"MethodAlias,{core.MethodAlias}\n",
        f"Comment,{core.Comment}\n",
        f"ForecastGeneratedIso8601Utc,{core.ForecastGeneratedIso8601Utc}\n",
        f"ForecastStartIso8601Utc,{core.ForecastStartIso8601Utc}\n",
        f"UniformSliceDurationMinutes,{core.UniformSliceDurationMinutes}\n",
        f"TimezoneString,{core.TimezoneString}\n",
        f"CurrencyUnit,{core.CurrencyUnit}\n",
        f"PriceUid,{core.PriceUid}\n",
        f"Header,Forecast Real Time LMP Electricity Price (Currency Unit/MWh)\n",
    ]
    for price in core.Prices:
        lines.append(f"{price}\n")
    with open(price_file, "w") as outfile:
        outfile.writelines(lines)

    try:
        cmd = f"INSERT INTO eprt_forecast_sync_100 (price_uid, p_node_alias, forecast_generated_time_unix_s, forecast_start_Time_unix_s, method_alias, currency_unit, uniform_slice_duration_minutes, total_slices) VALUES ('{core.PriceUid}','{core.PNodeAlias}',{pendulum.parse(core.ForecastGeneratedIso8601Utc).int_timestamp},{pendulum.parse(core.ForecastStartIso8601Utc).int_timestamp},'{core.MethodAlias}','{core.CurrencyUnit}',{core.UniformSliceDurationMinutes}, {len(core.Prices)})"
        cursor.execute(cmd)
        cmd = f"INSERT INTO csv_file_by_key (price_uid, type_name, file_name) VALUES ('{core.PriceUid}', 'csv.eprt.forecast.sync.1_0_0', '{price_file}');\n"
        cursor.execute(cmd)
        db.commit()
    except Exception as e:
        os.system(f"rm {price_file}")
        db.close()
        raise Exception(
            f"Failure storing new local forecast {price_file} in ps_db.sqlite3! Not generating: {e}"
        )
    cursor.close()
    db.close()
    print(f"Done creating new csv.eprt.forecast.sync.1_0_0 price file {price_file}")
    return core
