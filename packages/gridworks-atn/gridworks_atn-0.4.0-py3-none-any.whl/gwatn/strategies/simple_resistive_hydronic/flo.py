# type: ignore
import math
import random
import time
from typing import Dict
from typing import List
from typing import Optional
from typing import no_type_check

import gridworks.conversion_factors as cf
import numpy as np
import pendulum

import gwatn.strategies.simple_resistive_hydronic.flo_utils as flo_utils
from gwatn.data_classes.d_graph import DGraph
from gwatn.strategies.simple_resistive_hydronic.edge import (
    Edge_SimpleResistiveHydronic as Edge,
)
from gwatn.strategies.simple_resistive_hydronic.node import (
    Node_SimpleResistiveHydronic as Node,
)
from gwatn.types import FloParamsSimpleresistivehydronic


class Flo_SimpleResistiveHydronic(DGraph):
    MAGIC_HEAT_PUMP_DELTA_F = 20
    FAILED_HEATING_PENALTY_DOLLARS = 10**6

    def __init__(
        self,
        params: FloParamsSimpleresistivehydronic,
        d_graph_id: str,
    ):
        """

        Args:
            params:
            d_graph_id:
        """
        self.toast = 1
        self.params: FloParamsSimpleresistivehydronic = params
        self.RealtimeElectricityPrice = np.array(self.params.RealtimeElectricityPrice)
        self.DistributionPrice = np.array(self.params.DistributionPrice)

        self.max_energy_kwh = flo_utils.get_max_energy_kwh(self.params)

        self.currency_unit = self.params.CurrencyUnit
        DGraph.__init__(
            self,
            d_graph_id=d_graph_id,
            graph_strategy_alias="SimpleResistiveHydronic",
            flo_start_unix_time_s=pendulum.datetime(
                year=self.params.StartYearUtc,
                month=self.params.StartMonthUtc,
                day=self.params.StartDayUtc,
                hour=self.params.StartHourUtc,
                minute=self.params.StartMinuteUtc,
            ).timestamp(),
            slice_duration_hrs=list(np.array(self.params.SliceDurationMinutes) / 60),
            default_storage_steps=self.params.StorageSteps,
            starting_store_idx=self.params.StartingStoreIdx,
            timezone_string=self.params.TimezoneString,
            home_city=self.params.HomeCity,
            currency_unit=self.params.CurrencyUnit,
            max_storage=self.max_energy_kwh,
            max_power_in=self.params.RatedPowerKw,
            wh_exponent=3,
        )
        # Override base class dictionaries with SimpleResistiveHydronic objects
        self.node: Dict[int, Dict[int, Node]] = {}
        """
        self.node is a dictionary representing the nodes in the graph.

        The dictionary structure is as follows:
        - The outer dictionary's keys represent the time slice index (jj).
        - The inner dictionary's keys represent the energy index (kk).
        - The corresponding value is the node with the given time slice index (jj) and energy index (kk).

        Example usage: self.node[jj][kk] returns the node with time slice index jj and energy index kk.
        """

        self.edge: Dict[int, Dict[int, Dict[int, Edge]]] = {}
        """
        self.edge is a dictionary representing the edges in the graph. Each edge is an object
        determined by its starting timeslice index (start_ts_idx), its starting store index
        (start_idx) and its ending store index (end_idx)

        The dictionary structure as follows:
        - The first key represents the starting timeslice index
        - The second key represents the starting store index
        - The third key represents the final store index

        Example usage: self.edge[ts_idx][start_idx][end_idx] returns the edge starting at the node
        with time slice index start_ts_idx and store index start_idx, and ending with the node
        with time slice index start_ts_idx + 1 and store end_idx.
        """

        self.best_edge: Dict[Node, Edge] = {}
        """
        self.best_edge[node] is the optimal edge choice going forward from node.

        That is, its a dictionary mapping each node to the best next edge on the least-cost path
        going forward to the end of the graph from that node. This dictionary is filled out in the
        `solve_dijkstra` method, as the key step in using Dijkstra's algorithm, which solves
        for the least-cost path not only for the starting node but for all nodes in the graph.
        """

        self.e_step_wh: float = 1000 * self.max_energy_kwh / self.params.StorageSteps
        """
        The increment of energy, in watt-hours, associated to incrementing the store index by 1.
        """
        self.energy_cost_per_kwh: Dict[int, float] = {}
        self.set_energy_cost_per_kwh()
        self.uncosted_edges: Dict[
            Edge, int
        ] = {}  # using dict keys instead of list for faster searching

        self.create_graph()
        self.solve_dijkstra()

    def create_slice_nodes(self, ts_idx: int) -> None:
        """
        Create slice nodes for a given timeslice index.

        This function creates and initializes slice nodes for a specific timeslice index.
        Each slice node represents a storage step and stores the energy at that step in Wh.

        Args:
            ts_idx (int): The timeslice index.

        Returns:
            None

        Note:
            The created slice nodes are stored in the `node` attribute of the object.
        """
        self.node[ts_idx] = {}
        for store_idx in range(self.params.StorageSteps + 1):
            new_node = Node(
                ts_idx=ts_idx,
                store_idx=store_idx,
                energy_wh=store_idx * self.e_step_wh,
            )
            self.node[ts_idx][store_idx] = new_node

    def create_nodes(self) -> None:
        for ts_idx in range(self.time_slices + 1):
            self.create_slice_nodes(ts_idx)

    def set_energy_cost_per_kwh(self):
        for ts_idx in range(self.time_slices):
            self.energy_cost_per_kwh[ts_idx] = self.get_energy_cost_per_kwh(ts_idx)

    ######################################################
    # Functions of edges
    ######################################################

    # Cost related

    def get_energy_cost_per_kwh(self, ts_idx: int) -> float:
        energy_cost_per_mwh = self.params.RealtimeElectricityPrice[ts_idx]
        dist_cost_per_mwh = self.params.DistributionPrice[ts_idx]

        cost_per_mwh = energy_cost_per_mwh + dist_cost_per_mwh
        return cost_per_mwh / 1000

    ######################################################
    # Functions of edges - Water temp related
    #####################################################

    def set_failed_edge_properties(self, edge: Edge):
        """Set costs"""
        edge.cost = self.FAILED_HEATING_PENALTY_DOLLARS
        edge.hp_electricity_avg_kw = 10000
        edge.avg_kw = 0

    def get_failed_edge(self, node: Node) -> Edge:
        edge = Edge(
            start_ts_idx=node.ts_idx, start_idx=node.store_idx, end_idx=node.store_idx
        )
        self.set_failed_edge_properties(edge)
        return edge

    def create_uncosted_edges_from_node(self, node: Node) -> None:
        """Creates edges starting at a node."""
        edges: List[Edge] = []
        self.edge[node.ts_idx][node.store_idx] = {}

        slice_hrs = self.params.SliceDurationMinutes[node.ts_idx] / 60
        requested_energy_wh = (
            self.params.PowerLostFromHouseKwList[node.ts_idx] * 1000 * slice_hrs
        )
        passive_loss_wh = flo_utils.get_passive_loss_wh(
            self.params, node.ts_idx, node.store_idx
        )
        real_next_e_min_wh = node.energy_wh - requested_energy_wh - passive_loss_wh

        # note this is clearly an idealization. For example, in the summer when it is hot
        # and there is no need for heat, our model shows the tank staying at return water temp
        # with no passive loss.
        idealized_next_e_min_wh = max(0.0, real_next_e_min_wh)

        real_next_e_max_wh = (
            node.energy_wh
            + self.params.RatedPowerKw * 1000
            - requested_energy_wh
            - passive_loss_wh
        )
        real_next_e_max_wh = min(real_next_e_max_wh, self.max_energy_kwh * 1000)
        idealized_next_e_max_wh = max(0.0, real_next_e_max_wh)

        min_next_idx = round(idealized_next_e_min_wh / self.e_step_wh)
        max_next_idx = round(idealized_next_e_max_wh / self.e_step_wh)

        if min_next_idx > max_next_idx:
            raise Exception(f"Conceptual error in get_uncosted_edges_from_node! Fix!!")

        for i in range(min_next_idx, max_next_idx + 1):
            edge = Edge(
                start_ts_idx=node.ts_idx,
                start_idx=node.store_idx,
                end_idx=i,
            )
            self.uncosted_edges[edge] = 1
            self.edge[node.ts_idx][node.store_idx][i] = edge

    def create_uncosted_edges(self):
        for jj in range(self.time_slices):
            # if jj % 500 == 0:
            #     print(f"{time.time() - st:1.0f} seconds for {jj} slices")
            self.edge[jj] = {}
            for node in self.node[jj].values():
                self.create_uncosted_edges_from_node(node=node)

    def set_edge_cost(self, edge: Edge) -> None:
        """Given an edge:
        - set the edge cost to the cost of electricity required to buy the amount of electricity
         needed to meet the heating requests of the house following this edge
        """
        node = self.node[edge.start_ts_idx][edge.start_idx]
        slice_hrs = self.params.SliceDurationMinutes[node.ts_idx] / 60
        requested_energy_wh = (
            self.params.PowerLostFromHouseKwList[node.ts_idx] * 1000 * slice_hrs
        )
        passive_loss_wh = flo_utils.get_passive_loss_wh(
            self.params, node.ts_idx, node.store_idx
        )

        delta_store_wh = (edge.end_idx - edge.start_idx) * self.e_step_wh

        boost_e_used_wh = delta_store_wh + requested_energy_wh + passive_loss_wh
        if boost_e_used_wh < -self.e_step_wh / 2:
            raise Exception(
                f"Trouble with edge {edge}! boost energy {round(boost_e_used_wh / 1000,2)} kW "
                f"is less than 0 by more than half an e step {round(self.e_step_wh / 2, 2)} kW."
            )

        boost_e_used_kwh = boost_e_used_wh / 1000

        edge.cost = boost_e_used_kwh * self.energy_cost_per_kwh[edge.start_ts_idx]
        edge.avg_kw = boost_e_used_kwh / slice_hrs

    def add_all_edge_costs(self) -> None:
        for edge in self.uncosted_edges.keys():
            self.set_edge_cost(edge)
        self.uncosted_edges = {}

    def create_graph(self) -> None:
        # print(f"Creating graph nodes, edges and edge weights")
        st = time.time()
        self.create_nodes()
        nt = time.time()
        # print(f"{time.time() - st:1.0f} seconds to make nodes")
        self.create_uncosted_edges()
        et = time.time()
        # print(f"{et - nt:1.0f} seconds for building edges")
        self.add_all_edge_costs()
        ct = time.time()
        # print(f"{ct - et:1.0f} seconds for costing edges")
        tt = time.time() - st
        # print(f"time per 100 slices:{tt*100000/self.time_slices:2.0f} ms ")
        # print(f"total time to build graph: {tt:2.0f} s")
        # print(f"Total number of slices: {self.time_slices}")
