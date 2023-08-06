import osmnx as ox
from shapely.geometry import LineString, Point
import geopandas as gpd
import numpy as np
import keplergl
import random
import pandas as pd


def visualise_route(dataset, height=400):
    """
    Creates a DataFrame of evenly spaced points from an randomised origins to destinations in a graph network.

    Parameters:
            dataset : DataFrame
                DataFrame containing a geometry column of Shapely Points and IDs
            height : int
                Height of the output map

    Returns:
            map : KeplerGL visualisation
    """

    # Checking if all relevant columns exist
    assert "geometry" in dataset.columns, "'geometry' column not found."
    assert "time" in dataset.columns, "'time' column not found."

    # Checking data types in columns are correct
    for geometry in dataset["geometry"]:
        assert isinstance(geometry, Point), f"Invalid geometry type: {type(geometry)}"

    # Setting up a map
    map = keplergl.KeplerGl(height=height)
    # Adding the data points to the map
    map.add_data(data=dataset, name="Route Points")

    return map


def generate_route(
    Gp, start_time, origin_node, destination_node, walk_speed=1.4, frequency="30s"
):
    """
    Creates a DataFrame of evenly spaced points from an origin to a destination in a graph network.

    Parameters:
            Gp : MultiDiGraph
                Graph network representing a geographic network of routes
            start_time : str
                Starting time at the origin point of the route
                Example: '2015-02-26 21:00:00'
            origin_node : int
                Node ID from OpenStreetMap
            destination_node : int
                Node ID from OpenStreetMap
            walk_speed : float
                Walking speed measured in meters per second
            frequency: str
                Time interval for sampling location points along a route

    Returns:
            gdf (DataFrame): Shapely Points with continuous timestamps along a route
    """

    # Find the shortest path between origin and destination
    route = ox.distance.shortest_path(
        Gp, origin_node, destination_node, weight="length", cpus=1
    )

    # Find the nodes along the shortest route
    nodes = ox.graph_to_gdfs(Gp, nodes=True, edges=False)
    route_nodes = nodes.loc[route]

    # Convert the CRS so route length is in meters
    gdf = gpd.GeoDataFrame(route_nodes, geometry="geometry", crs=4326)
    gdf = gdf.to_crs(epsg=3857)

    # Converting points to a LineString
    route_line = LineString(gdf["geometry"].tolist())
    # Creating an array of even spacing
    distances = np.arange(0, route_line.length, walk_speed)
    # Interpolate evenly spaced points along the LineString
    points = [route_line.interpolate(distance) for distance in distances]
    # Convert to a GeoDataFrame
    gdf = gpd.GeoDataFrame(geometry=points, crs=3857)
    # Add a continuous timestamp to each point along the route
    try:
        gdf["time"] = pd.date_range(start_time, freq=frequency, periods=len(gdf))
    except AssertionError:
        print(
            "Was unable to create a time range, please check either the timestamp and frequency is in a correct format."
        )
        exit(1)
    return gdf


