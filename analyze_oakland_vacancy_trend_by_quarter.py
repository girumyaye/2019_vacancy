import pandas as pd
import os
import re

years = [2019, 2020, 2021, 2022, 2023, 2024]
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
# Map each year to its folder and DBF file patterns
csv_map = {
    2019: '../2019 vacancy/oakland_vacancy_rates_2019.csv',
    2020: '../2020 vacancy/oakland_vacancy_rates_2020.csv',
    2021: '../2021 vacancy/oakland_vacancy_rates_2021.csv',
    2022: '../2022 vacancy/oakland_vacancy_rates_2022.csv',
    2023: '../2023 vacancy/oakland_vacancy_rates_2023.csv',
    2024: '../2024 vacancy/oakland_vacancy_rates_2024.csv',
}
# Patterns to identify quarters in filenames
quarter_patterns = {
    'Q1': re.compile(r'03(19|20|21|22|23|24)'),
    'Q2': re.compile(r'06(19|20|21|22|23|24)'),
    'Q3': re.compile(r'09(19|20|21|22|23|24)'),
    'Q4': re.compile(r'12(19|20|21|22|23|24)'),
}

results = []
for year in years:
    path = csv_map[year]
    if os.path.exists(path):
        df = pd.read_csv(path)
        # If SourceFile column exists, use it to determine quarter
        if 'SourceFile' in df.columns:
            for q, pat in quarter_patterns.items():
                mask = df['SourceFile'].astype(str).str.contains(pat)
                if mask.any():
                    avg = df.loc[mask, 'avg_vac_r'].mean()
                    results.append({'year': year, 'quarter': q, 'mean_avg_vac_r': avg})
                else:
                    results.append({'year': year, 'quarter': q, 'mean_avg_vac_r': None})
        else:
            # If no SourceFile, assume rows are ordered by quarter (repeat for each quarter)
            n = len(df) // 4
            for i, q in enumerate(quarters):
                part = df.iloc[i*n:(i+1)*n]
                avg = part['avg_vac_r'].mean() if not part.empty else None
                results.append({'year': year, 'quarter': q, 'mean_avg_vac_r': avg})
    else:
        for q in quarters:
            results.append({'year': year, 'quarter': q, 'mean_avg_vac_r': None})

summary = pd.DataFrame(results)
print(summary)
summary.to_csv('oakland_vacancy_rate_trend_by_quarter_2019_2024.csv', index=False)
