import pandas as pd
import geopandas as gpd
from shapely import wkt
import matplotlib.pyplot as plt

df = pd.read_csv('data/uber-movement-london-traversals.csv')
df['geometry'] = df['wktGeometry'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf.plot()
plt.savefig('uber_movements.png')
