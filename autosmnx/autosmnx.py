import osmnx as ox
from argparse import ArgumentParser
from pathlib import Path
import re
import sys
import datetime
import geopandas as gpd
import pandas as pd
from shapely.wkt import loads
import tqdm
import matplotlib.pyplot as plot
import os
from alive_progress import alive_bar; import time

# Success == 1
def arguments_init():
    import argparse
    # argument parser
    parser = argparse.ArgumentParser()

    # ver
    global ver
    ver = '0.4.0'

    # File argument
    parser.add_argument("--file", "-f", type=str, required=True)

    # Distance argument
    parser.add_argument("--distance", "-d", type=int, required=True)

    # Coordinates argument:
    parser.add_argument("--coordinates", "-c", nargs=2, type=float, required=False)

    # Output argument
    parser.add_argument("--output", "-o", type=str, required=True, help="the output file path")

    # Logger argument
    parser.add_argument("--log", "-L", type=str, help="toggle log mode")

    # Parse the arguments
    global args
    args = parser.parse_args()

    # Paths:
    # Define output path:
    global output_path
    output_path = args.output 

    # Define the file path
    global file_path
    file_path = str(args.file)

# Success == 0
# Logger:
def log_execution_count(filename):
    
    if not os.path.exists(filename):
        
        with open(filename, "w") as f:
            
            f.write("0")

    with open(filename, "r+") as f:
        
        count = int(f.read())
        f.seek(0)
        f.write(str(count + 1))

# define arg log check:
def truth_args(arg_truth=None):
    if os.path.exists(args.log):
        arg_truth = 1
    else:
        arg_truth = 0

def preprocessor():
 
    # Pass the file to the argument:
    file = gpd.read_file(args.file)

    # Preproccessing print:
    size = sys.getsizeof(file)
    kilo = size / 1024
    mega = kilo / 1024

    # Round mega:
    rounded_kilo = round(kilo, 1)
    rounded_mega = round(mega, 1)

    # Print the size of the file:
    print("Processing file of " + str(rounded_mega) + "MB in memory...")

    # Set the coordinate references
    file = gpd.GeoDataFrame.set_crs(file, crs="EPSG:4326")

    # df to file:
    global df
    df = file

    # to dataframe (this needs to be eliminated because it doubles the memory of the input!)
    global df_ex
    df_ex = pd.DataFrame(df)

    # define progress bar:
    global pbar
    pbar = tqdm.tqdm(total=len(df_ex), desc="Writing Plot")

    # log path:
    global log_path
    log_path = str(args.log)



