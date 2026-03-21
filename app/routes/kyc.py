from flask import Blueprint, request, jsonify
from app import db
from app.models import Customer, AuditLog
from app.services.risk_engine import assess_customer
from datetime import date, datetime

kyc_bp = Blueprint('kyc', __name__)


@kyc_bp.route('/submit', methods=['POST'])
def submit_kyc():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['full_name', 'email', 'date_of_birth', 'nationality', 'is_pep', 'documents_submitted']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    existing = Customer.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'error': 'Customer with this email already exists'}), 409

    dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    assessment = assess_customer(
        nationality=data['nationality'],
        is_pep=data['is_pep'],
        age=age,
        documents_submitted=data['documents_submitted']
    )

    customer = Customer(
        full_name=data['full_name'],
        email=data['email'],
        date_of_birth=dob,
        nationality=data['nationality'],
        risk_level=assessment['risk_level'],
        is_verified=False
    )
    db.session.add(customer)
    db.session.commit()

    log = AuditLog(
        customer_id=customer.id,
        action='KYC_SUBMITTED',
        performed_by='system',
        details=f"Risk score: {assessment['score']}, Level: {assessment['risk_level']}"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        'message': 'KYC submission successful',
        'customer_id': customer.id,
        'risk_assessment': assessment
    }), 201