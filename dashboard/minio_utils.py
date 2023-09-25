from minio import Minio
from minio.error import S3Error
import json
import io
import os
import requests


class MinioUtils:
    def __init__(self, bucket_name="", access_key="", secret_key="", secure=False):
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.minioClient = Minio(
            "minio:9000",
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False,
        )

    def upload_to_storage(self, json_data, prefix, obj_name):
        found = self.minioClient.bucket_exists(self.bucket_name)
        if not found:
            self.minioClient.make_bucket(self.bucket_name)

        json_data = json.dumps(json_data)
        object_name = obj_name

        try:
            self.minioClient.put_object(
                self.bucket_name,
                prefix + object_name,
                io.BytesIO(json_data.encode("utf-8")),
                len(json_data),
                content_type="application/json",
            )
        except S3Error as e:
            print(e)

    def download_from_storage(self, obj_name):
        found = self.minioClient.bucket_exists(self.bucket_name)
        if found:
            try:
                response = self.minioClient.get_object(self.bucket_name, obj_name)
                response = eval(response.data)  # convert bytes object to dictionary
                return response
            except S3Error as e:
                print(e)


if __name__ == "__main__":
    minioObj = MinioUtils("datalake", "user", "password")
    a = {"1": 1, "2": 2}
    minioObj.upload_to_storage(a, "aaa", "a.json")
