import pandas as pd
import os

# File paths for each year
files = [
    '../2020 vacancy/oakland_vacancy_rates_2020.csv',
    '../2021 vacancy/oakland_vacancy_rates_2021.csv',
    '../2022 vacancy/oakland_vacancy_rates_2022.csv',
    '../2023 vacancy/oakland_vacancy_rates_2023.csv',
    '../2024 vacancy/oakland_vacancy_rates_2024.csv',
]
years = [2020, 2021, 2022, 2023, 2024]

# Calculate mean avg_vac_r for each year
means = []
for file, year in zip(files, years):
    df = pd.read_csv(file)
    # Some files may have duplicate tracts per year, so take the mean per tract first, then mean across tracts
    tract_means = df.groupby('geoid')['avg_vac_r'].mean()
    means.append({'year': year, 'mean_avg_vac_r': tract_means.mean()})

result_df = pd.DataFrame(means)
result_df.to_csv('oakland_vacancy_rate_trend_2020_2024.csv', index=False)
print(result_df)
