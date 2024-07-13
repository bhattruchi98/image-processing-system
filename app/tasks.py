from celery import Celery
from . import create_app, db
from .models import Request, Product
from .utils import download_image, compress_image, upload_image
import pandas as pd
import os

app = create_app()
celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def process_csv(request_id, csv_content):
    request = Request.query.get(request_id)
    if not request:
        return

    csv_data = StringIO(csv_content)
    df = pd.read_csv(csv_data)

    products = []
    for index, row in df.iterrows():
        product = Product(
            request_id=request_id,
            product_name=row['Product Name'],
            input_image_urls=row['Input Image Urls']
        )
        db.session.add(product)
        products.append(product)
    
    db.session.commit()

    for product in products:
        input_urls = product.input_image_urls.split(',')
        output_urls = []

        for url in input_urls:
            image_path = download_image(url)
            compressed_image_path = compress_image(image_path)
            output_url = upload_image(compressed_image_path)
            output_urls.append(output_url)

        product.output_image_urls = ','.join(output_urls)
    
    request.status = 'Completed'
    db.session.commit()
