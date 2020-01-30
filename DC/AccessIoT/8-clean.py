import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_json("environ_MS83200MS_nowind_3m-10min.json")

cols = ["temperature", "humidity", "pressure"]

# Create a line plot
df[cols].plot(title="Environmental data")

# Label X-Axis
plt.xlabel("Time")

# Show plot
plt.show()

# Histogram plots
cols = ["temperature", "humidity", "pressure", "radiation"]

# Create a histogram
df[cols].hist(bins=30)

# Label Y-Axis
plt.ylabel("Frequency")

# Show plot
plt.show()


# Missing data
df = data
# Print head of the DataFrame
print(data.head())

# Drop missing rows
data_clean = data.dropna()
print(data_clean.head())


# Calculate and print NA count
print(data.isna().sum())