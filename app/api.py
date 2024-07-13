from flask import Blueprint, request, jsonify
from .validators import validate_csv
from .models import db, Request, Product

api_bp = Blueprint('api', __name__)

@api_bp.route('/upload', methods=['POST'])
def upload():
    csv_file = request.files.get('file')
    if not csv_file:
        return jsonify({"error": "No file provided"}), 400

    from .tasks import process_csv  # Import inside function to avoid circular import
    if not validate_csv(csv_file):
        return jsonify({"error": "Invalid CSV format"}), 400

    new_request = Request()
    db.session.add(new_request)
    db.session.commit()

    process_csv.delay(new_request.id, csv_file.read().decode('utf-8'))

    return jsonify({"request_id": new_request.id}), 202

@api_bp.route('/status/<int:request_id>', methods=['GET'])
def status(request_id):
    req = Request.query.get(request_id)
    if not req:
        return jsonify({"error": "Invalid request ID"}), 404

    products = Product.query.filter_by(request_id=request_id).all()
    products_data = [
        {
            "product_name": product.product_name,
            "input_image_urls": product.input_image_urls,
            "output_image_urls": product.output_image_urls
        } for product in products
    ]

    return jsonify({
        "request_id": req.id,
        "status": req.status,
        "products": products_data
    })
