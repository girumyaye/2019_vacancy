import pandas as pd
import os

years = [2019, 2020, 2021, 2022, 2023, 2024]
folder_map = {
    2019: '../2019 vacancy/oakland_vacancy_rates_2019.csv',
    2020: '../2020 vacancy/oakland_vacancy_rates_2020.csv',
    2021: '../2021 vacancy/oakland_vacancy_rates_2021.csv',
    2022: '../2022 vacancy/oakland_vacancy_rates_2022.csv',
    2023: '../2023 vacancy/oakland_vacancy_rates_2023.csv',
    2024: '../2024 vacancy/oakland_vacancy_rates_2024.csv',
}

results = []
for year in years:
    path = folder_map[year]
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Some files may have extra columns, just use geoid and avg_vac_r
        if 'avg_vac_r' in df.columns:
            avg = df['avg_vac_r'].mean()
            results.append({'year': year, 'mean_avg_vac_r': avg})
        else:
            results.append({'year': year, 'mean_avg_vac_r': None})
    else:
        results.append({'year': year, 'mean_avg_vac_r': None})

summary = pd.DataFrame(results)
print(summary)
trend = summary['mean_avg_vac_r'].dropna().tolist()
if len(trend) > 1:
    if trend[-1] < trend[0]:
        print('General decrease in avg_vac_r from 2019 to 2024.')
    elif trend[-1] > trend[0]:
        print('General increase in avg_vac_r from 2019 to 2024.')
    else:
        print('No significant change in avg_vac_r from 2019 to 2024.')
else:
    print('Insufficient data for trend analysis.')
