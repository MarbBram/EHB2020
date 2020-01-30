import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.read_csv("heatmap.csv")

# Calculate correlation
corr = data.corr()

# Print correlation
print(corr)

# Create a heatmap
sns.heatmap(corr, annot=True)

# Show plot
plt.show()



# Create a pairplot
sns.pairplot(data)

# Show plot
plt.show()


# Calculate mean
data["mean"] = data["temperature"].mean()

# Calculate upper and lower limits
data["upper_limit"] = data["mean"] + (data["temperature"].std() * 3)
data["lower_limit"] = data["mean"] - (data["temperature"].std() * 3)

# Plot the dataframe
data.plot()

plt.show()