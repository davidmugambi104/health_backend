from extension import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='staff')
    specialization = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', foreign_keys='Appointment.doctor_id')
    prescriptions = db.relationship('Prescription', backref='prescribing_doctor', foreign_keys='Prescription.prescribing_doctor_id')
    pending_actions = db.relationship('PendingAction', backref='assigned_user', foreign_keys='PendingAction.assigned_user_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    blood_type = db.Column(db.String(5))
    allergies = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    insurance_provider = db.Column(db.String(100))
    policy_number = db.Column(db.String(50))
    emergency_contact = db.Column(db.String(200))
    in_icu = db.Column(db.Boolean, default=False)
    on_ventilator = db.Column(db.Boolean, default=False)
    isolation_status = db.Column(db.String(20))
    telemedicine_ready = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient')
    prescriptions = db.relationship('Prescription', backref='patient')
    lab_results = db.relationship('LabResult', backref='patient')
    medical_records = db.relationship('MedicalRecord', backref='patient')
    vital_signs = db.relationship('VitalSign', backref='patient')
    notifications = db.relationship('Notification', backref='patient')
    enrollments = db.relationship('Enrollment', backref='patient')
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.date_of_birth:
            today = datetime.today().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled, no-show
    reason = db.Column(db.Text)
    notes = db.Column(db.Text)
    telemedicine = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medication_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    prescribing_doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prescribing_doctor_name = db.Column(db.String(100))
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LabResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    result_value = db.Column(db.String(100))
    date = db.Column(db.Date)
    critical_flag = db.Column(db.Boolean, default=False)
    acknowledged = db.Column(db.Boolean, default=False)
    ordering_provider = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date)
    notes = db.Column(db.Text)
    provider = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VitalSign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    heart_rate = db.Column(db.Integer)
    blood_pressure = db.Column(db.String(10))  # e.g., "120/80"
    oxygen_saturation = db.Column(db.Float)  # percentage
    temperature = db.Column(db.Float)  # Celsius
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))  # appointment, prescription, lab_result, etc.
    read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    code = db.Column(db.String(50), unique=True)
    patients = db.relationship('Patient', secondary='enrollment', backref='programs')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed, withdrawn
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=10)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PendingAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action_type = db.Column(db.String(50))  # follow_up, test, consultation, etc.
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)