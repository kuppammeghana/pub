import streamlit as st
import pandas as pd
from PIL import Image, ImageEnhance
import numpy as np
import os
import plotly.graph_objs as go

st.set_page_config(page_title="Pub Finder App",
                   page_icon=":🍺:",
                   layout="centered")

# absolute path to this file
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# absolute path to this file's root directory
PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
# absolute path of directory_of_interest
dir_of_interest = os.path.join(PARENT_DIR, "resources")

HOME_IMAGE_PATH = os.path.join(dir_of_interest, "images","pub.jpg")
LOCATIONS_IMAGE_PATH = os.path.join(dir_of_interest, "images", "pub_location.jpg")
NEAREST_IMAGE_PATH = os.path.join(dir_of_interest, "images", "pub_nearest.jpg")
DATA_PATH = os.path.join(dir_of_interest, "data", "pub_data.csv")

# st.markdown("<h1 style='color: red;'>Pub Finder App</h1>", unsafe_allow_html=True)

# Load home page image
home_img = Image.open(HOME_IMAGE_PATH)
enhancer = ImageEnhance.Contrast(home_img)
home_img = enhancer.enhance(1.5)

# Load locations page image
locations_img = Image.open(LOCATIONS_IMAGE_PATH)
enhancer = ImageEnhance.Contrast(locations_img)
locations_img = enhancer.enhance(1.5)

# Load nearest pub page image
nearest_img = Image.open(NEAREST_IMAGE_PATH)
enhancer = ImageEnhance.Contrast(nearest_img)
nearest_img = enhancer.enhance(1.5)

# Load data
df = pd.read_csv(DATA_PATH)

# Page Number 1 - Home Page
def home():
    st.markdown("<h1 style='color: blue; font-style: italic;'>Pub Finder App</h1>", unsafe_allow_html=True)
    st.image(home_img, caption=None, width=500, use_column_width=200, clamp=False, channels="RGB", output_format="auto")
    st.write("This app allows you to find pubs in the United Kingdom (UK) and discover their locations.")
    st.write(f'We have {len(df)} pub locations in our database.')
    st.write("- Number of unique local authorities:", df["local_authority"].nunique())
    st.write("- Number of unique postal codes:", df["postcode"].nunique())
    st.write('Use the navigation sidebar to explore the app.')

# Page Number 2 - Pub Locations
def pub_locations():
    st.markdown("<h1 style='color: red; font-style: italic;'>Pub Locations</h1>", unsafe_allow_html=True)
    st.image(locations_img, caption=None, width=500, use_column_width=200, clamp=False, channels="RGB", output_format="auto")
    location_type = st.radio('Search by:', ('Postal Code', 'Local Authority'))
    if location_type == 'Postal Code':
        location = st.text_input('Enter Postal Code (e.g., LL13 7LU):')
        pubs = df[df['postcode'] == location]
    else:
        location = st.selectbox('Select Local Authority:', df['local_authority'].unique())
        pubs = df[df['local_authority'] == location]
    st.write(f'We found {len(pubs)} pubs in {location}.')
    st.map(pubs[['latitude', 'longitude']])

# Page Number 3 - Find the Nearest Pub
def nearest_pub():
    st.markdown("<h1 style='color: green; font-style: italic;'>Find the Nearest Pub</h1>", unsafe_allow_html=True)
    st.image(nearest_img, caption=None, width=500, use_column_width=200, clamp=False, channels="RGB", output_format="auto")
    lat = float(st.text_input('Enter your Latitude:', value=51.5074))
    lon = float(st.text_input('Enter your Longitude:', value=-0.1278))
    n_pubs = st.slider('Number of nearest pubs to display:', 1, 10, 5)

    pubs = df[['name', 'latitude', 'longitude']]
    pubs['distance'] = np.sqrt((pubs['latitude'] - lat) ** 2 + (pubs['longitude'] - lon) ** 2)
    pubs = pubs.sort_values('distance').head(n_pubs)

    fig = go.Figure(go.Scattermapbox(
        lat=pubs['latitude'],
        lon=pubs['longitude'],
        mode='markers',
        marker=dict(
            size=10,
            color='blue'
        ),
        text=pubs['name'],
        hoverinfo='text'
    ))

    fig.update_layout(
        mapbox=dict(
            center=dict(lat=lat, lon=lon),
            style='open-street-map',
            zoom=12
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=600
    )

    st.plotly_chart(fig)
    st.write(f'The {n_pubs} nearest pubs to your location:')
    for i, row in pubs.iterrows():
        st.write(f"{row['name']} ({row['distance']:.2f} km)")

# App
def app():
    st.sidebar.title('Navigation')
    pages = ['Home', 'Pub Locations', 'Find the Nearest Pub']
    page = st.sidebar.selectbox('Select a page:', pages)
    if page == 'Home':
        home()
    elif page == 'Pub Locations':
        pub_locations()
    elif page == 'Find the Nearest Pub':
        nearest_pub()

if __name__ == '__main__':
    app()