# R script: Aggregate annual crime totals and compare with vacancy rates (2019-2024)
library(dplyr)
library(readr)

# Load full crime data
crime <- read_csv('crime_2019_2025_full.csv')
crime$year <- as.integer(substr(crime$DateTime, 1, 4))

# Aggregate total annual crime counts (2019-2024)
crime_totals <- crime %>%
  filter(year >= 2019 & year <= 2024) %>%
  group_by(year) %>%
  summarise(total_crimes = n())

# Load annual mean vacancy rates (from quarterly trend)
vac <- read_csv('oakland_vacancy_rate_trend_by_quarter_2019_2024.csv')
vac$year <- as.integer(vac$year)
annual_vac <- vac %>%
  group_by(year) %>%
  summarise(mean_vacancy_rate = mean(mean_avg_vac_r))

# Merge on year
merged <- inner_join(annual_vac, crime_totals, by = 'year')
write_csv(merged, 'vacancy_vs_crime_annual_2019_2024_r.csv')

# Correlation (Pearson)
pearson <- cor(merged$mean_vacancy_rate, merged$total_crimes, method = 'pearson')
# Correlation (Spearman)
spearman <- cor(merged$mean_vacancy_rate, merged$total_crimes, method = 'spearman')

cat('Merged data:\n')
print(merged)
cat(sprintf('Pearson correlation: %.3f\n', pearson))
cat(sprintf('Spearman correlation: %.3f\n', spearman))
