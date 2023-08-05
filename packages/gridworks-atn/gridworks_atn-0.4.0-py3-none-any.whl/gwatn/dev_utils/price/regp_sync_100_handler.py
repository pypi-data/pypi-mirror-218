import datetime
import sqlite3
import uuid

import gwprice.dev_utils.price_source_files as price_source_files
import pendulum
from gridworks.errors import SchemaError

import gwatn.types.hack_test_dummy as test_dummy

# Regp Requests received
from gwatn.types.gnode_regprequest_ps.r_gnode_regp_sync_req.r_gnode_regp_sync_req_1_0_0 import (
    Payload as RGnodeRegpSyncReq100Payload,
)
from gwatn.types.gnode_regprequest_ps.r_gnode_regp_sync_req.r_gnode_regp_sync_req_1_0_0 import (
    R_Gnode_Regp_Sync_Req_1_0_0,
)
from gwatn.types.ps_regprices_gnode.csv_regp_sync.csv_regp_sync_1_0_0 import (
    Csv_Regp_Sync_1_0_0,
)
from gwatn.types.ps_regprices_gnode.r_regp_sync.r_regp_sync_1_0_0 import (
    Payload as RegpSync100Payload,
)
from gwatn.types.ps_regprices_gnode.r_regp_sync.r_regp_sync_1_0_0 import (
    R_Regp_Sync_1_0_0,
)


# Message payloads for message protocols sent


DB_FILE = "src/satn/dev_utils/price/forecast_data/ps_db.sqlite3"


def csv_file_by_uid(price_uid: str) -> str:
    db_file = DB_FILE
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cmd = f"SELECT file_name FROM csv_file_by_key WHERE type_name = 'csv.regp.sync.1_0_0' AND price_uid = '{price_uid}'"
    rows = cursor.execute(cmd).fetchall()
    if len(rows) == 0:
        raise Exception(
            f"PriceUid {price_uid} is not associated with a csv.regp.sync.1_0_0 message!!"
        )
        # TODO: turn this into sending back an error message
    cursor.close()
    db.close()
    file = rows[0][0]
    return file


def payload_from_file(
    regp_type_name: str,
    regp_csv: str,
    flo_start_utc: datetime.datetime,
    flo_total_time_hrs: int,
) -> RegpSync100Payload:
    if regp_type_name == "csv.regp.sync.1_0_0":
        try:
            orig_csv = Csv_Regp_Sync_1_0_0(reg_price_csv=regp_csv).payload
        except FileNotFoundError:
            raise Exception(f"Cannot find price file {regp_csv}!")
    else:
        raise Exception(f"Does not handle TypeName {regp_type_name}")
    uniform_slice_duration_hrs = orig_csv.UniformSliceDurationHrs
    total_slices = int(flo_total_time_hrs / uniform_slice_duration_hrs)

    req = R_Gnode_Regp_Sync_Req_1_0_0(
        agent=test_dummy.TEST_DUMMY_AGENT,
        to_g_node_alias=test_dummy.TEST_DUMMY_G_NODE_ALIAS,
        p_node_alias=orig_csv.PNodeAlias,
        method_alias=orig_csv.MethodAlias,
        start_utc=flo_start_utc,
        uniform_slice_duration_hrs=orig_csv.UniformSliceDurationHrs,
        total_slices=total_slices,
        timezone_string=orig_csv.TimezoneString,
        currency_unit=orig_csv.CurrencyUnit,
    ).payload

    payload = regp_sync_100_paired_request(req=req, agent=test_dummy.TEST_DUMMY_AGENT)
    return payload


def regp_sync_100_paired_request(
    req: RGnodeRegpSyncReq100Payload, agent
) -> RegpSync100Payload:
    uniform_slice_duration_hrs = req.UniformSliceDurationHrs
    total_slices = req.TotalSlices
    slice_duration_hr_string = f"[{uniform_slice_duration_hrs}] * {total_slices}"
    db_file = DB_FILE
    db = sqlite3.connect(db_file)
    cursor = db.cursor()

    cmd = (
        f"SELECT price_uid FROM regp_sync_100 WHERE "
        f"p_node_alias = '{req.PNodeAlias}' AND "
        f"start_year_utc = {req.StartYearUtc} AND "
        f"start_month_utc = {req.StartMonthUtc} AND "
        f"start_day_utc = {req.StartDayUtc} AND "
        f"start_hour_utc = {req.StartHourUtc} AND "
        f"start_minute_utc = {req.StartMinuteUtc} AND "
        f"method_alias = '{req.MethodAlias}' AND "
        f"currency_unit = '{req.CurrencyUnit}' AND "
        f"slice_duration_hrs = '{slice_duration_hr_string}'"
    )

    rows = cursor.execute(cmd).fetchall()
    cursor.close()
    db.close()
    if len(rows) == 0:
        file = create_new_regp_sync_100_and_return_filename(req)
    else:
        price_uid = rows[0][0]
        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        cmd = f"SELECT file_name FROM csv_file_by_key WHERE type_name = 'csv.regp.sync.100' AND price_uid = '{price_uid}'"
        rows = cursor.execute(cmd).fetchall()
        if len(rows) == 0:
            raise Exception(
                f"PriceUid {price_uid} is in table regp_sync_100 but no match in csv_file_by_key!!"
            )
        cursor.close()
        db.close()
        file = rows[0][0]
    payload = Csv_Regp_Sync_1_0_0(file).paired_rabbit_payload(agent=agent)
    is_valid, errors = payload.is_valid()
    if not is_valid:
        raise SchemaError(f"Errors making payload: {errors}")
    return payload


