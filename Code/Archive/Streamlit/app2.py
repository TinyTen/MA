import streamlit as st

import math as math
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
from cmcrameri import cm
from PIL import Image

import matplotlib.pyplot as plt
from plotly.express import bar, scatter, colors, imshow
from colors_cameri import davos

def app():
    st.title('Search for ingredients')

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

    ## read in data
    df_food = pd.read_excel("Code/Mockdata012.xlsx")
    df_food.set_index('Food product', inplace=True)
    mean_value = df_food.median(skipna=True,
        level=None,
        numeric_only=True,)
    normalised_df_food = df_food/mean_value

    nutrition =  ['calories [kcal]',
 'total_fat [g]',
 'saturated_fat [g]',
 'cholesterol [mg]',
 'sodium [mg]',
 'choline [mg]',
 'folate [mcg]',
 'folic_acid [mcg]',
 'niacin [mg]',
 'pant_acid [mg]',
 'riboflavin [mg]',
 'thiamin [mg]',
 'vitamin_a [IU]',
 'vitamin_a_rae [mcg]',
 'carotene_alpha [mcg]',
 'carotene_beta [mcg]',
 'cryxaanthin [mcg]',
 'lut_zea [mcg]',
 'lucopene [nan]',
 'vitamin_b12 [mcg]',
 'vitamin_b6 [mg]',
 'vitamin_c [mg]',
 'vitamin_d [IU]',
 'vitamin_e [mg]',
 'tocoph [mg]',
 'vitamin_k [mcg]',
 'calcium [mg]',
 'copper [mg]',
 'irom [mg]',
 'magnesium [mg]',
 'manganese [mg]',
 'phosphorous [mg]',
 'potassium [mg]',
 'selenium [mcg]',
 'zink [mg]',
 'protein [g]',
 'alanine [g]',
 'arginine [g]',
 'aspar [g]',
 'cystine [g]',
 'glutam [g]',
 'glycine [g]',
 'histidine [g]',
 'hy_proline [nan]',
 'isoleucine [g]',
 'leucine [g]',
 'lysine [g]',
 'methionine [g]',
 'ph_alanine [g]',
 'proline [g]',
 'serine [g]',
 'threonine [g]',
 'tryptophan [g]',
 'tyrosine [g]',
 'valine [g]',
 'carbhy [g]',
 'fiber [g]',
 'sugars [g]',
 'fructose [g]',
 'galactose [g]',
 'glucose [g]',
 'lactose [g]',
 'maltose [g]',
 'sucrose [g]',
 'fat [g]',
 'sat_fat_acids [g]',
 'mon_fat_acids [g]',
 'pol_fat_acids [g]',
 'trans_fat_acids [mg]',
 'alcohol [g]',
 'ash [g]',
 'caffeine [mg]',
 'theobromine [mg]',
 'water [g]']

    ecology = ['Land use change',
 'Animal Feed',
 'Farm',
 'Processing',
 'Transport',
 'Packging',
 'Retail',
 'Total_emissions',
 'EuEmkg',
 'Waterkg',
 'GreGaskcal',
 'Lndusekg',
 'Scarkg']

    all_aspects = nutrition + ecology

    def filter_data(normalised_df_food = normalised_df_food, 
                choice_food_products = list(normalised_df_food.index), choice_aspects = all_aspects, 
                category = normalised_df_food['Category'], allergens = normalised_df_food['Allergens'],
                nutritionalform = normalised_df_food['NutritionalForm'], protein_limit = 0):

        normalised_df_food = normalised_df_food[normalised_df_food['Category'].isin(list(category))]
        normalised_df_food = normalised_df_food[normalised_df_food['Allergens'].isin((allergens))]
        normalised_df_food = normalised_df_food[normalised_df_food['NutritionalForm'].isin(list(nutritionalform))]
        normalised_df_food = normalised_df_food[normalised_df_food['protein [g]'] > protein_limit]


        df = normalised_df_food.loc[choice_food_products][ choice_aspects]
        
        return df

    ##set filters
    choice_food_products = st.multiselect('Please select the food products you want to compare:',
    list(normalised_df_food.index),     default= list(normalised_df_food.index)
    )

    choice_aspects = st.multiselect('Please select what you want to compare:',
    list(df_food.columns), default= list(df_food.columns)   
    )

    category = st.multiselect('Please select the category you want to compare:',
    df_food['Category'].unique(), default= df_food['Category'].unique()
    )

    allergens = st.multiselect('Please select the allergens you want to include:',
    df_food['Allergens'].unique(), default= df_food['Allergens'].unique()
    )

    nutritionalform = st.multiselect('Please select the nutritional forms you want to include:',
    df_food['NutritionalForm'].unique(), default= df_food['NutritionalForm'].unique()
    )

    protein_limit = st.number_input('Please select the lower limit of protein content you want to include:', 
                                    max_value = 100 , min_value=0)

    normalised_df_food = normalised_df_food
    # choice_food_products = choice_food_products
    # choice_aspects = choice_aspects
    # category = category
    # allergens = allergens
    # nutritionalform = nutritionalform
    # protein_limit = protein_limit


    df = filter_data(choice_food_products = choice_food_products,
                         choice_aspects = choice_aspects,
                         category = category,
                         allergens = allergens,
                         nutritionalform = nutritionalform,
                         protein_limit = protein_limit)

    # plt.figure(figsize=(20, 20))
    fig1 = imshow(df.T, text_auto=False, aspect="auto", width=800,height=1600,
        color_continuous_scale=davos
                )
    fig1.update_xaxes(side = "top")
    st.plotly_chart(fig1, use_container_width=True)

    plt.figure(figsize=(20, 20))
    fig2 = imshow(df.T, text_auto=True, aspect="auto", width=800,height=1600,
        color_continuous_scale=davos
                )
    fig2.update_xaxes(side = "top")
    st.plotly_chart(fig2, use_container_width=True)