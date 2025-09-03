import pandas as pd

# Load the 2020 Oakland vacancy rates CSV
csv_path = '../2020 vacancy/oakland_vacancy_rates_2020.csv'
df = pd.read_csv(csv_path)

# Count unique geoids in the file
unique_tracts = df['geoid'].nunique()
total_rows = len(df)
print(f"Unique tracts (geoids): {unique_tracts}")
print(f"Total rows: {total_rows}")

# Check if any geoid appears more than 4 times
geoid_counts = df['geoid'].value_counts()
more_than_4 = geoid_counts[geoid_counts > 4]
if not more_than_4.empty:
    print("Geoids appearing more than 4 times:")
    print(more_than_4)
else:
    print("No geoids appear more than 4 times.")
