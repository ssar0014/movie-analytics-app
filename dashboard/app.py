from minio_utils import MinioUtils
from analytics import AnalyticsService
import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
minio_access_key = os.environ.get("MINIO_ACCESS_KEY")
minio_secret_key = os.environ.get("MINIO_SECRET_KEY")

st.title("Movie Information App")
st.markdown("_Working Prototype v0.1_")

cinemaworld_conn = st.toggle("Connect to the Cinemaworld DB")
if cinemaworld_conn:
    st.info("Connected to the Cinemaworld DB", icon="ℹ️")
    api_endpoint = "http://127.0.0.1:5000/get_all_movies/cinemaworld"

    # Function to make API call
    def get_movies():
        retries = 0
        max_retries = 10
        while retries < max_retries:
            response = requests.get(api_endpoint)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 500:
                retries += 1
            else:
                return {
                    "error": f"Error fetching data. Status code: {response.status_code}"
                }

    # Button to call API
    if st.button("Extract Data from the Cinemaworld Database"):
        # initialize the minio helper object
        minioUtilsObj = MinioUtils(
            bucket_name="datalake",
            access_key=minio_access_key,
            secret_key=minio_secret_key,
        )
        with st.spinner("Fetching Data..."):
            # call the flask api
            movies = get_movies()
        st.success("Done!")
        object_name = "all_movies.json"
        minioUtilsObj.upload_to_storage(json_data=movies, obj_name=object_name)
        st.info(
            f"JSON response uploaded to {minioUtilsObj.bucket_name}/{object_name} successfully.",
            icon="ℹ️",
        )
        analyticsObj = AnalyticsService(
            file_name=object_name,
            minio_access_key=minio_access_key,
            minio_secret_key=minio_secret_key,
        )
        st.dataframe(analyticsObj.create_dataframe_from_json())
