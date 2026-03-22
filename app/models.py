from app import db
from datetime import datetime, timezone


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    nationality = db.Column(db.String(60), nullable=False)
    risk_level = db.Column(db.String(20), default='pending')
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    documents = db.relationship('Document', backref='customer', lazy=True)
    audit_logs = db.relationship('AuditLog', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.full_name} - Risk: {self.risk_level}>'


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    def __repr__(self):
        return f'<Document {self.document_type} for customer {self.customer_id}>'


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    performed_by = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    details = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<AuditLog {self.action} at {self.timestamp}>'


from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    role = db.Column(db.String(20), default='analyst')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User {self.username} - Role: {self.role}>'