import csv
import os
import sqlite3

import gridworks.property_format as property_format
import pendulum
from gridworks.data_classes.market_type import Da60
from gridworks.data_classes.market_type import MarketType
from gridworks.data_classes.market_type import Rt15Gate5
from gridworks.data_classes.market_type import Rt60Gate5
from gridworks.data_classes.market_type import Rt60Gate30

from gwatn.enums.hack_price_method import PriceMethod
from gwatn.types.ps_electricityprices_gnode.csv_epda_actual.csv_epda_actual_1_0_0 import (
    Csv_Epda_Actual_1_0_0,
)
from gwatn.types.ps_electricityprices_gnode.csv_eprt_actual.csv_eprt_actual_1_0_0 import (
    Csv_Eprt_Actual_1_0_0,
)


os.system("cd src/satn/dev_utils/price/actual_data && python init_actual_prices_db.py")

DEFAULT_DB_FILE = "src/satn/dev_utils/price/actual_data/actual_price_db.sqlite3"
ROOT_INPUT_DIR = "../gridworks-ps/input_data/electricity_prices"


def main(
    root_input_dir=ROOT_INPUT_DIR,
    db_file=DEFAULT_DB_FILE,
):
    price_files = []
    for subdir, dirs, files in os.walk(root_input_dir):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".csv"):
                price_files.append(filepath)

    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    print(f"Updating actual prices in {db_file}")
    for price_file in price_files:
        with open(price_file) as csv_file:
            reader = csv.reader(csv_file)
            type_name = next(reader)[1].strip()
            if (
                type_name == "csv.eprt.actual.1_0_0"
                or type_name == "csv.epda.actual.1_0_0"
            ):
                if type_name == "csv.eprt.actual.1_0_0":
                    core = Csv_Eprt_Actual_1_0_0(price_file).payload.Core
                    if core.MethodAlias in [PriceMethod.ERCOT_RTM60_APIZIP.value]:
                        market_type = Rt60Gate5
                    elif core.MethodAlias in [
                        PriceMethod.ISONEEXPRESS_FINALRT_HR_WEB.value
                    ]:
                        market_type = Rt60Gate30
                    elif core.MethodAlias in [PriceMethod.ERCOT_RTM15_APIZIP.value]:
                        market_type = Rt15Gate5
                    else:
                        raise Exception(
                            f"Does not know how to assign real time market type to method alias {core.MethodAlias}"
                        )
                elif type_name == "csv.epda.actual.1_0_0":
                    core = Csv_Epda_Actual_1_0_0(price_file).payload.Core
                    if core.MethodAlias in [
                        PriceMethod.ERCOT_DAM60_APIZIP.value,
                        PriceMethod.ISONEEXPRESS_DA_WEB.value,
                    ]:
                        market_type = Da60
                    else:
                        raise Exception(
                            f"Does not know how to assign DA market type to method alias {core.MethodAlias}"
                        )
                market_alias = f"{market_type.name.value}.{core.PNodeAlias}"
                try:
                    property_format.check_is_market_name(market_alias)
                except ValueError as e:
                    raise Exception(
                        f"{market_alias} is not a properly formatted market alias. See property_format.is_market_alias_lrd_format"
                    )
                first_market_slot_start_utc = pendulum.parse(
                    core.FirstMarketSlotStartIso8601Utc
                )
                first_market_slot_start_s = first_market_slot_start_utc.int_timestamp
                for i in range(len(core.Prices)):
                    market_slot_start_s = (
                        first_market_slot_start_s
                        + i * market_type.duration_minutes * 60
                    )
                    market_slot_alias = f"{market_alias}.{market_slot_start_s}"
                    try:
                        property_format.check_is_market_slot_name_lrd_format(
                            market_slot_alias
                        )
                    except ValueError as e:
                        raise Exception(
                            f"{market_slot_alias} is not a property formatted market slot alias. See property_format.is_market_slot_alias_lrd_format"
                        )
                    cmd = f"INSERT INTO market_price (market_slot_alias, value, price_unit) values ('{market_slot_alias}',{core.Prices[i]}, '{market_type.price_unit}')"
                    try:
                        cursor.execute(cmd)
                        db.commit()
                    except sqlite3.IntegrityError:
                        # print(f"Duplicate price for market slot {market_slot_alias}, start time {pendulum.from_timestamp(market_slot_start_s)}. Ignoring")
                        pass

    db.close()
