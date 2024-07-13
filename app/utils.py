import requests
from PIL import Image
from io import BytesIO
import os
import boto3

def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    path = os.path.join('/tmp', os.path.basename(url))
    img.save(path)
    return path

def compress_image(image_path):
    img = Image.open(image_path)
    compressed_path = image_path.replace('.jpg', '_compressed.jpg')
    img.save(compressed_path, quality=50)
    return compressed_path

def upload_image(image_path):
    s3 = boto3.client('s3')
    bucket = 'your-s3-bucket'
    key = os.path.basename(image_path)
    s3.upload_file(image_path, bucket, key)
    return f"https://{bucket}.s3.amazonaws.com/{key}"