def osmnx_loop():    
    # Loop over the rows in the dataframe
    for index, row in df.iterrows():

        # update the tqdm progress bar:
        pbar.update(1)

        # Get the geometry from the current row
        geometry = row['geometry']

        # Get the centroid of the geometry
        centroid = geometry.centroid

        # Get the latitude and longitude from the centroid
        lat = centroid.y
        lon = centroid.x

        distance = args.distance

        # Get the current time and format it as a string
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        # NODES
        
        # Error for no graph nodes in query:
        try:
        
            # Use OSMNX to get the network around the coordinates
            G = ox.graph_from_point((lat, lon), dist=distance, network_type='drive')
            G = ox.bearing.add_edge_bearings(G, precision=1)

        except:

            next

        # Download buildings:
        try:

            build = ox.geometries_from_point((lat, lon), tags={'building': True}, dist=distance)

        except:

            next

        # PARKS:
        # Download parks:
        try:

            leisure = ox.geometries_from_point((lat, lon), tags={'leisure': True}, dist=distance)

        except:

            next
    
        # Format parks:
        try:

            parks = leisure[leisure["leisure"].isin(["park","playground"])]

        except:

            next

        # WATERS:
        # Download natural water:

        try:
        
            water = ox.geometries_from_point((lat, lon), tags={"water": True}, dist=distance)
    
        except:
    
            next

        try:

            water2 = ox.geometries_from_point((lat, lon), tags={"waterway": True})
        
        except:

            next

        # Download seas:
        try:

            sea = ox.geometries_from_point((lat, lon), tags={"place": "sea"}, dist=distance)

        except:

            next

        # Wood: 
        try:

            wood = ox.geometries_from_point((lat, lon), tags={"natural": "wood"})
        
        except:

            next
        
        # Shrubs:
        try:
            
            shrub = ox.geometries_from_point((lat, lon), tags={"natural": "shrubbery"})
        
        except:

            next
        
        # Farmland:
        try:

            farmland = ox.geometries_from_point((lat, lon), tags={"landuse": "farmland"})
        
        except:

            next
        
        # Cemetary:
        try:

            cemetary = ox.geometries_from_point((lat, lon), tags={"landuse": "cemetary"})
        
        except:

            next

        # Commercial:
        try:

            commercial = ox.geometries_from_point((lat, lon), tags={"landuse": "commercial"})

        except:

            next
        

        # Municipality
        try:

            office = ox.geometries_from_point((lat, lon), tags={"office": True})

        except:

            next
        
        # Neighborhood
        try:

            residential = ox.geometries_from_point((lat, lon), tags={"landuse": "residential"})

        except:

            next
        
        # Railraod:
        try:

            railroad = ox.geometries_from_point((lat, lon), tags={"landuse": "railway"})

        except:

            next

        # Retail:        
        try:

            retail = ox.geometries_from_point((lat, lon), tags={"landuse" : "retail"})

        except:

            next
        
        # Industrial:
        try:

            industrial = ox.geometries_from_point((lat, lon), tags={"landuse": "industrial"})

        except:

            next
        
        # Military:
        try:

            military = ox.geometries_from_point((lat, lon), tags={"military": True})
        
        except:

            next
        
        # Railway:
        try:

            railway = ox.geometries_from_point((lat, lon), tags={"railway": True})

        except:

            next

        # Place:
        try:

            place = ox.geometries_from_point((lat, lon), tags={"place": True})

        except:

            next
        
        # The code for filtering the results will go here; 
        # likely to be a `def osm_filter` situation

        # Create figure and plot the graph:
        fig, ax = ox.plot_graph(G, save=False, show=False, edge_linewidth=2, edge_color='black', node_size=1, figsize=(100,100), bgcolor='white')

        # fig plot:

        # Conditional logic for layers:
    
        # Parks:
        if len(parks) >= 1:
        
            parks.plot(ax=ax, hatch='.', color='#89c4ba', zorder=-1)
    
        else:

            next

        # Buildings:
        if len(build) >= 1:
        
            build.plot(ax=ax, color='black', zorder=1, alpha=0.65)

        else:

            next
    
        # Water:
        if len(water) >= 1:

            water.plot(ax=ax, color="#d4f1f9", hatch='', zorder=-1)

        else:

            next

    
        # Seas:
        if len(sea) >= 1:

            sea.plot(ax=ax, color="#d4f1f9", zorder=-1)
    
        else:

            next

        # Wood:
        if len(wood) >= 1:

            wood.plot(ax=ax, color="#357c5e", hatch="o", zorder=-1, alpha=0.5)
        
        else:

            next

        # Shrub:
        if len(shrub) >= 1:

            shrub.plot(ax=ax, color="#54847b", hatch="o", zorder=-1, alpha=0.25)
        
        else:

            next
        
        # Farmland:
        if len(farmland) >= 1:

            farmland.plot(ax=ax, color="tan", hatch="o", zorder=-1, alpha=0.65)

        else:

            next

        # Cemetary:
        if len(cemetary) >= 1:

            cemetary.plot(ax=ax, color="gray", hatch='--', zorder=0, alpha=0.4)
        
        else:

            next
        
        # Commercial:
        if len(commercial) >= 1:

            commercial.plot(ax=ax, color="pink", zorder=-1, alpha=0.25)

        else:

            next

        # Residential:
        if len(residential) >= 1:

            residential.plot(ax=ax, color="gray", alpha=0.25)
        
        else:

            next

        # Retail:
        if len(retail) >= 1:

            retail.plot(ax=ax, color="#6699CC", alpha=0.25)

        else:

            next
        
        # Industrial:
        if len(industrial) >= 1:

            industrial.plot(ax=ax, color="#7c5e35", alpha=0.25)

        else:
            
            next

        # Office:
        if len(office) >= 1:

            office.plot(ax=ax, color="#818AA8")
        
        else:

            next
        
        # Military:
        if len(military) >= 1:

            military.plot(ax=ax, color="red", alpha=0.5)

        # Railway:
        if len(railway) >= 1:

            railroad.plot(ax=ax, color="green")
        
        else:

            next

        # Place:
        if len(place) >= 1:

            place.plot(ax=ax, color="gray", alpha=0.1, zorder=-1)

        else:

            next
        
        # Water2:
        if len(water2) >= 1:

            water2.plot(ax=ax, color="#d4f1f9")

        else:

            next
            
        # // maybe define administration layer for argument in -cli call?
        # define location name:
        location_name = row['ADM3_EN']

        # Add a text annotation to the graph with the location name
        ax.annotate(location_name, xy=(0, 1), xycoords='axes fraction', fontsize=144,
                xytext=(5, -5), textcoords='offset points', ha='left', va='top', color="black")

        # Distance as string:
        distance_str = str(distance)

        # Build path as string cat:
        path = str(output_path) + '/plots/' + distance_str + '_v' + ver + '_' + timestamp + '_{}.png'.format(location_name)

        # Split the path into the directory and the file name
        dirname = os.path.dirname(path)

        # Save the figure:
        fig.savefig(path)

        # // Close the plot
        plot.close(fig)

        # Arg truth:
        arg_truth = 1
    
        # Truth args:
        truth_args(arg_truth)

        # Log:
        if arg_truth == 1:

            if os.path.exists(args.log):

                log_execution_count(filename = str(log_path)+'new.txt')

        else:

            next