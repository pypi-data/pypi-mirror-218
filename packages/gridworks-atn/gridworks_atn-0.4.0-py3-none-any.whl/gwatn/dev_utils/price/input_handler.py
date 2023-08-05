import pendulum

from gwatn.types.ps_electricityprices_gnode.csv_eprt_sync.csv_eprt_sync_1_0_0 import (
    Csv_Eprt_Sync_1_0_0,
)


USD_PER_GBP = 1.38


def get_flo_starttime_from_eprt_csv(
    rt_price_type_name, rt_price_csv, csv_starting_offset_hours
):
    if rt_price_type_name == "csv.eprt.sync.1_0_0":
        try:
            rt_elec_price_payload = Csv_Eprt_Sync_1_0_0(
                real_time_electricity_price_csv=rt_price_csv
            ).payload
        except FileNotFoundError:
            raise Exception(f"Cannot find price file {rt_price_csv}!")
    else:
        raise Exception(f"Does not handle TypeName {rt_price_type_name}")

    utc_csv_start = pendulum.datetime(
        rt_elec_price_payload.StartYearUtc,
        rt_elec_price_payload.StartMonthUtc,
        rt_elec_price_payload.StartDayUtc,
        rt_elec_price_payload.StartHourUtc,
        rt_elec_price_payload.StartMinuteUtc,
        0,
    )
    flo_start_datetime_utc = utc_csv_start + pendulum.duration(
        hours=csv_starting_offset_hours
    )
    return flo_start_datetime_utc
