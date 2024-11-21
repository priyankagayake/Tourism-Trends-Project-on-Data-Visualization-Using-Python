# -*- coding: utf-8 -*-
"""Tourism Trend.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cu5_F188XvZC5mBOx3ixVIKsEBldnldg
"""

!pip install plotly

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
file_path = '/content/tourism_dataset.csv'  # Replace with your file path
tourism_data = pd.read_csv(file_path)

# Preview dataset
print(tourism_data.head())
print(tourism_data.info())

# Top 10 most visited locations
top_locations = tourism_data.sort_values(by='Visitors', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_locations, x='Location', y='Visitors', hue='Country', palette='viridis')
plt.title('Top 10 Most Visited Locations')
plt.xlabel('Location')
plt.ylabel('Number of Visitors')
plt.xticks(rotation=45)
plt.legend(title='Country')
plt.show()

# Revenue contribution by each country
country_revenue = tourism_data.groupby('Country')['Revenue'].sum()

country_revenue.plot.pie(autopct='%1.1f%%', figsize=(8, 8), title='Revenue Contribution by Country')
plt.ylabel('')  # Remove ylabel
plt.show()

# Average rating for each location category
category_ratings = tourism_data.groupby('Category')['Rating'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=category_ratings, x='Category', y='Rating', palette='cool')
plt.title('Average Rating by Location Category')
plt.xlabel('Category')
plt.ylabel('Average Rating')
plt.xticks(rotation=45)
plt.show()

# Scatter plot to analyze relationship between revenue and visitors
plt.figure(figsize=(8, 6))
sns.scatterplot(data=tourism_data, x='Visitors', y='Revenue', hue='Category', size='Revenue', sizes=(20, 200), palette='deep')
plt.title('Revenue vs Visitors')
plt.xlabel('Visitors')
plt.ylabel('Revenue')
plt.grid(True)
plt.show()

# Countplot to show accommodation availability by category
plt.figure(figsize=(10, 6))
sns.countplot(data=tourism_data, x='Category', hue='Accommodation_Available', palette='Set2')
plt.title('Accommodation Availability by Location Category')
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Accommodation Available')
plt.show()

from ipywidgets import interact, Dropdown

# Interactive filter function
def filter_data(country, category):
    filtered_data = tourism_data.copy()

    # Filter by Country
    if country != "All":
        filtered_data = filtered_data[filtered_data['Country'] == country]

    # Filter by Category
    if category != "All":
        filtered_data = filtered_data[filtered_data['Category'] == category]

    # Display filtered data
    display(filtered_data.head(10))
    print(f"Total Locations: {len(filtered_data)}")

# Create dropdown options
country_options = ["All"] + list(tourism_data['Country'].unique())
category_options = ["All"] + list(tourism_data['Category'].unique())

# Interact widget
interact(filter_data,
         country=Dropdown(options=country_options, description="Country"),
         category=Dropdown(options=category_options, description="Category"))

# Add a new column for revenue per visitor
tourism_data['Revenue_per_Visitor'] = tourism_data['Revenue'] / tourism_data['Visitors']

# Handle cases with 0 visitors to avoid division errors
tourism_data['Revenue_per_Visitor'].fillna(0, inplace=True)

# Display top 10 locations by revenue per visitor
top_revenue_per_visitor = tourism_data[['Location', 'Country', 'Revenue_per_Visitor']].sort_values(by='Revenue_per_Visitor', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_revenue_per_visitor, x='Location', y='Revenue_per_Visitor', hue='Country', palette='plasma')
plt.title('Top 10 Locations by Revenue Per Visitor')
plt.xlabel('Location')
plt.ylabel('Revenue Per Visitor')
plt.xticks(rotation=45)
plt.legend(title='Country')
plt.show()

# Compute correlation matrix
correlation_matrix = tourism_data[['Visitors', 'Revenue', 'Rating', 'Revenue_per_Visitor']].corr()

# Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Between Variables')
plt.show()

# Interactive map to visualize visitors by country
fig = px.scatter_geo(
    tourism_data,
    locations="Country",  # Use Country names
    locationmode="country names",  # Match countries
    hover_name="Location",  # Display location names on hover
    size="Visitors",  # Adjust marker size by number of visitors
    color="Category",  # Use categories for color coding
    title="Tourist Locations by Visitor Count",
    projection="natural earth"  # Use natural earth projection
)
fig.show()