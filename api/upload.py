import logging

from pathlib import Path

import boto3

BUCKET_NAME = "videos"

s3 = boto3.resource("s3")
bucket = s3.Bucket(BUCKET_NAME)


def create_bucket():
    logging.debug(f"Creating bucket {BUCKET_NAME}")
    if BUCKET_NAME in map(lambda b: b.name, iter(s3.buckets.all())):
        logging.debug(f"\tBucket {BUCKET_NAME} already exists; proceeding")
    else:
        bucket.create()
        logging.warning(f"New Bucket {BUCKET_NAME} created")

    return None


def upload(path: Path) -> str:
    key = path.name
    bucket.upload_file(path, key)
    return key
