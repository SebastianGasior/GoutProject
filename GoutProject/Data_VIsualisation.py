import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np  # Import numpy since we use np.ndenumerate

# Load your dataset (assuming it's in the current directory,
# update the path if it is elsewhere)
df = pd.read_excel('processed_dataset.xlsx')

# Count the number of foods in each Classified Group
group_counts = df['Classified_Group'].value_counts().sort_index()

# Create a bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x=group_counts.index, y=group_counts.values)
plt.title('Number of Foods in Each Classified Group')
plt.xlabel('Classified Group')
plt.ylabel('Number of Foods')
plt.xticks(range(len(group_counts)), ['1 (Lowest)', '2', '3', '4', '5 (Highest)'])  # Adjusting labels according to group counts
plt.show()

# Create a bubble chart: Concentration of Purines in Different Food Types

# Group the data by 'Type of Food' and 'Classified_Group', then count the occurrences
grouped = df.groupby(['Type of Food', 'Classified_Group']).size().reset_index(name='Counts')

# Create a pivot table for the bubble chart
pivot_table = grouped.pivot(index='Type of Food', columns='Classified_Group', values='Counts').fillna(0)

# Generate a bubble chart
plt.figure(figsize=(10, 8))
bubble_sizes = pivot_table.multiply(100).values  # Multiply by 100 for better visualization

for (i, j), size in np.ndenumerate(bubble_sizes):
    plt.scatter(x=j-1, y=i, s=size, alpha=0.5)  # Plot bubbles

# Adjust the labels and title
plt.xticks(ticks=np.arange(len(pivot_table.columns)), labels=['1', '2', '3', '4', '5'])
plt.yticks(ticks=np.arange(len(pivot_table.index)), labels=pivot_table.index, rotation=45)
plt.xlabel('Classified Group')
plt.ylabel('Type of Food')
plt.title('Average data for Total Purines and Uric Acid per 100g for each group')

# Custom legends
sizes = [50, 100, 150, 200, 250]  # Example sizes for our legend
legend_labels = ['50 (lowest)', '100', '150', '200', '250 (highest)']  # Example labels for our legend
for i, size in enumerate(sizes):
    plt.scatter([], [], s=size, alpha=0.5, label=legend_labels[i])

plt.legend(scatterpoints=1, frameon=False, labelspacing=1, title='Purine Concentration Scale')

# Show the plot
plt.show()

# Heatmap

# Calculate mean uric acid content per serving for each 'Type of Food' within each 'Classified_Group'
mean_uric_acid = df.pivot_table(values='Uric_acid_per_serving', index='Type of Food', columns='Classified_Group', aggfunc='mean').fillna(0)

# Create a heatmap to visualize the data
plt.figure(figsize=(12, 8))
sns.heatmap(mean_uric_acid, annot=True, fmt=".1f", linewidths=.5, cmap='YlGnBu')
plt.title('Average Uric Acid Content per Serving by Food Type and Classified Group')
plt.xlabel('Classified Group')
plt.ylabel('Type of Food')
plt.show()

# Comparison Bar Chart

# Example data from the 'Type of Food' groups
food_groups = [
    'Cereals, Beans, Soybean Products, and Dried Seaweeds',
    'Vegetables',
    'Eggs, Dairy Products, Mushrooms, and Fruits',
    'Animal Meat and Processed Meat',
    'Fresh Fish',
    'Fish Roe, Fish Milt, Shellfish, Mollusks, and Dried Fish',
    'Dried Fish, Canned Fish, Processed Fish, and Snacks',
    'Seasonings and Supplements'
]

# Simulated average data for Total Purines and Uric Acid per 100g for each group
total_purines_per_100g = [113, 84, 206, 50, 141, 147, 1034, 43]
uric_acid_per_100g = [137, 99, 244, 60, 168, 177, 1231, 56]

# Positions for the bars on the x-axis
ind = np.arange(len(food_groups))

# Width of the bars
bar_width = 0.35

fig, ax = plt.subplots(figsize=(14, 8))

# Creating the bars
purines_bars = ax.bar(ind - bar_width/2, total_purines_per_100g, bar_width, label='Total Purines per 100g', color='blue')
uric_acid_bars = ax.bar(ind + bar_width/2, uric_acid_per_100g, bar_width, label='Uric Acid per 100g', color='orange')

# Adding labels and title
ax.set_xlabel('Type of Food')
ax.set_ylabel('Content per 100g')
ax.set_title('Average Uric Acid Content per Serving by Food Type and Classified Group')
ax.set_xticks(ind)
ax.set_xticklabels(food_groups, rotation=90)  # Rotate labels to fit long names
ax.legend()

# Adding value labels above the bars
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(purines_bars)
add_labels(uric_acid_bars)

# Show the plot
plt.tight_layout()
plt.show()

# Compute the average of 'Total_Purines_per_100g' and 'Uric_acid_per_100g'

average_df = df.groupby('Type of Food').agg(
    Average_Total_Purines=('Total_Purines_per_100g', 'mean'),
    Average_Uric_acid=('Uric_acid_per_100g', 'mean')
)

# Display the result
print(average_df)