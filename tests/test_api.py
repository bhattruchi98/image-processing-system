import pytest
from app import create_app, db
from app.models import Request, Product

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_upload(client):
    response = client.post('/upload', data={
        'file': (open('tests/sample.csv', 'rb'), 'sample.csv')
    })
    assert response.status_code == 202
    data = response.get_json()
    assert 'request_id' in data

def test_status(client):
    response = client.get('/status/1')
    assert response.status_code == 404

    new_request = Request(status='Pending')
    db.session.add(new_request)
    db.session.commit()

    response = client.get(f'/status/{new_request.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Pending'
