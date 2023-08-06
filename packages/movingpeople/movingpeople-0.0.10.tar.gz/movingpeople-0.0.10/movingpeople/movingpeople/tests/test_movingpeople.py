import osmnx as ox
from shapely.geometry import LineString, Point
import geopandas as gpd
import numpy as np
import keplergl
import random
import pandas as pd

import unittest
from ..src import (
    generate_route,
    generate_routes,
    visualise_route,
)

# Search query for a geographic area
query = "City of Westminster"
# Get the walking network for the query location
G = ox.graph.graph_from_place(query, network_type="walk", simplify=True)
# Project the graph to WGS84
Gp = ox.project_graph(G, to_crs="4326")


class TestUniqueRoutes(unittest.TestCase):
    def test_(self):
        # To make two randomised routes
        two_routes = generate_routes(
                                    Gp,
                                    time_from="2015-02-26 21:42:53",
                                    time_until=None,
                                    time_strategy="fixed",
                                    route_strategy="many-many",
                                    origin_destination_coords=None,
                                    total_routes=2,
                                    walk_speed=1.4,
                                    frequency="1s",
                                    )
        # Unique number of route ids should equal 2
        self.assertEqual(two_routes['id'].nunique(), 2, "incorrect number of unique ids")
