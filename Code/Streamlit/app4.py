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
from colors_cameri import davos, oslo

def app():
    st.title('Protein Sources - Study Results')
    st.text('''
    A feature for the database is an input screen where students can store study results \n
    from literature review. This collection of studies should facilitate the search and \n
    comparison of new findings.''')

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
    # Data are from:
    # ZHAW database mix from end of 2022
    df_studies = pd.read_excel("Code/study_data.xlsx")
    df_studies.rename(columns={"Unnamed: 0": "source"}, inplace=True)
    df_studies.set_index('source', inplace = True)
    df_studies['Datum der Studie (Jahr)']= pd.to_datetime(df_studies['Datum der Studie (Jahr)'])

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
 #-----------------------------

    # figure

    options2 = df_studies.columns

    parameters2 = st.multiselect(
        'Please select the paramters you want to compare (max. 3 items):',
        options2, default= ['Fat [%]',  'Protein [%]', 'GWP, kg CO2-EQ/kg product'],
              max_selections = 3)
    
    options_food2 = list(df_studies.index.unique())

    choice_food2 = st.multiselect(
        'Please select the protein sources you want to compare (max. 3 items):',
        options_food2, default=[ 'grasshopper', 'snail'],
        max_selections = 3)


    df_plot = df_studies.loc[choice_food2][parameters2].reset_index(drop = True).T


    fig = bar(df_plot,
    #              x='ingredient',
    #              y='value', 
                barmode="group",
                facet_col=df_plot.index, 
                facet_col_spacing=0.06,
                color_discrete_sequence=oslo_rgb[:10],
        color_continuous_scale=None, orientation = 'v'
        , title = 'Values for chosen parameter {}<br>for studies about {}.<br>The different studies are placed on the x-axis, encoded by numbers (see legend) and sorted<br>in ascending order for each subplot. See studies dictionary for the numbers.'.format(parameters2, choice_food2))
    fig.update_xaxes(matches=None, showticklabels=True)
    fig.update_yaxes(matches=None, showticklabels=True)
    fig.update_layout(   autosize=False,
                    width=800,
                    height=800,
                    margin={'t': 200},

                legend=dict(title = 'Study number',
                        )
            )
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    st.plotly_chart(fig, use_container_width=False)