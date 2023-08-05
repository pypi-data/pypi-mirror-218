from gwatn import conversion_factors as cf
from gwatn.errors import PhysicalSystemFailure
from gwatn.types import FloParamsSimpleresistivehydronic


def get_max_energy_kwh(params: FloParamsSimpleresistivehydronic) -> float:
    """
    Calculates the maximum usable energy stored in the water tanks for a heating system modeled using
    the Simple Resistive Hydronic AtomicTNode strategy.

    This model assumes idealized stratification, where the water is in a single cylindrical tank
    and has two temperatures: a high temperature, `params.MaxStoreTempF`, and a low temperature,
    which is the return water temp (RWT) from the distribution system. There is a totally
    horizontal thermocline; that is, above a certain height in the tank all water is the max
    temp, and below that height all water is the return water temp.

    The state of maximum energy in the tank is when the entire tank is at the highest temperature.
    However, determining the amount of energy in kilowatt-hours (kWh) requires establishing a baseline
    energy level. In this calculation, the assumption is made that the baseline energy is the amount
    of energy the tank would contain if it were uniformly at the return water temp. This choice
    provides a reasonable approximation for the "zero energy" reference in this model.

    This model of a water tank heated by resistive elements is highly idealized.

    Args:
        params (FloParamsSimpleresistivehydronic): The parameters of the heating system. Specifically,
        it uses these attributes of a FloParamsSimpleresistivehydronic object:
        - StoreSizeGallons
        - MaxStoreTempF
        - RequiredSourceWaterTempF
        - ReturnWaterDeltaTempF
        This function can also be used with objects that can be duck-typed as `AtnParams`.

    Returns:
        float: The maximum usable energy stored in kilowatt-hours (kWh) in the water tanks.
    """
    return_water_temp_f = params.RequiredSourceWaterTempF - params.ReturnWaterDeltaTempF
    store_size_pounds = params.StoreSizeGallons * cf.POUNDS_OF_WATER_PER_GALLON

    # Calculate the maximum energy in btus
    # Original defn of a BTU: the amount of heat (energy) required to raise the temperature of one
    # pound of water by one degree Fahrenheit. https://en.wikipedia.org/wiki/British_thermal_unit
    max_energy_btu = store_size_pounds * (params.MaxStoreTempF - return_water_temp_f)

    # Calculate the maximum energy in kWh
    max_energy_kwh = max_energy_btu / cf.BTU_PER_KWH

    return max_energy_kwh


def get_max_system_heat_output_avg_kw(
    params: FloParamsSimpleresistivehydronic,
) -> float:
    """
    Calculates the maximum heat output attainable by a heating system  modeled using
    the Simple Resistive Hydronic AtomicTNode strategy.

    This calculation takes into account the parameters of the system, including the gallons per minute
    (gpm) of the circulator pump for the single-zone distribution system and the difference
    (delta_temp_f) between the source/supply water temperature (SWT) entering the distribution system
    and the return water temperature (RWT) coming back from the distribution system.

    Please note that this model assumes a constant speed for the circulator pump and a fixed temperature delta.
    It provides a reasonable estimate for understanding the mechanics of single-zone homes, but may not accurately
    model multi-zone homes or address all potential issues.

    Finally, note that this is not the same as the amount of heat that a house requires on the coldest
    day of a Typical Modeled Year.

    For more information on the Simple Resistive Hydronic model, please visit:
    - AtomicTNode Simple Resistive Hydronic model: [Params API](https://gridworks-atn.readthedocs.io/en/latest/simple-resistive-hydronic.html)
    - Params API: [FloParamsSimpleresistivehydronic](https://gridworks-atn.readthedocs.io/en/latest/types/flo-params-simpleresistivehydronic.html)


    Args:
        params (FloParamsSimpleresistivehydronic): The parameters of the heating system. Specifically:
            - CirculatorPumpGpm
            - ReturnWaterDeltaTempF

    Returns:
        float: The maximum heat output in kilowatts (kW) that the heating system can provide.

    """

    gpm = params.CirculatorPumpGpm
    pounds_per_hr = 60 * gpm * cf.POUNDS_OF_WATER_PER_GALLON
    delta_temp_f = params.ReturnWaterDeltaTempF

    # Original defn of a BTU: the amount of heat (energy) required to raise the temperature of one
    # pound of water by one degree Fahrenheit. https://en.wikipedia.org/wiki/British_thermal_unit
    #
    # note that many US HVAC tradespeople use this as the form of energy, instead of the SI units
    # of Joules or kWh.  There are 3412 BTUs per kWh - useful to memorize if you are paying attention
    # to electric heating.
    max_dist_system_btus_per_hour = pounds_per_hr * delta_temp_f
    max_dist_system_out_kw = max_dist_system_btus_per_hour / cf.BTU_PER_KWH

    design_day_kw = min(max_dist_system_out_kw, params.RatedPowerKw)

    return design_day_kw


