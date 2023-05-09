import app1
import app2
import app3
import app4
import streamlit as st



PAGES = {
    "Overview": app1,
    "Comparing Food Items": app2,
    "Evaluating Recipes": app3,
    "Protein Sources - Study Results": app4
}
st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()