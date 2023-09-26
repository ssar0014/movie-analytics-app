import os
import requests
import streamlit as st
from minio_utils import MinioUtils
from analytics import AnalyticsService


class DashboardUtils:
    def __init__(self, base_url="", max_retries=5):
        self.base_url = base_url
        self.max_retries = max_retries

    def get_movies(self, dbname):
        retries = 0
        while retries < self.max_retries:
            response = requests.get(self.base_url + f"get_all_movies/{dbname}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 500:
                retries += 1
            else:
                return {
                    "error": f"Error fetching data. Status code: {response.status_code}"
                }

    def get_pricing_data(self, dbname, movie_id):
        retries = 0
        while retries < self.max_retries:
            response = requests.get(
                self.base_url + f"get_movie_info/{dbname}/" + movie_id
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 500:
                retries += 1
            else:
                return {
                    "error": f"Error fetching data. Status code: {response.status_code}"
                }

    def on_activate(self, minio_access_key, minio_secret_key, dbname):
        # initialize the minio helper object
        prefix = "all_movies/"
        object_name = f"all_movies_{dbname}.json"
        minioUtilsObj = MinioUtils(
            bucket_name="datalake",
            access_key=minio_access_key,
            secret_key=minio_secret_key,
        )
        with st.spinner("Fetching Data..."):
            # call the flask api
            objects = minioUtilsObj.minioClient.list_objects(
                minioUtilsObj.bucket_name, prefix=prefix + object_name
            )
            num_objects = sum(1 for _ in objects)
            if num_objects > 0:
                st.write("Movies data already in data lake! Continuing...")
            else:
                movies = self.get_movies(dbname)
                minioUtilsObj.upload_to_storage(
                    json_data=movies, prefix=prefix, obj_name=object_name
                )
                st.info(
                    f"API response uploaded to minio bucket: {minioUtilsObj.bucket_name} successfully.",
                    icon="ℹ️",
                )
        analyticsObj = AnalyticsService(
            minio_access_key=minio_access_key,
            minio_secret_key=minio_secret_key,
            bucket_name=minioUtilsObj.bucket_name,
        )
        st.success("Done!")

        with st.expander("Data Preview"):
            all_movies_df = analyticsObj.create_dataframe_from_json(
                file_name=object_name
            )
            st.dataframe(all_movies_df)

        with st.spinner("Fetching Price Data..."):
            objects = minioUtilsObj.minioClient.list_objects(
                minioUtilsObj.bucket_name, prefix=f"movie_data/{dbname}/"
            )
            num_objects = sum(1 for _ in objects)
            if num_objects > 0:
                st.write("Price data already in data lake! Continuing...")
            else:
                for idx, json_data in enumerate(all_movies_df.values):
                    movie_id = json_data[-1]
                    movie_pricing_data = self.get_pricing_data(dbname, movie_id)
                    prefix = f"movie_data/{dbname}/"
                    object_name = movie_id + ".json"
                    minioUtilsObj.upload_to_storage(
                        json_data=movie_pricing_data,
                        prefix=prefix,
                        obj_name=object_name,
                    )

                st.info(
                    f"Pricing data stored in datalake.",
                    icon="ℹ️",
                )

        with st.expander("Pricing Data Preview"):
            all_movies_df_pricing = analyticsObj.create_dataframe_from_multiple_json(
                prefix=f"movie_data/{dbname}/"
            )
            st.dataframe(all_movies_df_pricing)

        st.markdown(f"**Found Cheapest Movie and Director from {dbname}...**")
        cheapest_dict_movie = analyticsObj.find_cheapest_movie(all_movies_df_pricing)
        st.write(f":orange[Cheapest Movie:] {cheapest_dict_movie['title']}")
        st.write(f":orange[Price :moneybag: :] {cheapest_dict_movie['price']}")

        st.markdown(f"**Found Cheapest Director from {dbname}...**")
        cheapest_dict_director = analyticsObj.find_cheapest_director(
            all_movies_df_pricing
        )
        st.write(
            f":orange[Cheapest Movie Provider (Director):] {cheapest_dict_director['director']}"
        )
        st.write(f":orange[Price :moneybag: :] {cheapest_dict_director['price']}")

        return (cheapest_dict_movie, cheapest_dict_director)
