import pytest
from app import create_app, db
from app.models import Customer, Document, AuditLog
from datetime import date


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


def test_create_customer(app):
    with app.app_context():
        customer = Customer(
            full_name='John Doe',
            email='john@example.com',
            date_of_birth=date(1990, 1, 15),
            nationality='French'
        )
        db.session.add(customer)
        db.session.commit()

        saved = Customer.query.filter_by(email='john@example.com').first()
        assert saved is not None
        assert saved.full_name == 'John Doe'
        assert saved.risk_level == 'pending'
        assert saved.is_verified == False


def test_customer_document_relationship(app):
    with app.app_context():
        customer = Customer(
            full_name='Jane Smith',
            email='jane@example.com',
            date_of_birth=date(1985, 6, 20),
            nationality='German'
        )
        db.session.add(customer)
        db.session.commit()

        doc = Document(
            customer_id=customer.id,
            document_type='passport',
            file_name='jane_passport.pdf'
        )
        db.session.add(doc)
        db.session.commit()

        assert len(customer.documents) == 1
        assert customer.documents[0].document_type == 'passport'


def test_audit_log_creation(app):
    with app.app_context():
        customer = Customer(
            full_name='Bob Wilson',
            email='bob@example.com',
            date_of_birth=date(1978, 3, 10),
            nationality='British'
        )
        db.session.add(customer)
        db.session.commit()

        log = AuditLog(
            customer_id=customer.id,
            action='KYC_SUBMITTED',
            performed_by='system'
        )
        db.session.add(log)
        db.session.commit()

        assert len(customer.audit_logs) == 1
        assert customer.audit_logs[0].action == 'KYC_SUBMITTED'