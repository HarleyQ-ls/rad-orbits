import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import json
from shapely.geometry import shape
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from descartes import PolygonPatch
import seaborn as sns
import matplotlib.colors as mcolors

color_palette = sns.color_palette("rocket")
fig = plt.figure(figsize=(10, 6))

# Load the data from CSV, here I took the data from spenvis
data = pd.read_csv('./datasets/spenvis/dataset_spenvis_tpo_800km.csv')

# Extract latitude, longitude, and mag field values
latitudes = data['lat'].values
longitudes = data['lon'].values
# values = data['B_Gauss'].values
values = data['Flux_cm_u-2_s_u-1_50MeV'].values


# World plot
ax = fig.add_subplot()
sc = ax.scatter(longitudes, latitudes, c=values, cmap='jet', s=15, alpha=0.6, norm=mcolors.LogNorm())
plt.colorbar(sc, label=r'$\text{AP-8 MAX Flux } > \, 50.00 \, \text{MeV (cm}^{-2} \, \text{s}^{-1}) \text{ at 800.0 km}$', shrink=0.6)
world = gpd.read_file("./datasets/countries/ne_110m_admin_0_countries.shp")
world.plot(
    ax=ax,
    color="lightgray",
    edgecolor="black",
    alpha=0.5,
    legend=True
)

# Load the JSON file containing the polygons
with open('outputs/polygons_tpo.json', 'r') as f:
    polygons = json.load(f)

# Modify this list based on the levels you want to plot
levels_to_plot = [10.0, 100.0, 1000.0]  

# Filter and plot polygons
color_counter = 0
for polygon_data in polygons:
    level = polygon_data.get("level")
    if level in levels_to_plot:
        try:
            # Extract the coordinates of the polygon
            coordinates = polygon_data['geometry']['coordinates'][0]  # Use only the exterior ring

            # Create a Polygon patch with no fill
            outline_patch = mpatches.Polygon(coordinates, closed=True, edgecolor='black', fill=False, linewidth=1.5)
            ax.add_patch(outline_patch)
            color_counter = color_counter + 1

        except (IndexError, TypeError, KeyError) as e:
            print(f"Skipping a polygon due to error: {e}")

# Show the plot
plt.xlabel('Longitude [Degrees]')
plt.ylabel('Latitude [Degrees]')
plt.tight_layout()
plt.title('Trapped protons according to the AP-8 model, at 800Km of height')
# plt.savefig('outputs/saa_overview.pdf', format='pdf', bbox_inches='tight')
plt.show()