import pandas as pd
import os
import re
from minio_utils import MinioUtils


class AnalyticsService:
    def __init__(self, minio_access_key="", minio_secret_key="", bucket_name=""):
        self.minio_secret_key = minio_secret_key
        self.minio_access_key = minio_access_key
        self.bucket_name = bucket_name
        self.df = pd.DataFrame([])
        self.response_list = []
        self.minioUtilsObj = MinioUtils(
            bucket_name=self.bucket_name,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
        )

    def __clean_movie_id(self, movie_id):
        movie_id = re.sub(r"[a-zA-Z]", "", movie_id)
        return movie_id

    def create_movie_id(self):
        self.df.loc[:, "movie_id"] = self.df.ID.apply(self.__clean_movie_id)
        return self.df

    def create_dataframe_from_json(self, file_name):
        json_response = self.minioUtilsObj.download_from_storage(
            "all_movies/" + file_name
        )
        df = pd.DataFrame(json_response["Movies"])
        self.df = df[["ID", "Title", "Year"]]
        self.df = self.create_movie_id()
        return self.df

    def create_dataframe_from_multiple_json(self, prefix):
        objects_movie_data = self.minioUtilsObj.minioClient.list_objects(
            self.bucket_name, prefix=prefix
        )

        for obj in objects_movie_data:
            response = self.minioUtilsObj.download_from_storage(obj.object_name)
            self.response_list.append(response)
        self.df = pd.DataFrame(self.response_list)
        self.df = self.df[["ID", "Title", "Director", "Year", "Price"]]
        self.df = self.create_movie_id()
        self.df.Price = self.df.Price.astype(float)
        return self.df

    def find_cheapest_movie(self, df_obj):
        df_obj = df_obj.sort_values(by="Price", ascending=True, ignore_index=True)
        # cheapest movie and director will be at the top of the dataframe now
        # so we can just return that
        cheapest_obj = {
            "title": df_obj.Title[0],
            "price": df_obj.Price[0],
        }
        return cheapest_obj

    def find_cheapest_director(self, df_obj):
        # we have grouped by directors and taken the sum of their prices
        # this will give us the cumulative price of each director
        # we can then sort it and get the cheapest director
        df_obj = df_obj.groupby("Director")["Price"].sum().reset_index()
        df_obj = df_obj.sort_values(by="Price", ignore_index=True)
        cheapest_obj = {
            "director": df_obj.Director[0],
            "price": df_obj.Price[0],
        }
        return cheapest_obj
