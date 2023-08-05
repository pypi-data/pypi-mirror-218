""" SimpleResistiveHydronic DNode Definition
"""
from typing import Optional

from gwatn.data_classes.d_node import DNode


SIG_FIGS_FOR_OUTPUT = 6


class Node_SimpleResistiveHydronic(DNode):
    def __init__(
        self,
        ts_idx: int,
        store_idx: int,
        energy_wh: float,
    ):
        DNode.__init__(
            self,
            ts_idx=ts_idx,
            store_idx=store_idx,
        )
        self.energy_wh = energy_wh

    def __repr__(
        self,
    ) -> str:
        rep = f"DNode => TimeSliceIdx: {self.ts_idx}, StoreIdx: {self.store_idx}"
        if self.path_cost:
            rep += f", Path cost: ${round(self.path_cost, 3)}"
        if self.energy_wh:
            rep += f", Energy: {round(self.energy_wh / 1000, 2)} kWh"
        return rep
