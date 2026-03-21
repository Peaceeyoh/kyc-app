import pytest
from app import create_app, db
from app.models import Customer


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_successful_kyc_submission(client):
    payload = {
        'full_name': 'John Doe',
        'email': 'john@example.com',
        'date_of_birth': '1990-01-15',
        'nationality': 'France',
        'is_pep': False,
        'documents_submitted': 2
    }
    response = client.post('/submit', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['risk_assessment']['risk_level'] == 'low'
    assert 'customer_id' in data


def test_high_risk_submission(client):
    payload = {
        'full_name': 'Ali Hassan',
        'email': 'ali@example.com',
        'date_of_birth': '1985-03-20',
        'nationality': 'Iran',
        'is_pep': True,
        'documents_submitted': 0
    }
    response = client.post('/submit', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['risk_assessment']['risk_level'] == 'high'


def test_missing_field_returns_400(client):
    payload = {
        'full_name': 'Jane Smith',
        'email': 'jane@example.com'
    }
    response = client.post('/submit', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'Missing field' in data['error']


def test_duplicate_email_returns_409(client):
    payload = {
        'full_name': 'John Doe',
        'email': 'duplicate@example.com',
        'date_of_birth': '1990-01-15',
        'nationality': 'France',
        'is_pep': False,
        'documents_submitted': 2
    }
    client.post('/submit', json=payload)
    response = client.post('/submit', json=payload)
    assert response.status_code == 409
    data = response.get_json()
    assert 'already exists' in data['error']