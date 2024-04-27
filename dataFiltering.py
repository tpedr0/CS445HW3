import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('taxData2021.txt', sep='\t').set_index('item')
df.replace('X', np.nan, inplace=True)

# Calculate the number of NaNs and zeroes in each row
df['number_of_NaNs'] = df[df.columns].isna().sum(1)
df['number_of_zeroes'] = df[df.columns].eq('0').sum(1)

# Filter the DataFrame
item_df = df[(df['number_of_NaNs'] == 0) & (df['number_of_zeroes'] == 0)]

# Print the filtered DataFrame
print(item_df)

# Save the filtered DataFrame to a CSV file
item_df.to_csv('filteredTaxData2021.csv', index=True)
