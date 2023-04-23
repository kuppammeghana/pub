import streamlit as st

st.title("Innomatics Pub Project App")
st.snow()

btn_click = st.button("Click Me!")

if btn_click == True:
    st.subheader("You clicked me :smile:")
    st.balloons()