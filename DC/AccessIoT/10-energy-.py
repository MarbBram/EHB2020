# import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("energy.csv")

# Replace the timestamp with the parsed timestamp
df['ts'] = pd.to_datetime(df["ts"], unit="ms")
print(df.head())

