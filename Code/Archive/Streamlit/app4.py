import streamlit as st
def app():
    st.title('APP4')
    st.write('Welcome to app4')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("A cat")
        st.image("..\ZHAW\ZHAW_Logo.png")

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")