def create_new_regp_sync_100_and_return_filename(
    req: RGnodeRegpSyncReq100Payload,
) -> str:
    flo_start = pendulum.datetime(
        year=req.StartYearUtc,
        month=req.StartMonthUtc,
        day=req.StartDayUtc,
        hour=req.StartHourUtc,
        minute=req.StartMinuteUtc,
    )
    prices = []
    comment = ""
    while len(prices) < req.TotalSlices:
        orig_length = len(prices)
        prices, new_comment = get_expanded_prices_and_comment(prices=prices, req=req)
        if len(prices) == orig_length:
            raise Exception(
                f"No source file for reg prices after {len(prices)} slices with PNodeAlias {req.PNodeAlias}, MethodAlias {req.MethodAlias}, CurrencyUnit {req.CurrencyUnit} with flo starting {flo_start}') "
            )
        comment += new_comment
        if len(prices) == 0:
            raise Exception(f"No source price data found")

    new = R_Regp_Sync_1_0_0(
        agent=test_dummy.TEST_DUMMY_AGENT,
        p_node_alias=req.PNodeAlias,
        method_alias=req.MethodAlias,
        comment=comment,
        start_utc=flo_start,
        uniform_slice_duration_hrs=req.UniformSliceDurationHrs,
        timezone_string=req.TimezoneString,
        currency_unit=req.CurrencyUnit,
        price_uid=str(uuid.uuid4()),
        prices=prices,
    ).payload

    slice_duration_hr_string = f"[{new.UniformSliceDurationHrs}] * {len(new.Prices)}"
    new_file = create_new_regp_sync_csv_from_payload(c=new)
    db_file = "src/satn/dev_utils/price/forecast_data/ps_db.sqlite3"
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cmd = f"INSERT INTO regp_sync_100 (price_uid, p_node_alias, start_year_utc, start_month_utc, start_day_utc, start_hour_utc, start_minute_utc, method_alias, currency_unit, slice_duration_hrs) VALUES ('{new.PriceUid}','{new.PNodeAlias}',{new.StartYearUtc},{new.StartMonthUtc},{new.StartDayUtc},{new.StartHourUtc},{new.StartMinuteUtc},'{new.MethodAlias}', '{new.CurrencyUnit}','{slice_duration_hr_string}')"
    cursor.execute(cmd)
    cmd = f"INSERT INTO csv_file_by_key (price_uid, type_name, file_name) VALUES ('{new.PriceUid}','csv.regp.sync.1_0_0','{new_file}')"
    cursor.execute(cmd)
    db.commit()
    cursor.close()
    db.close()
    return new_file


def create_new_regp_sync_csv_from_payload(c: RegpSync100Payload):
    iso = c.PNodeAlias.split(".")[1]
    uid_pre = c.PriceUid.split("-")[0]
    hours = int(c.UniformSliceDurationHrs * len(c.Prices))
    file = f"src/satn/dev_utils/price/forecast_data/{iso}/regp__{c.PNodeAlias}__{c.StartYearUtc}__{hours}__{c.MethodAlias}__{uid_pre}.csv"
    print(f"Creating new reg price file {file}")
    lines = [
        f"MpAlias,csv.regp.sync.1_0_0\n",
        f"PNodeAlias,{c.PNodeAlias}\n",
        f"MethodAlias,{c.MethodAlias}\n",
        f"Comment,{c.Comment}\n",
        f"StartYearUtc,{c.StartYearUtc}\n",
        f"StartMonthUtc,{c.StartMonthUtc}\n",
        f"StartDayUtc,{c.StartDayUtc}\n",
        f"StartHourUtc,{c.StartHourUtc}\n",
        f"StartMinuteUtc,{c.StartMinuteUtc}\n",
        f"UniformSliceDurationHrs,{c.UniformSliceDurationHrs}\n",
        f"TimezoneString,{c.TimezoneString}\n",
        f"CurrencyUnit,{c.CurrencyUnit}\n",
        f"PriceUid,{c.PriceUid}\n",
        f"Header,Regulation Price (Currency Unit/MWh)\n",
    ]
    for price in c.Prices:
        lines.append(f"{price}\n")
    with open(file, "w") as outfile:
        outfile.writelines(lines)
    return file


