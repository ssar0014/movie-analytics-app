from minio_utils import MinioUtils
import json
import io
import os
import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
minio_access_key = os.environ.get("MINIO_ACCESS_KEY")
minio_secret_key = os.environ.get("MINIO_SECRET_KEY")


st.title("Movie Information App")
api_endpoint = "http://127.0.0.1:5000/get_movie_info/filmworld/0076759"


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
if st.button("Get All Movies"):
    # initialize the minio helper object
    minioUtilsObj = MinioUtils(
        bucket_name="datalake", access_key=minio_access_key, secret_key=minio_secret_key
    )
    st.write("Fetching movies...")

    # call the flask api
    movies = get_movies()
    object_name = "all_movies.json"
    minioUtilsObj.upload_to_storage(json_data=movies, obj_name=object_name)
    st.write(movies)
    st.write(
        f"JSON response uploaded to {minioUtilsObj.bucket_name}/{object_name} successfully."
    )