def generate_routes(
    Gp,
    time_from,
    time_until=None,
    time_strategy="fixed",
    route_strategy="many-many",
    origin_destination_coords=None,
    total_routes=1,
    walk_speed=1.4,
    frequency="1s",
):
    """
    Creates a DataFrame of evenly spaced points from an randomised origins to destinations in a graph network.

    Parameters:
            Gp : MultiDiGraph
                Graph network representing a geographic network of routes
            time_from : str
                Timestamp of the earliest start time possible
                Example: '2015-02-26 21:00:00'
            time_until : str
                Timestamp of the latest start time possible
                Example: '2015-02-26 22:00:00'
            time_strategy : str
                Determines whether the route start time is fixed or randomised. If randomised, also requires 'time_until' to be defined
            route_strategy : str
                Determines fixed or randomised origin and destination locations. Options are 'many-many', 'one-one', 'one-many', 'many-one'
            total_routes : int
                Total number of individual routes
                Example: 5
            origin_destination_coords : list
                Coordinates in EPSG:4326 used if the route_strategy is 'one-one', 'one-many', 'many-one' either for defining the origin or destination
                Example : [51.499127, -0.153522, 51.498523, -0.155438] when route_strategy is 'one-one'
            walk_speed : float
                Walking speed measured in meters per second
                Example : 1.4
            frequency : str
                Time interval for sampling location points along a route
                Example : '30s'
    Returns:
            df (DataFrame): Shapely Points with continuous timestamps along a multiple routes
    """
    # Checking there is more than one node in the network
    assert len(list(Gp.nodes)) != 1, "Graph network only contains one node."

    # Checking total routes is greater than 0
    assert (
        total_routes > 0
    ), f"Total number of routes should be 1 or more. Currently set as {total_routes}."
    # Checking walk_speed is greater than 0
    assert (
        walk_speed > 0
    ), f"walk_speed needs to be greater than 0. Currently set as {walk_speed}."

    # Creating an empty list
    route_dfs = []

    for i in range(total_routes):
        # Checking theres a valid time_strategy
        assert time_strategy in [
            "random",
            "fixed",
        ], "Invalid input, available inputs are 'random' or 'fixed'."
        # Checking theres a valid route_strategy
        assert route_strategy in [
            "many-many",
            "one-one",
            "one-many",
            "many-one",
        ], "Invalid input, available inputs are 'many-many', 'one-one', 'one-many', 'many-one."

        if route_strategy == "many-many":
            # Selecting random origin and destination nodes from the graph
            origin_node = list(Gp.nodes)[random.randint(0, len(list(Gp.nodes)))]
            destination_node = list(Gp.nodes)[random.randint(0, len(list(Gp.nodes)))]
        elif route_strategy == "one-one":
            # Checking fixed coordinates are defined
            assert (
                origin_destination_coords != None
            ), "No origin or destination coordinates specified."
            # Checking all required origin/destination coordinates are present
            assert (
                len(origin_destination_coords) == 4
            ), "Invalid number of coordinates. Coordinates should follow the scheme [origin_lon, origin_lat, dest_lon, dest_lat]"

            # Selecting predefined origin and destination nodes from the graph
            origin_node = ox.nearest_nodes(
                Gp, origin_destination_coords[1], origin_destination_coords[0]
            )
            destination_node = ox.nearest_nodes(
                Gp, origin_destination_coords[3], origin_destination_coords[2]
            )
        elif route_strategy == "one-many":
            # Checking fixed coordinates are defined
            assert origin_destination_coords != None, "No origin coordinates specified."
            # Checking all required origin/destination coordinates are present
            assert (
                len(origin_destination_coords) == 2
            ), "Invalid number of coordinates. Coordinates should follow the scheme [origin_lon, origin_lat]"

            # Selecting predefined origin and destination nodes from the graph
            origin_node = ox.nearest_nodes(
                Gp, origin_destination_coords[1], origin_destination_coords[0]
            )
            destination_node = list(Gp.nodes)[random.randint(0, len(list(Gp.nodes)))]
        elif route_strategy == "many-one":
            # Checking fixed coordinates are defined
            assert (
                origin_destination_coords != None
            ), "No destination coordinates specified."
            # Checking all required origin/destination coordinates are present
            assert (
                len(origin_destination_coords) == 2
            ), "Invalid number of coordinates. Coordinates should follow the scheme [destination_lon, destination_lat]"

            # Selecting predefined origin and destination nodes from the graph
            origin_node = list(Gp.nodes)[random.randint(0, len(list(Gp.nodes)))]
            destination_node = ox.nearest_nodes(
                Gp, origin_destination_coords[1], origin_destination_coords[0]
            )

        if time_strategy == "fixed":
            # Convert strings to datetime
            time = pd.to_datetime(time_from)
        else:
            # Check that a time_until exists
            assert (
                time_until != None
            ), "No time_until is specified, which is required when using a 'random' time_strategy."

            # Convert strings to datetime
            time_from = pd.to_datetime(time_from)
            time_until = pd.to_datetime(time_until)

            # Check that time_until is after time_from
            assert time_from < time_until, "time_until is earlier than time_from."

            # Create a random start time
            time = time_from + (time_until - time_from) * random.random()

        # Use the generate_route function to output a route
        route = generate_route(
            Gp, time, origin_node, destination_node, walk_speed, frequency
        )
        # Add a route ID
        route["id"] = i + 1
        # Append back to the list
        route_dfs.append(route)
    # Concatenate list elements into a DataFrame
    df = pd.concat(route_dfs, ignore_index=True)

    return df