def get_expanded_prices_and_comment(prices: list, req: RGnodeRegpSyncReq100Payload):
    regp_source_file_by_uid = price_source_files.get_regp_sync_source_file_by_uid()
    flo_start_utc = pendulum.datetime(
        year=req.StartYearUtc,
        month=req.StartMonthUtc,
        day=req.StartDayUtc,
        hour=req.StartHourUtc,
        minute=req.StartMinuteUtc,
    )
    flo_end = flo_start_utc + pendulum.duration(
        hours=req.TotalSlices * req.UniformSliceDurationHrs
    )
    marker_time = flo_start_utc + pendulum.duration(
        hours=len(prices) * req.UniformSliceDurationHrs
    )
    db_file = "src/satn/dev_utils/price/forecast_data/ps_db.sqlite3"
    db = sqlite3.connect(db_file)
    cursor = db.cursor()

    cmd = (
        f"SELECT price_uid FROM regp_sync_100 WHERE p_node_alias = '{req.PNodeAlias}' AND "
        f"method_alias = '{req.MethodAlias}' AND "
        f"currency_unit = '{req.CurrencyUnit}'"
    )

    rows = cursor.execute(cmd).fetchall()
    cursor.close()
    db.close()
    price_uids = list(
        filter(lambda x: x in regp_source_file_by_uid.keys(), map(lambda x: x[0], rows))
    )
    if len(price_uids) == 0:
        raise Exception(
            f"That is strange. No price source file matches PNodeAlias {req.PNodeAlias}, MethodAlias {req.MethodAlias}, CurrencyUnit {req.CurrencyUnit}"
        )

    candidate_start = {}
    candidate_final_slice_start = {}
    slice_d = {}
    for uid in price_uids:
        file = f"../gridworks-ps/{regp_source_file_by_uid[uid]}"
        c = Csv_Regp_Sync_1_0_0(file).payload
        csv_start_utc = pendulum.datetime(
            year=c.StartYearUtc,
            month=c.StartMonthUtc,
            day=c.StartDayUtc,
            hour=c.StartHourUtc,
            minute=c.StartMinuteUtc,
        )
        candidate_start[uid] = csv_start_utc
        candidate_final_slice_start[uid] = csv_start_utc + pendulum.duration(
            hours=c.UniformSliceDurationHrs * (len(c.Prices) - 1)
        )
        slice_d[uid] = c.UniformSliceDurationHrs
    price_uids = list(
        filter(
            lambda x: candidate_start[x] <= marker_time
            and slice_d[x] == req.UniformSliceDurationHrs,
            price_uids,
        )
    )
    if len(price_uids) == 0:
        raise Exception(
            f"No source file for reg prices with PNodeAlias {req.PNodeAlias}, MethodAlias {req.MethodAlias}, CurrencyUnit {req.CurrencyUnit} with flo starting {flo_start_utc}"
        )

    best_uid = max(price_uids, key=lambda x: candidate_final_slice_start[x] - flo_end)
    if candidate_final_slice_start[best_uid] < flo_start_utc:
        raise Exception(
            f"No source file for reg prices with PNodeAlias {req.PNodeAlias}, MethodAlias {req.MethodAlias}, CurrencyUnit {req.CurrencyUnit} with flo starting {flo_start_utc}"
        )

    file = f"../gridworks-ps/{regp_source_file_by_uid[best_uid]}"

    c = Csv_Regp_Sync_1_0_0(file).payload

    offset_row = int(
        (flo_start_utc - candidate_start[best_uid]).total_seconds()
        / 3600
        / c.UniformSliceDurationHrs
    )
    if marker_time > candidate_final_slice_start[best_uid]:
        can_add_value = False
    else:
        can_add_value = True

    i = offset_row
    while can_add_value:
        prices.append(c.Prices[i])
        marker_time += pendulum.duration(hours=c.UniformSliceDurationHrs)
        i += 1
        if (
            marker_time > candidate_final_slice_start[best_uid]
            or len(prices) >= req.TotalSlices
        ):
            can_add_value = False
    comment = f"Used {i - offset_row} slices from {regp_source_file_by_uid[best_uid]}"
    return prices, comment
