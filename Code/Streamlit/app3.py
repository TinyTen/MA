import streamlit as st

import math as math
import pandas as pd
import numpy as np
# import seaborn as sns
import streamlit as st
from cmcrameri import cm
from PIL import Image

import matplotlib.pyplot as plt
from plotly.express import bar, scatter, colors, imshow, pie
from colors_cameri import davos, oslo

def app():
    st.title('Evaluating Recipes')
    st.text('In this section you can create your own recipes and evaluate the composition \nof the parameters of interest.')

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
    df_dapro = pd.read_excel('Code/df_dapro_en.xlsx')
    df_dapro.rename(columns= {'Unnamed: 0': ' '}, inplace=True)
    df_dapro.set_index(' ', drop = True, inplace=True)

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
    
    def calculate_recipe(df, ingredients, proportions):
        df.loc['recipe'] = 0
        sum_recipe = df.loc['recipe']
        dict_recipe = dict(zip(ingredients, proportions))
        for key in dict_recipe:
            sum_recipe += (dict_recipe[key] * (df.loc[key]/100))
        sum_recipe_per100 = (sum_recipe/sum(dict_recipe.values()))*100
        return pd.DataFrame(sum_recipe_per100)

# calculation
    
    options_food = list(df_dapro.index)

    choice_food = st.multiselect(
        'Please select the food items you want to use in the recipe:',
        options_food, default=['Apple', 'Cashew nut', 'Chicken'])

    ingredients = choice_food

    proportions = np.zeros(len(ingredients))

    for i in range(len(ingredients)):
        proportions[i] = st.number_input('Insert a amount for ingredient {} in g.'.format(i+1))


    # dict_recipe = dict(zip(ingredients, proportions))

    # df_recipe = calculate_recipe(df_dapro.select_dtypes(include=np.number),
    #                          ingredients = ingredients, 
    #                          proportions = proportions)


# figure1
    fig1 = pie(names = ingredients, values = proportions, 
        color_discrete_sequence=oslo_rgb[1::3], 
            title = ('Currently Chosen Composition of the Recipe: Proportions in Percent of Weight.<br>Sum of the Recipe is {}g.').format(sum(proportions)))
    st.plotly_chart(fig1, use_container_width=False)

