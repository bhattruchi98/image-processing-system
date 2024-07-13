from datetime import datetime
from . import db

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    products = db.relationship('Product', backref='request', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    input_image_urls = db.Column(db.Text, nullable=False)  # Store comma-separated URLs
    output_image_urls = db.Column(db.Text, nullable=True)  # Store comma-separated URLs
