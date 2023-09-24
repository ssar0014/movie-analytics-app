import pandas as pd
import os
from minio_utils import MinioUtils


class AnalyticsService:
    def __init__(self, file_name="", minio_access_key="", minio_secret_key=""):
        self.file_name = file_name
        self.minio_secret_key = minio_secret_key
        self.minio_access_key = minio_access_key

    def create_dataframe_from_json(self):
        minioUtilsObj = MinioUtils(
            bucket_name="datalake",
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
        )
        json_response = minioUtilsObj.download_from_storage(self.file_name)
        df = pd.DataFrame(json_response["Movies"])
        return df
