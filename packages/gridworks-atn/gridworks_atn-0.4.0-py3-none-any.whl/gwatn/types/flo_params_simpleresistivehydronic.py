"""Type flo.params.simpleresistivehydronic, version 000"""
import json
from enum import auto
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from fastapi_utils.enums import StrEnum
from gridworks.errors import SchemaError
from gridworks.message import as_enum
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from gwatn.enums import DistributionTariff
from gwatn.enums import EnergySupplyType
from gwatn.enums import RecognizedCurrencyUnit


class DistributionTariff000SchemaEnum:
    enum_name: str = "distribution.tariff.000"
    symbols: List[str] = [
        "00000000",
        "2127aba6",
        "ea5c675a",
        "54aec3a7",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class DistributionTariff000(StrEnum):
    Unknown = auto()
    VersantA1StorageHeatTariff = auto()
    VersantATariff = auto()
    VersantA20HeatTariff = auto()

    @classmethod
    def default(cls) -> "DistributionTariff000":
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class DistributionTariffMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> DistributionTariff:
        if not DistributionTariff000SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to DistributionTariff000 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, DistributionTariff, DistributionTariff.default())

    @classmethod
    def local_to_type(cls, distribution_tariff: DistributionTariff) -> str:
        if not isinstance(distribution_tariff, DistributionTariff):
            raise SchemaError(
                f"{distribution_tariff} must be of type {DistributionTariff}"
            )
        versioned_enum = as_enum(
            distribution_tariff, DistributionTariff000, DistributionTariff000.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, DistributionTariff000] = {
        "00000000": DistributionTariff000.Unknown,
        "2127aba6": DistributionTariff000.VersantA1StorageHeatTariff,
        "ea5c675a": DistributionTariff000.VersantATariff,
        "54aec3a7": DistributionTariff000.VersantA20HeatTariff,
    }

    versioned_enum_to_type_dict: Dict[DistributionTariff000, str] = {
        DistributionTariff000.Unknown: "00000000",
        DistributionTariff000.VersantA1StorageHeatTariff: "2127aba6",
        DistributionTariff000.VersantATariff: "ea5c675a",
        DistributionTariff000.VersantA20HeatTariff: "54aec3a7",
    }


