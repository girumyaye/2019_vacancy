import pandas as pd

# Load crime data
crime = pd.read_csv('crime_2019_2025.csv')

# Aggregate total annual crime counts (all types, including empty CrimeType)
crime_totals = crime.groupby('Year', as_index=False)['Count'].sum()
crime_totals.rename(columns={'Count': 'total_crimes'}, inplace=True)

# Load annual mean vacancy rates (from quarterly trend)
vac = pd.read_csv('oakland_vacancy_rate_trend_by_quarter_2019_2024.csv')
vac['year'] = vac['year'].astype(int)
annual_vac = vac.groupby('year', as_index=False)['mean_avg_vac_r'].mean()
annual_vac.rename(columns={'mean_avg_vac_r': 'mean_vacancy_rate'}, inplace=True)

# Merge on year
merged = pd.merge(annual_vac, crime_totals, left_on='year', right_on='Year', how='inner')
merged = merged[['year', 'mean_vacancy_rate', 'total_crimes']]

# Save merged data
merged.to_csv('vacancy_vs_crime_annual_2019_2024.csv', index=False)

# Correlation (Pearson)
pearson = merged[['mean_vacancy_rate', 'total_crimes']].corr(method='pearson').iloc[0,1]

# Correlation (Spearman)
spearman = merged[['mean_vacancy_rate', 'total_crimes']].corr(method='spearman').iloc[0,1]

print('Merged data:')
print(merged)
print(f'Pearson correlation: {pearson:.3f}')
print(f'Spearman correlation: {spearman:.3f}')