def get_house_worst_case_heat_output_avg_kw(
    params: FloParamsSimpleresistivehydronic,
) -> float:
    worst_t = params.HouseWorstCaseTempF
    this_run_t = min(params.OutsideTempF)
    room_t = params.RoomTempF
    p = params.PowerLostFromHouseKwList
    this_run_max_system_kw = max(p)
    this_run_max_kw_in = this_run_max_system_kw + params.AmbientPowerInKw
    dd_max_kw_in = this_run_max_kw_in * (room_t - worst_t) / (room_t - this_run_t)
    return dd_max_kw_in - params.AmbientPowerInKw


# TODO: move into FloParams as an axiom.
def check_params_consistency(params: FloParamsSimpleresistivehydronic) -> None:
    """
    Checks if the heating system can meet the physical requirements of the house.

    If the house's worst-case heat requirement exceeds the maximum output of the system output, or if the required source water temperature is higher than the maximum store temperature, an exception
    of type PhysicalSystemFailure is raised.

    Args:
        params: An instance of FloParamsSimpleresistivehydronic containing the parameters for the heating system.

    Raises:
        PhysicalSystemFailure: If the house's worst-case heat requirement exceeds the maximum system output
                               or if the required source water temperature is higher than the maximum store temperature.
    """
    max_system_out = get_max_system_heat_output_avg_kw(params)
    max_house_out = get_house_worst_case_heat_output_avg_kw(params)

    if max_house_out > max_system_out:
        raise PhysicalSystemFailure(
            f"Max house requirement on worst case annual temp of "
            f"{params.HouseWorstCaseTempF}  "
            f"{round(max_house_out, 2)} kW exceeds max system "
            f"output of {round(max_system_out, 2)}"
        )

    this_run_lowest_ot = min(params.OutsideTempF)
    if this_run_lowest_ot < params.HouseWorstCaseTempF:
        raise ValueError(
            f"min outside temp {this_run_lowest_ot} F is lower than"
            f"House Worst Case Temp {params.HouseWorstCaseTempF} F!"
        )

    if params.RequiredSourceWaterTempF > params.MaxStoreTempF:
        raise PhysicalSystemFailure(
            f"Store temp cannot keep house warm! MaxStoreTempF is {params.MaxStoreTempF} F"
            f" and Required Source Water Temp is {params.RequiredSourceWaterTempF} F."
        )


def get_passive_loss_wh(
    params: FloParamsSimpleresistivehydronic, ts_idx: int, store_idx: int
) -> float:
    """
    Returns the loss of energy from the tank for a time slice due to radiating through the tank insulation,
    as a function of the starting node.

    A more accurate variant would provide passive loss as a function of an edge. However, given how small
    this loss typically is, this simplification is pretty insignificant compared to other inaccuracies
    of the model and we didn't think it was worth the additional complexity.

    Args:
        params:
        ts_idx
        store_idx:

    Returns:
        Energy lost passively from the tank through its insulation in the time slice,
        in Watt Hours.

    """
    slice_hrs = params.SliceDurationMinutes[ts_idx] / 60
    hot_ratio = store_idx / params.StorageSteps
    hot_pounds = hot_ratio * params.StoreSizeGallons * cf.POUNDS_OF_WATER_PER_GALLON
    hot_energy_wh = (
        (params.MaxStoreTempF - params.AmbientTempStoreF)
        * hot_pounds
        * 1000
        / cf.BTU_PER_KWH
    )
    hot_loss_wh = params.StorePassiveLossRatio * slice_hrs * hot_energy_wh

    rwt_pounds = (
        (1 - hot_ratio) * params.StoreSizeGallons * cf.POUNDS_OF_WATER_PER_GALLON
    )
    rwt_f = params.RequiredSourceWaterTempF - params.ReturnWaterDeltaTempF
    rwt_energy_wh = (
        (rwt_f - params.AmbientTempStoreF) * rwt_pounds * 1000 / cf.BTU_PER_KWH
    )
    rwt_loss_wh = params.StorePassiveLossRatio * slice_hrs * rwt_energy_wh

    passive_loss_wh = hot_loss_wh + rwt_loss_wh

    return passive_loss_wh
