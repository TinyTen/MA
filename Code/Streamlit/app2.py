import streamlit as st

import math as math
import pandas as pd
import numpy as np
# import seaborn as sns
import streamlit as st
from cmcrameri import cm
from PIL import Image

import matplotlib.pyplot as plt
from plotly.express import bar, scatter, colors, imshow
from colors_cameri import davos, oslo

def app():
    st.title('Comparing Food Items')
    st.text('In this section you can compare parameters for chosen food items.')

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
    df_dapro = pd.read_excel("Code/df_dapro_matrix.xlsx")
    df_dapro.rename(columns= {'Unnamed: 0': ' '}, inplace=True)
    df_dapro.set_index(' ', drop = True, inplace=True)
    df = pd.read_excel("Code/df_n_matrix.xlsx")
    df.rename(columns= {'Unnamed: 0': ' '}, inplace=True)
    df.set_index(' ', drop = True, inplace=True)

    oslo_rgb = ['rgb(0, 1, 0)',
    'rgb(11, 25, 39)',
    'rgb(17, 48, 77)',
    'rgb(27, 73, 117)',
    'rgb(46, 98, 160)',
    'rgb(78, 125, 199)',
    'rgb(111, 146, 202)',
    'rgb(144, 166, 201)',
    'rgb(176, 185, 200)',
    'rgb(215, 215, 216)',
    'rgb(255, 255, 255)'] 
 #----------------------------------------


# figure 1
    
    options_food = list(df_dapro.index)

    choice_food = st.multiselect(
        'Please select the food items you want to compare:',
        options_food, default=['Apple', 'Cashew nut', 'Chicken'])
    
    options = ['Protein_g/g', 'Eutrophying emissions per 100g (gPO₄eq per 100g}',
       'Land use per 100g (m² per 100g)', 
                'Freshwater withdrawals per 100g (liters per 100g)' , 'Alanin_mg/100g', 'Arginin_mg/100g', 'Cystein_mg/100g', 'Histidin_mg/100g', 
        'Isoleucin_mg/100g',  'Lysin_mg/100g', 'Vitamin B12-Cobalamin_μg/100g', 'Sodium_mg/100g', 'Cholesterin_mg/100g', 'Fat_g/100g','Simply unsaturated fatty acids mg/100g',]

    parameters = st.multiselect(
        'Please select the paramters you want to compare:',
        options, default=['Protein_g/g', 
              'Freshwater withdrawals per 100g (liters per 100g)' , 'Alanin_mg/100g'])


    df_plot = df_dapro.loc[choice_food][parameters]

    from sklearn import preprocessing

    min_max_scaler = preprocessing.MinMaxScaler(feature_range = (0,1))
    df_n = min_max_scaler.fit_transform(df_plot )
    df_n = pd.DataFrame(df_n, index = df_plot.index, columns=df_plot.columns)


    annotations = ((df_plot.T).to_numpy()).round(2)
    title_text =  'Comparison of the chosen parameters for the chosen food products (per 100g product). <br>Dark color signifies low values in comparison with the other chosen products, <br>bright colors signify high values.<br>The colours refer to each line separately (white = highest color of each row), so that<br>the values of different foods can be compared with each other.<br>The exact values are written in the respective panels.'


    plt.figure(figsize=(20, 20))
    fig = imshow(df_n.T, text_auto=False, aspect="auto", width=1000,height=750,
        color_continuous_scale=oslo, 
    #              ,   text = (df_dapro.T).to_numpy()
                )
    fig.update_xaxes(side = "top")
    # fig['layout'].update(annotations=annotations)
    fig.update_layout(title_text=title_text,title_y = 0.95, 
                            margin={'t': 220})

    fig.update_traces(text=annotations, texttemplate="%{text}")
    fig.update_coloraxes(showscale=False)

    st.plotly_chart(fig, use_container_width=True)

# # figure 2

    options_food2 = list(df_dapro.index)

    choice_food2 = st.multiselect(
        'Please select the food items you want to compare (max. 3 items):',
        options_food2, default=['Chicken', 'Cashew nut', 'Durum wheat'],
        max_selections = 3)
    

    options2 = ['Protein_g/g', 'Eutrophying emissions per 100g (gPO₄eq per 100g}',
       'Land use per 100g (m² per 100g)', 
                'Freshwater withdrawals per 100g (liters per 100g)' , 'Alanin_mg/100g', 'Arginin_mg/100g', 'Cystein_mg/100g', 'Histidin_mg/100g', 
        'Isoleucin_mg/100g',  'Lysin_mg/100g', 'Vitamin B12-Cobalamin_μg/100g', 'Sodium_mg/100g', 'Cholesterin_mg/100g', 'Fat_g/100g', 'Simply unsaturated fatty acids mg/100g',]


    parameters2 = st.multiselect(
        'Please select the paramters you want to compare (max. 3 items):',
        options2, default= ['Protein_g/g', 
                            'Lysin_mg/100g'],
              max_selections = 3)
    


    df_plot = df_dapro.loc[choice_food2][parameters2].T


    fig2 = bar(df_plot,
                barmode="group",
                facet_col=df_plot.index, 
                color_discrete_sequence=oslo_rgb[1::3],
        color_continuous_scale=None, orientation = 'v',
                            facet_col_spacing=0.06,
                width= 1000,
                height = 700,
                title = ('Comparison of the chosen parameters for the chosen food items (per 100g). <br>Items can be turned on or off by clicking in the item in the legend.')
                
        )
    fig2.update_xaxes(matches=None, showticklabels=True)
    fig2.update_yaxes(matches=None, showticklabels=True)
    st.plotly_chart(fig2, use_container_width=True)
