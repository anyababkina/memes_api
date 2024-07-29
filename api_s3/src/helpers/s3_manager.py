import boto3
from fastapi import HTTPException
from loguru import logger
from botocore.exceptions import NoCredentialsError, ClientError

from src.helpers.exceptions import S3Error
from src.settings import s3_settings


class S3FileManager:
    s3 = boto3.client(
        's3',
        endpoint_url=s3_settings.ENDPOINT_URL,
        aws_access_key_id=s3_settings.ACCESS_KEY,
        aws_secret_access_key=s3_settings.SECRET_ACCESS_KEY
    )

    bucket_name = s3_settings.BUCKET_NAME

    @classmethod
    def create_bucket(cls, bucket_name):
        try:
            cls.s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    @classmethod
    def upload_file(cls, file_content, object_key):
        try:
            cls.s3.put_object(Bucket=cls.bucket_name, Key=object_key, Body=file_content)
            object_url = f"https://{cls.bucket_name}.s3.amazonaws.com/{object_key}"
            logger.info(f"File uploaded successfully. URL: {object_url}")
            return object_url
        except NoCredentialsError:
            logger.error("Credentials not available.")
            raise S3Error
        except Exception as e:
            logger.error(f"Error uploading file to bucket '{cls.bucket_name}': {str(e)}")
            raise S3Error

    @classmethod
    def download_file(cls, object_key, local_path):
        try:
            cls.s3.download_file(cls.bucket_name, object_key, local_path)
            logger.success(f"File '{object_key}' downloaded successfully to '{local_path}'.")
        except NoCredentialsError:
            logger.error("Credentials not available.")
            raise S3Error
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.error(f"File '{object_key}' not found in bucket '{cls.bucket_name}'.")
                raise HTTPException(status_code=404, detail="File not found")
        except Exception as e:
            if e.__class__.__name__ == 'HTTPException':
                raise
            logger.error(f"Error downloading file '{object_key}' from bucket '{cls.bucket_name}': {str(e)}")
            raise S3Error

    @classmethod
    def delete_file(cls, object_key):
        try:
            cls.s3.delete_object(Bucket=cls.bucket_name, Key=object_key)
            logger.success(f"File '{object_key}' deleted successfully from bucket '{cls.bucket_name}'.")
        except NoCredentialsError:
            logger.error("Credentials not available.")
            raise S3Error
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                pass
            else:
                raise Exception
        except Exception as e:
            logger.error(f"Error deleting file '{object_key}' from bucket '{cls.bucket_name}': {str(e)}")
            raise S3Error



# S3FileManager.create_folder('test')
# S3FileManager.upload_file('orig_image_project334_.png', 'test/orig_image_project334_.png')
# S3FileManager.upload_file('result_density124_project334_.png', 'test/orig_image_project334_.png')