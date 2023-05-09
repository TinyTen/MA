"""
Streamlit Application Food Sustainability
Autor: Christina Koeck
Date: 02/2023
"""

# https://docs.streamlit.io/library/api-reference

import math as math
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
from PIL import Image

import matplotlib.pyplot as plt
from plotly.express import bar, scatter, colors



# Configuration
st.set_page_config(
    page_title="Food Sustainability"
)

image = Image.open('veggie.jpg')

st.image(image)

st.title("Comparison of sustainability parameters of food")

st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  background-color: blue !important;
}
</style>
""",
    unsafe_allow_html=True,
)


import warnings
warnings.filterwarnings('ignore')
                        

# Data 
df_food = pd.read_csv('df_food.csv')
df_food.drop('Unnamed: 0', axis =1, inplace=True)

#Visualisations

df = df_food
fig0 = scatter(df, size="Total_emissions", y="Land use per kilogram (m² per kilogram)",
                 x = 'Freshwater withdrawals per kilogram (liters per kilogram)', color="Category",
                 title ='Overview sustainability of food products, size of circles is the total emissions', 
           hover_name="Food product", size_max=60,
        color_discrete_sequence=colors.qualitative.Prism)
st.plotly_chart(fig0, use_container_width=True)


st.header('Here are some questions that help you to explore food sustainability. You can choose the categories and food products which you want to compare.')

# Which is the most sustainable / least sustainable
# Food (lowest total emissions) for the chosen category

st.subheader('Question 1: Which is the most sustainable (lowest total emissions) for the chosen category?')

cats = st.multiselect('Please select categories to display:',
    ['Grains', 'Vegetables', 'Sugar', 'Nuts', 'Plant_Dairy', 'Oils',
       'Fruits', 'Other', 'Animal_Prod', 'Dairy', 'Egg_Prod'],
       default='Vegetables')


fig1 = plt.figure(figsize=(20, 8))
filtered = df_food[df_food['Category'].isin(cats)]
sns.barplot(x = filtered['Food product'], y = filtered['Total_emissions'], palette="rocket", hue = filtered['Category'] )
plt.title(f'Total Emissions per kg of Food for Different Foods in the Chosen Categories = {cats}',
        fontsize=18, color= 'black', fontweight='bold')
plt.xlabel('')
plt.xticks(fontsize=10)
plt.yticks(fontsize=15)
plt.ylabel('Total Emissions', fontsize=18)
plt.legend(fontsize=15)
sns.despine(left=True, bottom=True)
st.pyplot(fig1)


# Which life cycle step has the greatest impact on total emissions (for selected food)?

st.subheader('Question 2: Which life cycle step has the greatest impact on total emissions (for selected food)?')

stages = ['Land use change', 'Animal Feed', 'Farm', 'Processing',
           'Transport', 'Packging', 'Retail']
lifecycle = df_food[['Food product','Land use change', 'Animal Feed', 'Farm', 'Processing',
           'Transport', 'Packging', 'Retail']]
lifecycle = lifecycle.T
lifecycle.columns = lifecycle.loc['Food product']
lifecycle.drop('Food product', axis = 0, inplace=True)

lifecycle['stage'] = stages

choice = st.multiselect('Please select food products to display:',
                        df_food['Food product'].unique(),
                        default='Potatoes')

fig2= plt.figure(figsize=(20, 8))
plt.title(f'Total Emissions per Processing Stage of Different Foods',
          fontsize=18, color= 'black', fontweight='bold')
sns.lineplot(lifecycle[choice], dashes= True, legend='full', linewidth = 5, alpha = 0.6)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
sns.despine(left=True, bottom=True)
st.pyplot(fig2)


# What is the least efficient food in terms of greenhouse gas emissions per 100g protein (kg CO₂eq per 100g protein)?

st.subheader('Question 3: What is the least efficient food in terms of greenhouse gas emissions per 100g protein (kg CO₂eq per 100g protein)?')


cats2 = st.multiselect('Please select categories to display for question 3:',
    ['Grains', 'Vegetables', 'Sugar', 'Nuts', 'Plant_Dairy', 'Oils',
       'Fruits', 'Other', 'Animal_Prod', 'Dairy', 'Egg_Prod'],
        default='Vegetables')


fig3 = plt.figure(figsize=(20, 8))
filtered = df_food[df_food['Category'].isin(cats2)]
sns.barplot(x = filtered['Food product'],
            y = filtered['Greenhouse gas emissions per 100g protein (kgCO₂eq per 100g protein)'],
           palette="rocket",
           hue = filtered['Category'] )
plt.title(f'Greenhouse Gas Emissions per 100g PROTEIN in the Chosen Categories = {cats2}', 
                   fontsize=18, color= 'black', fontweight='bold')
plt.xlabel('')
plt.xticks(fontsize=10)
plt.yticks(fontsize=15)
plt.ylabel('Greenhouse gas emissions per 100g protein (kgCO₂eq per 100g protein)', fontsize=13.5)
plt.legend(fontsize=15)
sns.despine(left=True, bottom=True)
st.pyplot(fig3)


# What is the least efficient food in terms of greenhouse gas emissions per 1000kcal (kgCO₂eq per 1000kcal)?
# Only the nutritional value of the food is taken into account here!

st.subheader('Question 4: What is the least efficient food in terms of greenhouse gas emissions per 1000kcal (kgCO₂eq per 1000kcal)? Only the nutritional value of the food is taken into account here!')

cats3 = 'Vegetables'
cats3 = st.multiselect('Please select categories to display for question 4:',
    ['Grains', 'Vegetables', 'Sugar', 'Nuts', 'Plant_Dairy', 'Oils',
       'Fruits', 'Other', 'Animal_Prod', 'Dairy', 'Egg_Prod'],
        default='Vegetables')


fig4 = plt.figure(figsize=(20, 8))
filtered = df_food[df_food['Category'].isin(cats3)]
sns.barplot(x = filtered['Food product'],
            y = filtered['Greenhouse gas emissions per 100g protein (kgCO₂eq per 100g protein)'],
           palette="rocket", 
           hue = filtered['Category'] )
plt.title(f'Greenhouse Gas Emissions per 100g PROTEIN in the Chosen Categories = {cats3}', 
                   fontsize=18, color= 'black', fontweight='bold')
plt.xlabel('')
plt.xticks(fontsize=10)
plt.yticks(fontsize=15)
plt.ylabel('Greenhouse gas emissions per 100g protein (kgCO₂eq per 100g protein)', fontsize=13.5)
plt.legend(fontsize=15)
sns.despine(left=True, bottom=True)
st.pyplot(fig4)


# How do sustainability measures and emissions correlate?

st.subheader('Question 5: How do sustainability measures and emissions correlate?')

per_protein = df_food.columns[[11, 13, 16, 19, 21]]
per_calories = df_food.columns[[9, 12, 15, 17, 22]]
measures = df_food[per_calories]
fig5 = plt.figure()
mask = np.triu(np.ones_like(measures.corr(), dtype=bool))
ax = sns.heatmap(measures.corr(), cmap="mako",
            annot= True, center=0.8,
           square=True, linewidths=.5,
           mask=mask)
ax.xaxis.tick_top()
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
ax.set_xticklabels(['Eutrophying Em', 'Freshwater Withd', 'Greenhouse gem', 'Land use', 'Scarcity water' ], rotation=90)
sns.despine(left=True, bottom=True)
plt.title('Pearson - Correlations', loc = 'right', y= 0.8)
st.pyplot(fig5)


# Do foods that do not require further processing cause higher emissions during the previous processing steps?

st.subheader('Question 6: Do foods that do not require further processing cause higher emissions during the previous processing steps?')

fig7 = bar(data_frame =df_food,  y = 'Food product', x = 'Total_emissions', color= 'Further processing needed',
          title ='Total_emissions per kg of food for differnt foods in the chosen category', 
        color_discrete_sequence=colors.qualitative.Prism, width=1700, height= 1000 )
st.plotly_chart(fig7, use_container_width=True)