import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# --- User settings ---
CRIME_CSV = 'crime_2019_2025_full.csv'
COUNCIL_SHP = 'CouncilDistrict_20250701/geo_export_2ecee881-b550-44e2-b7c7-693c0535255a.shp'  # <-- Update this to match the actual .shp filename
OUTPUT_CSV = 'crime_with_council_district.csv'

# --- Load crime data ---
df = pd.read_csv(CRIME_CSV)

# If you have a 'point' column like "(lat, lon)", extract coordinates:
if 'point' in df.columns:
    df['point'] = df['point'].str.replace('[()]', '', regex=True)
    df[['Latitude', 'Longitude']] = df['point'].str.split(',', expand=True)
    df['Latitude'] = df['Latitude'].astype(float)
    df['Longitude'] = df['Longitude'].astype(float)

# Drop rows with missing coordinates
df = df.dropna(subset=['Latitude', 'Longitude'])

# Create geometry column
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

# --- Load council districts shapefile ---
districts = gpd.read_file(COUNCIL_SHP)
districts = districts.to_crs('EPSG:4326')

# --- Spatial join ---
joined = gpd.sjoin(gdf, districts, how='left', predicate='within')

# --- Save result ---
joined.to_csv(OUTPUT_CSV, index=False)
print(f"Saved: {OUTPUT_CSV}")
