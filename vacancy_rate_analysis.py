import os
from dbfread import DBF
import pandas as pd

# List of DBF files
files = [
    'usps_vac_032019_tractsum_2kx.dbf',
    'usps_vac_062019_tractsum_2kx.dbf',
    'usps_vac_092019_tractsum_2kx.dbf',
    'usps_vac_122019_tractsum_2kx.dbf',
]

def list_columns(dbf_file):
    table = DBF(dbf_file)
    print(f"\nColumns in {dbf_file}:")
    print(list(table.field_names))
    return list(table.field_names)

# Step 1: List columns in each file
for f in files:
    if os.path.exists(f):
        list_columns(f)
    else:
        print(f"File not found: {f}")

VACANCY_COL = 'avg_vac_r'  # Checking the average vacancy rate column

# Step 3: Extract and aggregate vacancy rates
def extract_vacancy_rates(files, vacancy_col):
    dfs = []
    for f in files:
        if os.path.exists(f):
            table = DBF(f)
            df = pd.DataFrame(iter(table))
            df['SourceFile'] = f
            # Print sample of unique geoids for debugging
            if 'geoid' in df.columns:
                print(f"Sample geoids from {f}:")
                print(df['geoid'].drop_duplicates().astype(str).head(20).to_list())
                # Filter for geoids in the range 06001400100 to 06001408000 (Oakland tracts)
                geoids = df['geoid'].astype(str)
                filtered_df = df[(geoids >= '06001400100') & (geoids <= '06001408000')][['geoid', vacancy_col, 'SourceFile']]
                dfs.append(filtered_df)
    if dfs:
        result = pd.concat(dfs, ignore_index=True)
        return result
    else:
        return pd.DataFrame()

# Only run extraction if the column name is set
if VACANCY_COL:
    vacancy_df = extract_vacancy_rates(files, VACANCY_COL)
    print("\nVacancy Rates for Oakland (geoids 06001400100 to 06001408000):")
    print(vacancy_df.head())
    vacancy_df.to_csv('oakland_vacancy_rates_over_year.csv', index=False)
    print("\nResults saved to oakland_vacancy_rates_over_year.csv")
else:
    print("\nPlease update VACANCY_COL with the correct column name from the output above.")
