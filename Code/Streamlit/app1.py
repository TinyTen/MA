import streamlit as st
def app():
    """
Streamlit Application Food Sustainability
Autor: Christina Koeck
Date: 02/2023
"""

    # https://docs.streamlit.io/library/api-reference

    # if imports of seaborn and plotly do not work, try update the packages and restart computer (this version works with plotly==5.13.1, seaborn==0.12.1, streamlit==1.13.0 )
    import math as math
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import streamlit as st
    from cmcrameri import cm
    from PIL import Image

    import matplotlib.pyplot as plt
    from plotly.express import bar, scatter, colors



    # # Configuration
    st.title('Overview')



    

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

    col1, col2 = st.columns(2)


    ## read in data
    df_food = pd.read_excel("Code/df_dapro_en.xlsx")
    df_food.rename(columns= {'Unnamed: 0': ' '}, inplace=True)
    df_food.set_index(' ', drop = True, inplace=True)

    zhaw_color = (0.00000 , 0.39216 , 0.65098)

    ## create df with missing data
    missing = df_food.isna().sum()[df_food.isna().sum() > 0]

    
    with col1:
        st.image("ZHAW_Logo.png", width=300)




    with col2:
        st.title('Welcome to DaPro, the ZHAW protein database')
        st.metric(label="Count of parameters in database", value=len(df_food.columns))
        st.metric(label="Count of food items in database", value=len(df_food))
            # #plotly missing
    #     fig2 = bar(y = missing.index , x = missing)
    #     st.plotly_chart(fig2, use_container_width=True)

                #seaborn missing
    st.subheader('Currently, several food items lack information for some parameters. The graph shows which parameters have missing values and how many of them are missing.')
    fig1 = plt.figure(figsize=(30, 30))
    sns.barplot(y = missing.index , x = missing, color=zhaw_color)
    plt.yticks(fontsize=60)
    plt.xticks(fontsize=60)
    plt.xlabel('Count of missing values per parameter', fontsize=60)

    sns.despine(left=True, bottom=True)
    st.pyplot(fig1)


    st.subheader('Overview over the database')
    st.text('''
            Here all food items in the database are presented in a 3D plot. You can choose three\n
            parameters which are then displayed on the x-axis, the y-axis and as size of the \n
            bubbles.''')

        # chose the dimensions to display

    size = st.selectbox('Please select the paramter of which you want to see the distribution',
        ['Protein_g/g', 'Alanin_mg/100g', 'Arginin_mg/100g',  'Valin_mg/100g', 'Fat_g/100g', 'Cholesterin_mg/100g'],
    )

    x = st.selectbox('Please select the paramter of which you want to see the distribution',
        [  'Energy (kilojoule) _kJ/100g', 'Protein_g/g', 'Alanin_mg/100g', 'Vitamin B12-Cobalamin_μg/100g','Fat_g/100g', 'Simply unsaturated fatty acids mg/100g'],
    )

    y = st.selectbox('Please select the paramter of which you want to see the distribution',
        ['Lysin_mg/100g', 'Saturated fatty acids_mg/100g','Vitamin B12-Cobalamin_μg/100g', 'Fat_g/100g', 'Eutrophying emissions per 100g (gPO₄eq per 100g}',
       'Freshwater withdrawals per 100g (liters per 100g)',
       'Land use per 100g (m² per 100g)', ],
    )

    df = df_food 
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

    fig4 = scatter(df, 
                    y=y,
                    size= size,
                    x = x,
                    color = df.index, 
            hover_name=df.index, 
                    size_max=60,
            color_discrete_sequence = oslo_rgb,
                    title = 'Distribution of the food products in the database in regard to the chosen parameters.'
                    )
    st.plotly_chart(fig4, use_container_width=True)
                                
