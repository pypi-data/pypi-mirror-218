import datetime
import sqlite3
import uuid

import gwprice.dev_utils.price_source_files as price_source_files
import pendulum

import gwatn.types.hack_test_dummy as test_dummy
from gwatn.errors import SchemaError
from gwatn.types.gnode_distprequest_ps.r_gnode_distp_sync_req.r_gnode_distp_sync_req_1_0_0 import (
    Payload as RGnodeDistpSyncRec100Payload,
)
from gwatn.types.gnode_distprequest_ps.r_gnode_distp_sync_req.r_gnode_distp_sync_req_1_0_0 import (
    R_Gnode_Distp_Sync_Req_1_0_0,
)
from gwatn.types.ps_distprices_gnode.csv_distp_oneprice.csv_distp_oneprice_1_0_0 import (
    Csv_Distp_Oneprice_1_0_0,
)

# MessageMakers for reading eprt (electricity price real time) from csvs
from gwatn.types.ps_distprices_gnode.csv_distp_sync.csv_distp_sync_1_0_0 import (
    Csv_Distp_Sync_1_0_0,
)

# Message Payloads for message protocols sent by this strategy
from gwatn.types.ps_distprices_gnode.r_distp_sync.r_distp_sync_1_0_0 import (
    Payload as DistpSync100Payload,
)
from gwatn.types.ps_distprices_gnode.r_distp_sync.r_distp_sync_1_0_0 import (
    R_Distp_Sync_1_0_0,
)


# Message Payloads for messages received


DB_FILE = "src/satn/dev_utils/price/forecast_data/ps_db.sqlite3"


def csv_file_by_uid(price_uid: str) -> str:
    db_file = DB_FILE
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cmd = f"SELECT file_name FROM csv_file_by_key WHERE type_name = 'csv.distp.sync.1_0_0' AND price_uid = '{price_uid}'"
    rows = cursor.execute(cmd).fetchall()
    if len(rows) == 0:
        raise Exception(
            f"PriceUid {price_uid} is not associated with a csv.distp.sync.1_0_0 message!!"
        )

        # TODO: turn this into sending back an error message
    cursor.close()
    db.close()
    file = rows[0][0]
    return file