class RecognizedCurrencyUnit000SchemaEnum:
    enum_name: str = "recognized.currency.unit.000"
    symbols: List[str] = [
        "00000000",
        "e57c5143",
        "f7b38fc5",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class RecognizedCurrencyUnit000(StrEnum):
    UNKNOWN = auto()
    USD = auto()
    GBP = auto()

    @classmethod
    def default(cls) -> "RecognizedCurrencyUnit000":
        return cls.UNKNOWN

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class RecognizedCurrencyUnitMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> RecognizedCurrencyUnit:
        if not RecognizedCurrencyUnit000SchemaEnum.is_symbol(symbol):
            raise SchemaError(
                f"{symbol} must belong to RecognizedCurrencyUnit000 symbols"
            )
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(
            versioned_enum, RecognizedCurrencyUnit, RecognizedCurrencyUnit.default()
        )

    @classmethod
    def local_to_type(cls, recognized_currency_unit: RecognizedCurrencyUnit) -> str:
        if not isinstance(recognized_currency_unit, RecognizedCurrencyUnit):
            raise SchemaError(
                f"{recognized_currency_unit} must be of type {RecognizedCurrencyUnit}"
            )
        versioned_enum = as_enum(
            recognized_currency_unit,
            RecognizedCurrencyUnit000,
            RecognizedCurrencyUnit000.default(),
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, RecognizedCurrencyUnit000] = {
        "00000000": RecognizedCurrencyUnit000.UNKNOWN,
        "e57c5143": RecognizedCurrencyUnit000.USD,
        "f7b38fc5": RecognizedCurrencyUnit000.GBP,
    }

    versioned_enum_to_type_dict: Dict[RecognizedCurrencyUnit000, str] = {
        RecognizedCurrencyUnit000.UNKNOWN: "00000000",
        RecognizedCurrencyUnit000.USD: "e57c5143",
        RecognizedCurrencyUnit000.GBP: "f7b38fc5",
    }


class EnergySupplyType000SchemaEnum:
    enum_name: str = "energy.supply.type.000"
    symbols: List[str] = [
        "00000000",
        "cb18f937",
        "e9dc99a6",
    ]

    @classmethod
    def is_symbol(cls, candidate: str) -> bool:
        if candidate in cls.symbols:
            return True
        return False


class EnergySupplyType000(StrEnum):
    Unknown = auto()
    StandardOffer = auto()
    RealtimeLocalLmp = auto()

    @classmethod
    def default(cls) -> "EnergySupplyType000":
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        return [elt.value for elt in cls]


class EnergySupplyTypeMap:
    @classmethod
    def type_to_local(cls, symbol: str) -> EnergySupplyType:
        if not EnergySupplyType000SchemaEnum.is_symbol(symbol):
            raise SchemaError(f"{symbol} must belong to EnergySupplyType000 symbols")
        versioned_enum = cls.type_to_versioned_enum_dict[symbol]
        return as_enum(versioned_enum, EnergySupplyType, EnergySupplyType.default())

    @classmethod
    def local_to_type(cls, energy_supply_type: EnergySupplyType) -> str:
        if not isinstance(energy_supply_type, EnergySupplyType):
            raise SchemaError(
                f"{energy_supply_type} must be of type {EnergySupplyType}"
            )
        versioned_enum = as_enum(
            energy_supply_type, EnergySupplyType000, EnergySupplyType000.default()
        )
        return cls.versioned_enum_to_type_dict[versioned_enum]

    type_to_versioned_enum_dict: Dict[str, EnergySupplyType000] = {
        "00000000": EnergySupplyType000.Unknown,
        "cb18f937": EnergySupplyType000.StandardOffer,
        "e9dc99a6": EnergySupplyType000.RealtimeLocalLmp,
    }

    versioned_enum_to_type_dict: Dict[EnergySupplyType000, str] = {
        EnergySupplyType000.Unknown: "00000000",
        EnergySupplyType000.StandardOffer: "cb18f937",
        EnergySupplyType000.RealtimeLocalLmp: "e9dc99a6",
    }


def check_is_uuid_canonical_textual(v: str) -> None:
    """
    UuidCanonicalTextual format:  A string of hex words separated by hyphens
    of length 8-4-4-4-12.

    Raises:
        ValueError: if not UuidCanonicalTextual format
    """
    try:
        x = v.split("-")
    except AttributeError as e:
        raise ValueError(f"Failed to split on -: {e}")
    if len(x) != 5:
        raise ValueError(f"{v} split by '-' did not have 5 words")
    for hex_word in x:
        try:
            int(hex_word, 16)
        except ValueError:
            raise ValueError(f"Words of {v} are not all hex")
    if len(x[0]) != 8:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[1]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[2]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[3]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[4]) != 12:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")


def check_is_left_right_dot(v: str) -> None:
    """
    LeftRightDot format: Lowercase alphanumeric words separated by periods,
    most significant word (on the left) starting with an alphabet character.

    Raises:
        ValueError: if not LeftRightDot format
    """
    from typing import List

    try:
        x: List[str] = v.split(".")
    except:
        raise ValueError(f"Failed to seperate {v} into words with split'.'")
    first_word = x[0]
    first_char = first_word[0]
    if not first_char.isalpha():
        raise ValueError(f"Most significant word of {v} must start with alphabet char.")
    for word in x:
        if not word.isalnum():
            raise ValueError(f"words of {v} split by by '.' must be alphanumeric.")
    if not v.islower():
        raise ValueError(f"All characters of {v} must be lowercase.")


