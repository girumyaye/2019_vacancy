import os
from dbfread import DBF
import pandas as pd

# List of 2020 DBF files
files = [
    '../2020 vacancy/usps_vac_032020_tractsum_2kx.dbf',
    '../2020 vacancy/usps_vac_062020_tractsum_2kx.dbf',
    '../2020 vacancy/usps_vac_092020_tractsum_2kx.dbf',
    '../2020 vacancy/usps_vac_122020_tractsum_2kx.dbf',
]

VACANCY_COL = 'avg_vac_r'

# Extract and aggregate vacancy rates for Oakland geoids

def extract_oakland_vacancy_rates(files, vacancy_col):
    dfs = []
    for f in files:
        if os.path.exists(f):
            table = DBF(f)
            df = pd.DataFrame(iter(table))
            if 'geoid' in df.columns:
                geoids = df['geoid'].astype(str)
                oakland_df = df[(geoids >= '06001400100') & (geoids <= '06001408000')][['geoid', vacancy_col]]
                dfs.append(oakland_df)
    if dfs:
        result = pd.concat(dfs, ignore_index=True)
        return result
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    oakland_vacancy = extract_oakland_vacancy_rates(files, VACANCY_COL)
    print("Oakland 2020 Vacancy Rates (geoid, avg_vac_r):")
    print(oakland_vacancy.head())
    oakland_vacancy.to_csv('../2020 vacancy/oakland_vacancy_rates_2020.csv', index=False)
    print("\nResults saved to 2020 vacancy/oakland_vacancy_rates_2020.csv")
