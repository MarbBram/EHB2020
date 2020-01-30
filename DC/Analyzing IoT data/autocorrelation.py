import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
traffic = pd.read_csv("vehicles.csv")


# Plot traffic dataset
traffic[:"2018-11-10"].plot()

# Show plot
plt.show()

# Seasonal decomposition

# Import modules
import statsmodels.api as sm

# Perform decompositon
res = sm.tsa.seasonal_decompose(traffic["vehicles"])

# Print the seasonal component
print(res.seasonal)

# Plot the result
res.plot()

# Show the plot
plt.show()


import statsmodels.api as s
matplotlib.pyplot as plt

df = pd.read_json("environ_MS83200MS_nowind_3m-10min.json")
# Resample dataframe to 1h
df_seas = df.resample('1h').max()

# Run seasonal decompose
decomp = sm.tsa.seasonal_decompose(df_seas)