class FloParamsSimpleresistivehydronic(BaseModel):
    """ """

    GNodeAlias: str = Field(
        title="GNodeAlias",
    )
    FloParamsUid: str = Field(
        title="FloParamsUid",
    )
    HomeCity: str = Field(
        title="HomeCity",
        default="MILLINOCKET_ME",
    )
    TimezoneString: str = Field(
        title="TimezoneString",
        default="US/Eastern",
    )
    StartYearUtc: int = Field(
        title="StartYearUtc",
        default=2020,
    )
    StartMonthUtc: int = Field(
        title="StartMonthUtc",
        default=1,
    )
    StartDayUtc: int = Field(
        title="StartDayUtc",
        default=1,
    )
    StartHourUtc: int = Field(
        title="StartHourUtc",
        default=0,
    )
    StartMinuteUtc: int = Field(
        title="StartMinuteUtc",
        default=0,
    )
    StorageSteps: int = Field(
        title="StorageSteps",
        default=100,
    )
    StoreSizeGallons: int = Field(
        title="StoreSizeGallons",
        default=240,
    )
    MaxStoreTempF: int = Field(
        title="MaxStoreTempF",
        default=210,
    )
    RatedPowerKw: float = Field(
        title="RatedPowerKw",
        default=9.5,
    )
    RequiredSourceWaterTempF: int = Field(
        title="RequiredSourceWaterTempF",
        default=120,
    )
    CirculatorPumpGpm: float = Field(
        title="CirculatorPumpGpm",
        default=4.5,
    )
    ReturnWaterDeltaTempF: int = Field(
        title="ReturnWaterDeltaTempF",
        default=20,
    )
    RoomTempF: int = Field(
        title="RoomTempF",
        default=70,
    )
    AmbientPowerInKw: float = Field(
        title="AmbientPowerInKw",
        default=1.2,
    )
    HouseWorstCaseTempF: float = Field(
        title="HouseWorstCaseTempF",
        default=-7,
    )
    StorePassiveLossRatio: float = Field(
        title="StorePassiveLossRatio",
        default=0.005,
    )
    PowerLostFromHouseKwList: List[float] = Field(
        title="PowerLostFromHouseKwList",
        default=[3.42],
    )
    AmbientTempStoreF: int = Field(
        title="AmbientTempStoreF",
        default=65,
    )
    SliceDurationMinutes: List[int] = Field(
        title="SliceDurationMinutes",
        default=[60],
    )
    RealtimeElectricityPrice: List[float] = Field(
        title="RealtimeElectricityPrice",
        default=[10.35],
    )
    DistributionPrice: List[float] = Field(
        title="DistributionPrice",
        default=[40.0],
    )
    OutsideTempF: List[float] = Field(
        title="OutsideTempF",
        default=[-5.1],
    )
    RtElecPriceUid: str = Field(
        title="RtElecPriceUid",
    )
    DistPriceUid: str = Field(
        title="DistPriceUid",
    )
    WeatherUid: str = Field(
        title="WeatherUid",
    )
    CurrencyUnit: RecognizedCurrencyUnit = Field(
        title="CurrencyUnit",
        default=RecognizedCurrencyUnit.USD,
    )
    Tariff: DistributionTariff = Field(
        title="Tariff",
        default=DistributionTariff.VersantA1StorageHeatTariff,
    )
    EnergyType: EnergySupplyType = Field(
        title="EnergyType",
        default=EnergySupplyType.RealtimeLocalLmp,
    )
    StandardOfferPriceDollarsPerMwh: int = Field(
        title="StandardOfferPriceDollarsPerMwh",
        default=110,
    )
    FlatDistributionTariffDollarsPerMwh: int = Field(
        title="FlatDistributionTariffDollarsPerMwh",
        default=113,
    )
    StartingStoreIdx: int = Field(
        title="StartingStoreIdx",
        default=50,
    )
    TypeName: Literal[
        "flo.params.simpleresistivehydronic"
    ] = "flo.params.simpleresistivehydronic"
    Version: str = "000"

    @validator("GNodeAlias")
    def _check_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(f"GNodeAlias failed LeftRightDot format validation: {e}")
        return v

    @validator("FloParamsUid")
    def _check_flo_params_uid(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"FloParamsUid failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("RtElecPriceUid")
    def _check_rt_elec_price_uid(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"RtElecPriceUid failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("DistPriceUid")
    def _check_dist_price_uid(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"DistPriceUid failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("WeatherUid")
    def _check_weather_uid(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"WeatherUid failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("CurrencyUnit")
    def _check_currency_unit(cls, v: RecognizedCurrencyUnit) -> RecognizedCurrencyUnit:
        return as_enum(v, RecognizedCurrencyUnit, RecognizedCurrencyUnit.UNKNOWN)

    @validator("Tariff")
    def _check_tariff(cls, v: DistributionTariff) -> DistributionTariff:
        return as_enum(v, DistributionTariff, DistributionTariff.Unknown)

    @validator("EnergyType")
    def _check_energy_type(cls, v: EnergySupplyType) -> EnergySupplyType:
        return as_enum(v, EnergySupplyType, EnergySupplyType.Unknown)

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        del d["CurrencyUnit"]
        CurrencyUnit = as_enum(
            self.CurrencyUnit, RecognizedCurrencyUnit, RecognizedCurrencyUnit.default()
        )
        d["CurrencyUnitGtEnumSymbol"] = RecognizedCurrencyUnitMap.local_to_type(
            CurrencyUnit
        )
        del d["Tariff"]
        Tariff = as_enum(self.Tariff, DistributionTariff, DistributionTariff.default())
        d["TariffGtEnumSymbol"] = DistributionTariffMap.local_to_type(Tariff)
        del d["EnergyType"]
        EnergyType = as_enum(
            self.EnergyType, EnergySupplyType, EnergySupplyType.default()
        )
        d["EnergyTypeGtEnumSymbol"] = EnergySupplyTypeMap.local_to_type(EnergyType)
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa


class FloParamsSimpleresistivehydronic_Maker:
    type_name = "flo.params.simpleresistivehydronic"
    version = "000"

    def __init__(
        self,
        g_node_alias: str,
        flo_params_uid: str,
        home_city: str,
        timezone_string: str,
        start_year_utc: int,
        start_month_utc: int,
        start_day_utc: int,
        start_hour_utc: int,
        start_minute_utc: int,
        storage_steps: int,
        store_size_gallons: int,
        max_store_temp_f: int,
        rated_power_kw: float,
        required_source_water_temp_f: int,
        circulator_pump_gpm: float,
        return_water_delta_temp_f: int,
        room_temp_f: int,
        ambient_power_in_kw: float,
        house_worst_case_temp_f: float,
        store_passive_loss_ratio: float,
        power_lost_from_house_kw_list: List[float],
        ambient_temp_store_f: int,
        slice_duration_minutes: List[int],
        realtime_electricity_price: List[float],
        distribution_price: List[float],
        outside_temp_f: List[float],
        rt_elec_price_uid: str,
        dist_price_uid: str,
        weather_uid: str,
        currency_unit: RecognizedCurrencyUnit,
        tariff: DistributionTariff,
        energy_type: EnergySupplyType,
        standard_offer_price_dollars_per_mwh: int,
        flat_distribution_tariff_dollars_per_mwh: int,
        starting_store_idx: int,
    ):
        self.tuple = FloParamsSimpleresistivehydronic(
            GNodeAlias=g_node_alias,
            FloParamsUid=flo_params_uid,
            HomeCity=home_city,
            TimezoneString=timezone_string,
            StartYearUtc=start_year_utc,
            StartMonthUtc=start_month_utc,
            StartDayUtc=start_day_utc,
            StartHourUtc=start_hour_utc,
            StartMinuteUtc=start_minute_utc,
            StorageSteps=storage_steps,
            StoreSizeGallons=store_size_gallons,
            MaxStoreTempF=max_store_temp_f,
            RatedPowerKw=rated_power_kw,
            RequiredSourceWaterTempF=required_source_water_temp_f,
            CirculatorPumpGpm=circulator_pump_gpm,
            ReturnWaterDeltaTempF=return_water_delta_temp_f,
            RoomTempF=room_temp_f,
            AmbientPowerInKw=ambient_power_in_kw,
            HouseWorstCaseTempF=house_worst_case_temp_f,
            StorePassiveLossRatio=store_passive_loss_ratio,
            PowerLostFromHouseKwList=power_lost_from_house_kw_list,
            AmbientTempStoreF=ambient_temp_store_f,
            SliceDurationMinutes=slice_duration_minutes,
            RealtimeElectricityPrice=realtime_electricity_price,
            DistributionPrice=distribution_price,
            OutsideTempF=outside_temp_f,
            RtElecPriceUid=rt_elec_price_uid,
            DistPriceUid=dist_price_uid,
            WeatherUid=weather_uid,
            CurrencyUnit=currency_unit,
            Tariff=tariff,
            EnergyType=energy_type,
            StandardOfferPriceDollarsPerMwh=standard_offer_price_dollars_per_mwh,
            FlatDistributionTariffDollarsPerMwh=flat_distribution_tariff_dollars_per_mwh,
            StartingStoreIdx=starting_store_idx,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: FloParamsSimpleresistivehydronic) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> FloParamsSimpleresistivehydronic:
        """
        Given a serialized JSON type object, returns the Python class object
        """
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> FloParamsSimpleresistivehydronic:
        d2 = dict(d)
        if "GNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing GNodeAlias")
        if "FloParamsUid" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FloParamsUid")
        if "HomeCity" not in d2.keys():
            raise SchemaError(f"dict {d2} missing HomeCity")
        if "TimezoneString" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TimezoneString")
        if "StartYearUtc" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartYearUtc")
        if "StartMonthUtc" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartMonthUtc")
        if "StartDayUtc" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartDayUtc")
        if "StartHourUtc" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartHourUtc")
        if "StartMinuteUtc" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartMinuteUtc")
        if "StorageSteps" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StorageSteps")
        if "StoreSizeGallons" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StoreSizeGallons")
        if "MaxStoreTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing MaxStoreTempF")
        if "RatedPowerKw" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RatedPowerKw")
        if "RequiredSourceWaterTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RequiredSourceWaterTempF")
        if "CirculatorPumpGpm" not in d2.keys():
            raise SchemaError(f"dict {d2} missing CirculatorPumpGpm")
        if "ReturnWaterDeltaTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ReturnWaterDeltaTempF")
        if "RoomTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RoomTempF")
        if "AmbientPowerInKw" not in d2.keys():
            raise SchemaError(f"dict {d2} missing AmbientPowerInKw")
        if "HouseWorstCaseTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing HouseWorstCaseTempF")
        if "StorePassiveLossRatio" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StorePassiveLossRatio")
        if "PowerLostFromHouseKwList" not in d2.keys():
            raise SchemaError(f"dict {d2} missing PowerLostFromHouseKwList")
        if "AmbientTempStoreF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing AmbientTempStoreF")
        if "SliceDurationMinutes" not in d2.keys():
            raise SchemaError(f"dict {d2} missing SliceDurationMinutes")
        if "RealtimeElectricityPrice" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RealtimeElectricityPrice")
        if "DistributionPrice" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DistributionPrice")
        if "OutsideTempF" not in d2.keys():
            raise SchemaError(f"dict {d2} missing OutsideTempF")
        if "RtElecPriceUid" not in d2.keys():
            raise SchemaError(f"dict {d2} missing RtElecPriceUid")
        if "DistPriceUid" not in d2.keys():
            raise SchemaError(f"dict {d2} missing DistPriceUid")
        if "WeatherUid" not in d2.keys():
            raise SchemaError(f"dict {d2} missing WeatherUid")
        if "CurrencyUnitGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing CurrencyUnitGtEnumSymbol")
        if (
            d2["CurrencyUnitGtEnumSymbol"]
            in RecognizedCurrencyUnit000SchemaEnum.symbols
        ):
            d2["CurrencyUnit"] = RecognizedCurrencyUnitMap.type_to_local(
                d2["CurrencyUnitGtEnumSymbol"]
            )
        else:
            d2["CurrencyUnit"] = RecognizedCurrencyUnit.default()
        if "TariffGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TariffGtEnumSymbol")
        if d2["TariffGtEnumSymbol"] in DistributionTariff000SchemaEnum.symbols:
            d2["Tariff"] = DistributionTariffMap.type_to_local(d2["TariffGtEnumSymbol"])
        else:
            d2["Tariff"] = DistributionTariff.default()
        if "EnergyTypeGtEnumSymbol" not in d2.keys():
            raise SchemaError(f"dict {d2} missing EnergyTypeGtEnumSymbol")
        if d2["EnergyTypeGtEnumSymbol"] in EnergySupplyType000SchemaEnum.symbols:
            d2["EnergyType"] = EnergySupplyTypeMap.type_to_local(
                d2["EnergyTypeGtEnumSymbol"]
            )
        else:
            d2["EnergyType"] = EnergySupplyType.default()
        if "StandardOfferPriceDollarsPerMwh" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StandardOfferPriceDollarsPerMwh")
        if "FlatDistributionTariffDollarsPerMwh" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FlatDistributionTariffDollarsPerMwh")
        if "StartingStoreIdx" not in d2.keys():
            raise SchemaError(f"dict {d2} missing StartingStoreIdx")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return FloParamsSimpleresistivehydronic(
            GNodeAlias=d2["GNodeAlias"],
            FloParamsUid=d2["FloParamsUid"],
            HomeCity=d2["HomeCity"],
            TimezoneString=d2["TimezoneString"],
            StartYearUtc=d2["StartYearUtc"],
            StartMonthUtc=d2["StartMonthUtc"],
            StartDayUtc=d2["StartDayUtc"],
            StartHourUtc=d2["StartHourUtc"],
            StartMinuteUtc=d2["StartMinuteUtc"],
            StorageSteps=d2["StorageSteps"],
            StoreSizeGallons=d2["StoreSizeGallons"],
            MaxStoreTempF=d2["MaxStoreTempF"],
            RatedPowerKw=d2["RatedPowerKw"],
            RequiredSourceWaterTempF=d2["RequiredSourceWaterTempF"],
            CirculatorPumpGpm=d2["CirculatorPumpGpm"],
            ReturnWaterDeltaTempF=d2["ReturnWaterDeltaTempF"],
            RoomTempF=d2["RoomTempF"],
            AmbientPowerInKw=d2["AmbientPowerInKw"],
            HouseWorstCaseTempF=d2["HouseWorstCaseTempF"],
            StorePassiveLossRatio=d2["StorePassiveLossRatio"],
            PowerLostFromHouseKwList=d2["PowerLostFromHouseKwList"],
            AmbientTempStoreF=d2["AmbientTempStoreF"],
            SliceDurationMinutes=d2["SliceDurationMinutes"],
            RealtimeElectricityPrice=d2["RealtimeElectricityPrice"],
            DistributionPrice=d2["DistributionPrice"],
            OutsideTempF=d2["OutsideTempF"],
            RtElecPriceUid=d2["RtElecPriceUid"],
            DistPriceUid=d2["DistPriceUid"],
            WeatherUid=d2["WeatherUid"],
            CurrencyUnit=d2["CurrencyUnit"],
            Tariff=d2["Tariff"],
            EnergyType=d2["EnergyType"],
            StandardOfferPriceDollarsPerMwh=d2["StandardOfferPriceDollarsPerMwh"],
            FlatDistributionTariffDollarsPerMwh=d2[
                "FlatDistributionTariffDollarsPerMwh"
            ],
            StartingStoreIdx=d2["StartingStoreIdx"],
            TypeName=d2["TypeName"],
            Version="000",
        )