def payload_from_file(
    distp_type_name: str,
    distp_csv: str,
    flo_start_utc: datetime.datetime,
    flo_total_time_hrs: int,
) -> DistpSync100Payload:
    if distp_type_name == "csv.distp.sync.1_0_0":
        try:
            orig_csv = Csv_Distp_Sync_1_0_0(
                distp_electricity_price_csv=distp_csv
            ).payload
        except FileNotFoundError:
            raise Exception(f"Cannot find price file {distp_csv}!")
    else:
        raise Exception(f"Does not handle TypeName {distp_type_name}")

    uniform_slice_duration_hrs = orig_csv.UniformSliceDurationHrs
    total_slices = int(flo_total_time_hrs / uniform_slice_duration_hrs)

    req = R_Gnode_Distp_Sync_Req_1_0_0(
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

    return distp_sync_100_paired_request(req=req, agent=test_dummy.TEST_DUMMY_AGENT)


def distp_sync_100_paired_request(
    req: RGnodeDistpSyncRec100Payload, agent
) -> DistpSync100Payload:
    uniform_slice_duration_hrs = req.UniformSliceDurationHrs
    total_slices = req.TotalSlices
    slice_duration_hr_string = f"[{uniform_slice_duration_hrs}] * {total_slices}"
    db_file = DB_FILE
    db = sqlite3.connect(db_file)
    cursor = db.cursor()

    cmd = (
        f"SELECT price_uid FROM distp_sync_100 WHERE "
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
        file = create_new_distp_sync_100_and_return_filename(req)
    else:
        price_uid = rows[0][0]
        db = sqlite3.connect(db_file)
        cursor = db.cursor()
        cmd = f"SELECT file_name FROM csv_file_by_key WHERE type_name = 'csv.distp.sync.1_0_0' AND price_uid = '{price_uid}'"
        rows = cursor.execute(cmd).fetchall()
        if len(rows) == 0:
            raise Exception(
                f"PriceUid {price_uid} is in table distp_sync_100 but not csv_file_by_key!!"
            )
        cursor.close()
        db.close()
        file = rows[0][0]

    payload = Csv_Distp_Sync_1_0_0(file).paired_rabbit_payload(agent=agent)
    is_valid, errors = payload.is_valid()
    if not is_valid:
        raise SchemaError(f"Errors making payload: {errors}")

    return payload


def create_new_distp_sync_100_and_return_filename(
    req: RGnodeDistpSyncRec100Payload,
) -> str:
    start_utc = pendulum.datetime(
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
                f"No source file for reg prices after {len(prices)} slices with PNodeAlias {req.PNodeAlias}, MethodAlias {req.MethodAlias}, CurrencyUnit {req.CurrencyUnit} with flo starting {start_utc}') "
            )
        comment += new_comment
        if len(prices) == 0:
            raise Exception(f"No source price data found")

    new = R_Distp_Sync_1_0_0(
        agent=test_dummy.TEST_DUMMY_AGENT,
        p_node_alias=req.PNodeAlias,
        method_alias=req.MethodAlias,
        comment=comment,
        start_utc=start_utc,
        uniform_slice_duration_hrs=req.UniformSliceDurationHrs,
        timezone_string=req.TimezoneString,
        currency_unit=req.CurrencyUnit,
        prices=prices,
        price_uid=str(uuid.uuid4()),
    ).payload

    slice_duration_hr_string = f"[{new.UniformSliceDurationHrs}] * {len(new.Prices)}"
    new_file = create_new_distp_sync_csv_from_payload(c=new)
    db_file = "src/satn/dev_utils/price/forecast_data/ps_db.sqlite3"
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cmd = f"INSERT INTO distp_sync_100 (price_uid, p_node_alias, start_year_utc, start_month_utc, start_day_utc, start_hour_utc, start_minute_utc, method_alias, currency_unit, slice_duration_hrs) VALUES ('{new.PriceUid}','{new.PNodeAlias}',{new.StartYearUtc},{new.StartMonthUtc},{new.StartDayUtc},{new.StartHourUtc},{new.StartMinuteUtc},'{new.MethodAlias}', '{new.CurrencyUnit}','{slice_duration_hr_string}')"
    cursor.execute(cmd)
    cmd = f"INSERT INTO csv_file_by_key (price_uid, type_name, file_name)  VALUES ('{new.PriceUid}','csv.distp.sync.1_0_0','{new_file}')"
    cursor.execute(cmd)
    db.commit()
    cursor.close()
    db.close()
    return new_file


def create_new_distp_sync_csv_from_payload(c: DistpSync100Payload) -> str:
    iso = c.PNodeAlias.split(".")[1]
    uid_pre = c.PriceUid.split("-")[0]
    hours = int(c.UniformSliceDurationHrs * len(c.Prices))
    file = f"src/satn/dev_utils/price/forecast_data/{iso}/distp__{c.PNodeAlias}__{c.StartYearUtc}__{hours}__{c.MethodAlias}__{uid_pre}.csv"
    print(f"Creating new dist price file {file}")
    lines = [
        f"MpAlias,csv.distp.sync.1_0_0\n",
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
        f"Header, Distribution Electricity Price (Currency Unit/MWh)\n",
    ]
    for price in c.Prices:
        lines.append(f"{price}\n")
    with open(file, "w") as outfile:
        outfile.writelines(lines)
    return file


def get_expanded_prices_and_comment(prices: list, req: RGnodeDistpSyncRec100Payload):
    distp_sync_source_file_by_uid = (
        price_source_files.get_distp_sync_source_file_by_uid()
    )
    distp_oneprice_source_file_by_uid = (
        price_source_files.get_distp_oneprice_source_file_by_uid()
    )
    distp_source_file_by_uid = {
        **distp_sync_source_file_by_uid,
        **distp_oneprice_source_file_by_uid,
    }
    flo_start_utc = pendulum.datetime(
        year=req.StartYearUtc,
        month=req.StartMonthUtc,
        day=req.StartDayUtc,
        hour=req.StartHourUtc,
        minute=req.StartMinuteUtc,
    )
    flo_end_utc = flo_start_utc + pendulum.duration(
        hours=req.TotalSlices * req.UniformSliceDurationHrs
    )
    marker_time_utc = flo_start_utc + pendulum.duration(
        hours=len(prices) * req.UniformSliceDurationHrs
    )
    db_file = "src/satn/dev_utils/price/forecast_data/ps_db.sqlite3"
    db = sqlite3.connect(db_file)
    cursor = db.cursor()

    cmd = (
        f"SELECT price_uid FROM distp_sync_100 WHERE p_node_alias = '{req.PNodeAlias}' AND "
        f"method_alias = '{req.MethodAlias}' AND "
        f"currency_unit = '{req.CurrencyUnit}'"
    )

    rows = cursor.execute(cmd).fetchall()
    cursor.close()
    db.close()
    price_uids = list(
        filter(
            lambda x: x in distp_source_file_by_uid.keys(), map(lambda x: x[0], rows)
        )
    )
    if len(price_uids) == 0:
        raise Exception(
            f"That is strange. No price source file matches PNodeAlias {req.PNodeAlias}, MethodAlias {req.MethodAlias}, CurrencyUnit {req.CurrencyUnit}"
        )

    candidate_start = {}
    candidate_final_slice_start = {}
    slice_d = {}
    for uid in price_uids:
        file = f"../gridworks-ps/{distp_source_file_by_uid[uid]}"
        if uid in distp_sync_source_file_by_uid.keys():
            c = Csv_Distp_Sync_1_0_0(file).payload
            csv_start = pendulum.datetime(
                year=c.StartYearUtc,
                month=c.StartMonthUtc,
                day=c.StartDayUtc,
                hour=c.StartHourUtc,
                minute=c.StartMinuteUtc,
            )
            candidate_start[uid] = csv_start
            slice_d[uid] = c.UniformSliceDurationHrs
            candidate_final_slice_start[uid] = csv_start + pendulum.duration(
                hours=c.UniformSliceDurationHrs * (len(c.Prices) - 1)
            )
        elif uid in distp_oneprice_source_file_by_uid.keys():
            c = Csv_Distp_Oneprice_1_0_0(file).payload
            csv_start = pendulum.datetime(
                year=c.StartYearUtc,
                month=c.StartMonthUtc,
                day=c.StartDayUtc,
                hour=c.StartHourUtc,
                minute=c.StartMinuteUtc,
            )
            candidate_start[uid] = csv_start
            slice_d[uid] = c.UniformSliceDurationHrs
        else:
            raise Exception(
                "Strange. prices should be either distp.sync or distp.oneprice"
            )

    price_uids = list(
        filter(
            lambda x: candidate_start[x] <= marker_time_utc
            and slice_d[x] == req.UniformSliceDurationHrs,
            price_uids,
        )
    )
    if len(price_uids) == 0:
        raise Exception(
            f"No source file for distprice with PNodeAlias {req.PNodeAlias}, MethodAlias {req.MethodAlias}, CurrencyUnit {req.CurrencyUnit} with flo starting {flo_start_utc}"
        )

    good_oneprices = list(
        filter(lambda x: x in distp_oneprice_source_file_by_uid.keys(), price_uids)
    )
    if len(good_oneprices) > 0:
        best_uid = good_oneprices[0]
        c = Csv_Distp_Oneprice_1_0_0(distp_oneprice_source_file_by_uid[best_uid])
    else:
        price_uids = list(
            filter(lambda x: x in distp_sync_source_file_by_uid.keys(), price_uids)
        )
        best_uid = max(
            price_uids, key=lambda x: candidate_final_slice_start[x] - flo_end_utc
        )
        if candidate_final_slice_start[best_uid] < flo_start_utc:
            raise Exception(
                f"No source file for dist prices with PNodeAlias {req.PNodeAlias}, MethodAlias {req.MethodAlias}, CurrencyUnit {req.CurrencyUnit} with flo starting {flo_start_utc}"
            )

        file = f"../gridworks-ps/{distp_sync_source_file_by_uid[best_uid]}"
        c = Csv_Distp_Sync_1_0_0(file).payload

    offset_row = int(
        (flo_start_utc - candidate_start[best_uid]).total_seconds()
        / 3600
        / c.UniformSliceDurationHrs
    )
    if marker_time_utc > candidate_final_slice_start[best_uid]:
        can_add_value = False
    else:
        can_add_value = True
    i = offset_row
    while can_add_value:
        prices.append(c.Prices[i])
        marker_time_utc += pendulum.duration(hours=c.UniformSliceDurationHrs)
        i += 1
        if (
            marker_time_utc > candidate_final_slice_start[best_uid]
            or len(prices) >= req.TotalSlices
        ):
            can_add_value = False
    comment = f"Used {i - offset_row} slices from {distp_source_file_by_uid[best_uid]}"
    return prices, comment
