# R script: Bar graph of crime counts by year and crime type (side-by-side bars)
library(ggplot2)
library(readr)
library(dplyr)
library(lubridate)

# Load the data
crime <- read_csv('crime_2019_2025.csv')

# If DateTime column exists, extract Year from it; otherwise use Year column
year_col <- if ("DateTime" %in% colnames(crime)) {
  crime$DateTime <- as.POSIXct(crime$DateTime, format = "%m/%d/%Y %I:%M:%S %p")
  year(crime$DateTime)
} else {
  crime$Year
}
crime$Year <- year_col

# Filter out empty CrimeType (optional)
crime <- crime %>% filter(CrimeType != "")

# Group by year and crime type, count occurrences
crime_summary <- crime %>%
  group_by(Year, CrimeType) %>%
  summarise(Count = sum(Count), .groups = 'drop')

# Bar plot: side-by-side bars by crime type, colored by year
p <- ggplot(crime_summary, aes(x = CrimeType, y = Count, fill = as.factor(Year))) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(x = "Crime Type", y = "Number of Crimes", title = "Crime Counts by Year and Type", fill = "Year") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

# Save plot
ggsave("crime_by_year_and_type_dodge.png", p, width = 14, height = 7)

# Print plot to screen
print(p)