# figure 2


    options = ['Protein_g/g', 'Eutrophying emissions per 100g (gPO₄eq per 100g}',
       'Land use per 100g (m² per 100g)', 
                'Freshwater withdrawals per 100g (liters per 100g)' , 'Alanin_mg/100g', 'Arginin_mg/100g', 'Cystein_mg/100g', 'Histidin_mg/100g', 
        'Isoleucin_mg/100g',  'Lysin_mg/100g', 'Vitamin B12-Cobalamin_μg/100g', 'Sodium_mg/100g', 'Cholesterin_mg/100g', 'Fat_g/100g', 'Simply unsaturated fatty acids mg/100g',]

    parameters = st.multiselect(
        'Please select the paramters you want to compare:',
        options, default=['Protein_g/g',  'Freshwater withdrawals per 100g (liters per 100g)'],
              max_selections=3)
    
    df_plot = (df_dapro.loc[ingredients][parameters].mul(proportions, axis='rows')/sum(proportions)).T.reset_index()

    fig2 = bar(df_plot,
    #              x='ingredient',
    #              y='value', 
                barmode="stack",
                facet_col='index', 
                color_discrete_sequence=oslo_rgb[0::3],
                                        facet_col_spacing=0.1,
        color_continuous_scale=None,
    width = 900, height = 600
            ,   )

    title = 'Display of the chosen parameter for the current recipe (per 100g of total recipe): <br>The absolute contribution of all ingredients is shown. <br>Items can be turned on or off by clicking in the item in the legend.'
        

    fig2.update_layout(title_text=title, title_y = 0.95, 
            margin={'t': 120})
    fig2.update_xaxes(matches=None,showticklabels=False, side = "bottom", color = 'white', )
    fig2.update_layout(  xaxis_title=' ')

    fig2.update_yaxes(matches=None, showticklabels=True)
    fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    st.plotly_chart(fig2, use_container_width=False)

    # figure 2



    st.subheader('Amino Acid Score')

    st.text('''
    In addition to the previous visualisation, the AminoAcidScore for the recipe is \n
    presented here, since the database is focussed on proteins.''')

    # calculation
    df_recipe_prot = (df_dapro.loc[ingredients][[
    'Histidin_mg/100g',
    'Isoleucin_mg/100g',
    'Leucin_mg/100g',
    'Lysin_mg/100g',
    'Threonin_mg/100g',
    'Tryptophan_mg/100g',
    'Valin_mg/100g',
        'Methionin_mg/100g',
        'Cystein_mg/100g',
        'Alanin_mg/100g',
        'Tyrosin_mg/100g',
        'Protein_g/g']]).T
    
    df_recipe_prot.loc['Methionine+Cysteine(SAA)_mg/100g'] = df_recipe_prot.loc['Methionin_mg/100g'] + df_recipe_prot.loc['Cystein_mg/100g']
    df_recipe_prot.loc['Phenylalanine+Tyrosine_mg/100g'] = df_recipe_prot.loc['Alanin_mg/100g'] + df_recipe_prot.loc['Tyrosin_mg/100g']

    # reference values essential amino acids: https://www.fao.org/ag/humannutrition/35978-02317b979a686a57aa4593304ffc17f06.pdf, TABLE 5:
    ess_aa= pd.read_excel("Code/EssentialAminoAcids.xlsx", sheet_name = 'Sheet2')
    ess_aa.set_index('Amino acid', inplace=True)

    df_aa_sep = df_recipe_prot.merge(ess_aa, right_on= ess_aa.index, left_index=True )
    for ingredient in ingredients:
        df_aa_sep[ingredient] = df_aa_sep[ingredient]/df_aa_sep['mg/g crude protein']

    df_aa_sep.drop(['key_0', 'mg/g crude protein'], axis =1, inplace = True)
    df_aa_sep = df_aa_sep.mul(proportions, axis='columns')/sum(proportions)/sum(df_dapro.loc[ingredients]['Protein_g/g'].mul(proportions, axis='rows')/sum(proportions))

    new_index = []
    for index in df_aa_sep.index:
        new_index.append(index.split('_')[0])
        
    df_aa_sep.index = new_index
    
    #figure
    import plotly.graph_objects as go


    fig3 = go.Figure()

    i = 0

    for ingredient in ingredients:

        fig3.add_trace(go.Barpolar(
            r = list(df_aa_sep[ingredient]),
            theta=list(df_aa_sep.index),
            name = ingredient,
            marker_color=oslo_rgb[i],

            marker_line_color="black",
            hoverinfo = ['all'],
            opacity=0.7   
        ))
        i += 2
        
   
    fig3.update_layout(
        title='Amino Acids Scores of all Essential Amino Acids: To be complete, the protein needs to reach 1 (outer border) <br>for all Amino Acids. The contribution of all recipe compounds is shown.',
        font_size=12,
        legend_font_size=15,
        polar_angularaxis_rotation=90,
        width=900,
        height=900,
        
        polar = dict(
                bgcolor = "rgb(223, 223, 223)",
                angularaxis = 
                    dict(
                        linewidth = 3,
                        showline=True,
                        linecolor='black'
                        ),
            radialaxis = 
                    dict( tickmode = 'array', 
                        range=[0, 1],
                        tickvals = [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2],       
                        showline = True,
                        linewidth = 2,
                        gridcolor = "white",
                        gridwidth = 2,
                        )
                    ),

                )

    fig3.update_layout(
                          margin={'t': 200})
    st.plotly_chart(fig3, use_container_width=False)
