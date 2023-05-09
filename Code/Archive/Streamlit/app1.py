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
    st.title('Welcome to ZHAW protein database')
    st.image("ZHAW/ZHAW_Logo.png", width=300)

    

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
    df_food = pd.read_excel("Code/Mockdata012.xlsx")
    ## create df with missing data
    missing = df_food.isna().sum()[df_food.isna().sum() > 0]

    
    with col1:
        st.metric(label="Count of samples in database", value=len(df_food))

            #seaborn missing
        st.subheader('Count of missing values')
        fig1 = plt.figure(figsize=(30, 30))
        sns.barplot(y = missing.index , x = missing, palette = cm.hawaii.colors)
        plt.yticks(fontsize=60)
        plt.xticks(fontsize=60)
        sns.despine(left=True, bottom=True)
        st.pyplot(fig1)

    with col2:
        st.metric(label="Count of parameters in database", value=len(df_food.columns))
            # #plotly missing
        fig2 = bar(y = missing.index , x = missing)
        st.plotly_chart(fig2, use_container_width=True)


    st.subheader('Distribution of data')

    parameter = st.selectbox('Please select the paramter of which you want to see the distribution',
        ['Category',  'Further processing needed',  'name', 'NutritionalForm', 'Allergens'],
    )
    
    fig3 = plt.figure(figsize=(10, 4))
    sns.countplot(df_food, x=parameter, palette = cm.hawaii.colors)
    sns.despine(left=True, bottom=True)
    st.pyplot(fig3)

    st.subheader('Distribution of parameters')
    column = st.selectbox('Please select the paramter of which you want to see the distribution',
        df_food.columns,
    )
    fig4 = plt.figure(figsize=(17, 10))
    sns.kdeplot(df_food[column], color = cm.hawaii.colors[5])
    # plt.yticks(fontsize=20)
    # plt.xticks(fontsize=20)
    sns.despine(left=True, bottom=True)
    st.pyplot(fig4)
                                
