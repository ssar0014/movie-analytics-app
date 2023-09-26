import os
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
from dashboard_utils import DashboardUtils

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
minio_access_key = os.environ.get("MINIO_ACCESS_KEY")
minio_secret_key = os.environ.get("MINIO_SECRET_KEY")
flask_base_url = os.environ.get("FLASK_BASE_URL")

st.title("Movie Information App")
st.markdown("_Working Prototype v0.1_")

# Connect and fetch data from the cinemaworld database
cinemaworld_conn = st.toggle("Find Movies On The Cinemaworld Database")
filmworld_conn = st.toggle("Find Movies On The Filmworld Database")

if cinemaworld_conn:
    st.info("Connected to the Cinemaworld DB", icon="ℹ️")
    dashboardUtilsObj = DashboardUtils(base_url=flask_base_url)

    st.info("Extract Data from the Cinemaworld Database", icon="ℹ️")
    cw_cheapest_movie, cw_cheapest_dir = dashboardUtilsObj.on_activate(
        minio_access_key=minio_access_key,
        minio_secret_key=minio_secret_key,
        dbname="cinemaworld",
    )

# Connect and fetch data from the filmworld database
if filmworld_conn:
    st.info("Connected to the Filmworld DB", icon="ℹ️")
    dashboardUtilsObj = DashboardUtils(base_url=flask_base_url)

    st.info("Extract Data from the Filmworld Database", icon="ℹ️")
    fw_cheapest_movie, fw_cheapest_dir = dashboardUtilsObj.on_activate(
        minio_access_key=minio_access_key,
        minio_secret_key=minio_secret_key,
        dbname="filmworld",
    )

if cinemaworld_conn and filmworld_conn:
    st.header("**Overall Cheapest Movie Across Both Databases...**")
    if cw_cheapest_movie["price"] < fw_cheapest_movie["price"]:
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.header(":orange[Cheapest Movie:]")
                st.write(f"{cw_cheapest_movie['title']}")
                image = Image.open("./attackOfTheClones.jpg")
                st.image(image)
            with col2:
                st.header(":orange[Price :moneybag: :]")
                st.write(f"{cw_cheapest_movie['price']}")
    else:
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.header(":orange[Cheapest Movie:]")
                st.write(f"{fw_cheapest_movie['title']}")

            with col2:
                st.header(":orange[Price :moneybag: :]")
                st.write(f"{fw_cheapest_movie['price']}")

    st.header("**Overall Cheapest Director Across Both Databases...**")
    if cw_cheapest_dir["price"] < fw_cheapest_dir["price"]:
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.header(":orange[Cheapest Movie Provider (Director):]")
                st.write(f"{cw_cheapest_dir['director']}")
            with col2:
                st.header(":orange[Price :moneybag: :]")
                st.write(f"{cw_cheapest_dir['price']}")
    else:
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.header(":orange[Cheapest Movie Provider (Director):]")
                st.write(f"{fw_cheapest_dir['director']}")
            with col2:
                st.header(":orange[Price :moneybag: :]")
                st.write(f"{fw_cheapest_dir['price']}")
