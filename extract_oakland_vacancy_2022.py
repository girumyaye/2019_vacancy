import os
from dbfread import DBF
import pandas as pd

# List of 2022 DBF files
files = [
    '../2022 vacancy/usps_vac_032022_tractsum_2kx.dbf',
    '../2022 vacancy/usps_vac_062022_tractsum_2kx.dbf',
    '../2022 vacancy/usps_vac_092022_tractsum_2kx.dbf',
    '../2022 vacancy/usps_vac_122022_tractsum_2kx.dbf',
]

VACANCY_COL = 'avg_vac_r'

def extract_oakland_vacancy_rates(files, vacancy_col):
    dfs = []
    for file in files:
        dbf = DBF(file, load=True)
        df = pd.DataFrame(iter(dbf))
        # Filter for Oakland tracts (geoids in range 06001400100–06001408000)
        df = df[df['geoid'].astype(str).str.match(r'^0600140[0-7][0-9]{3}$|^06001408000$')]
        dfs.append(df[['geoid', vacancy_col]])
    all_df = pd.concat(dfs, ignore_index=True)
    return all_df

if __name__ == "__main__":
    oakland_vacancy = extract_oakland_vacancy_rates(files, VACANCY_COL)
    oakland_vacancy.to_csv('../2022 vacancy/oakland_vacancy_rates_2022.csv', index=False)
    print("Saved: ../2022 vacancy/oakland_vacancy_rates_2022.csv")
