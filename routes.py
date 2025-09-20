from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_, or_, desc, extract
from models import (
    User, Patient, Appointment, Prescription, LabResult, 
    MedicalRecord, VitalSign, Notification, 
    Program, Enrollment, Medication, PendingAction, AuditLog
)
from extension import db
import logging

logging.basicConfig(level=logging.INFO)

# Create blueprints for better organization
api = Blueprint('api', __name__)

# API Documentation route
@api.route('/api-docs')
def api_docs():
    rules = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint.startswith('api.'):  # Only include API blueprint routes
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))  # Exclude HEAD and OPTIONS
            rules.append({
                'endpoint': rule.endpoint,
                'methods': methods,
                'path': str(rule),
                'description': 'TODO: Add description'  # You can add manual descriptions if needed
            })
    # Sort by path for better readability
    rules.sort(key=lambda x: x['path'])
    return jsonify(rules)

# Authentication routes - STRIPPED OF AUTHENTICATION
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    logging.debug(f"Login request data: {data}")

    username = data.get('username')
    password = data.get('password')
    logging.debug(f"Attempting login for username: {username}")

    user = User.query.filter_by(username=username).first()
    logging.debug(f"User found: {user}")

    PLACEHOLDER_PASSWORD = "test1234"

    if user and (password == PLACEHOLDER_PASSWORD or user.check_password(password)):
        logging.info(f"Login successful for {username}")
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'email': user.email,
                'specialization': user.specialization
            }
        }), 200

    else:
        logging.error(f"Login failed for {username}")
        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401


@api.route('/logout')
def logout():
    return jsonify({'success': True})

# Dashboard routes
@api.route('/dashboard/stats')
def dashboard_stats():
    total_patients = Patient.query.count()
    todays_appointments = Appointment.query.filter(
        Appointment.date == date.today(),
        Appointment.status == 'scheduled'
    ).count()
    
    pending_prescriptions = Prescription.query.filter_by(status='pending').count()
    critical_labs = LabResult.query.filter_by(critical_flag=True, acknowledged=False).count()
    
    avg_heart_rate = db.session.query(func.avg(VitalSign.heart_rate)).scalar() or 72
    avg_oxygen = db.session.query(func.avg(VitalSign.oxygen_saturation)).scalar() or 98
    
    icu_count = Patient.query.filter_by(in_icu=True).count()
    ventilator_count = Patient.query.filter_by(on_ventilator=True).count()
    
    telemedicine_ready = Patient.query.filter_by(telemedicine_ready=True).count()
    telemedicine_appointments = Appointment.query.filter_by(
        telemedicine=True,
        date=date.today()
    ).count()
    
    return jsonify({
        'patient_stats': {
            'total': total_patients,
            'todays_appointments': todays_appointments,
            'pending_prescriptions': pending_prescriptions,
            'critical_labs': critical_labs
        },
        'health_metrics': {
            'heart_rate': round(avg_heart_rate),
            'blood_pressure': '120/80',
            'oxygen': round(avg_oxygen),
            'bmi': 24.2
        },
        'resource_status': {
            'icu': {'occupied': icu_count, 'total': 15},
            'ventilators': {'in_use': ventilator_count, 'total': 12},
            'isolation_beds': {'occupied': Patient.query.filter(Patient.isolation_status.isnot(None)).count(), 'total': 10}
        },
        'telemedicine': {
            'eligible': telemedicine_ready,
            'scheduled': telemedicine_appointments,
            'completed': Appointment.query.filter_by(
                telemedicine=True,
                status='completed',
                date=date.today()
            ).count()
        }
    })

@api.route('/dashboard/appointments')
def dashboard_appointments():
    appointments = Appointment.query.filter(
        Appointment.date == date.today()
    ).order_by(Appointment.start_time).all()
    
    result = []
    for appt in appointments:
        result.append({
            'id': f"A{appt.id:04d}",
            'time': appt.start_time.strftime('%H:%M'),
            'patient': appt.patient.name,
            'doctor': appt.doctor.username,
            'status': appt.status,
            'duration': int((appt.end_time.hour * 60 + appt.end_time.minute) - 
                           (appt.start_time.hour * 60 + appt.start_time.minute)) if appt.end_time else 30,
            'reason': appt.reason or 'Checkup',
            'notes': appt.notes or ''
        })
    
    return jsonify(result)

@api.route('/dashboard/doctors')
def dashboard_doctors():
    doctors = User.query.filter_by(role='doctor', active=True).all()
    
    result = []
    for doctor in doctors:
        patient_count = Appointment.query.filter_by(doctor_id=doctor.id).distinct(Appointment.patient_id).count()
        
        result.append({
            'id': doctor.id,
            'name': f"Dr. {doctor.username}",
            'specialty': doctor.specialization or 'General Medicine',
            'patients': patient_count,
            'rating': 4.8
        })
    
    return jsonify(result)

# Patient routes
@api.route('/patients', methods=['GET'])
def get_all_patients():
    try:
        patients = Patient.query.all()
        return jsonify([
            {
                'id': patient.patient_id,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'name': f"{patient.first_name} {patient.last_name}",
                'email': patient.email,
                'phone': patient.phone,
                'date_of_birth': patient.date_of_birth.isoformat(),
                'age': patient.age,
                'gender': patient.gender,
                'blood_type': patient.blood_type,
                'allergies': patient.allergies,
                'current_medications': patient.current_medications,
                'insurance_provider': patient.insurance_provider,
                'policy_number': patient.policy_number,
                'emergency_contact': patient.emergency_contact,
                'in_icu': patient.in_icu,
                'on_ventilator': patient.on_ventilator,
                'isolation_status': patient.isolation_status,
                'telemedicine_ready': patient.telemedicine_ready,
                'is_active': patient.is_active,
                'registered': patient.created_at.strftime('%b %d, %Y') if patient.created_at else None
            } for patient in patients
        ])
    except Exception as e:
        logging.error(f"Error fetching patients: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to fetch patients'}), 500


@api.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    logging.debug(f"Patient creation data: {data}")
    
    try:
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        date_of_birth = data.get('date_of_birth')
        gender = data.get('gender')
        blood_type = data.get('blood_type')
        allergies = data.get('allergies')

        if not all([first_name, last_name, email, phone, date_of_birth]):
            logging.error("Missing required fields")
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

        last_patient = Patient.query.order_by(desc(Patient.id)).first()
        new_id = f"PT-{1000 + (last_patient.id if last_patient else 0)}"

        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=dob,
            gender=gender,
            blood_type=blood_type,
            allergies=allergies,
            patient_id=new_id
        )
        patient.set_password('TempPassword123')

        db.session.add(patient)
        db.session.commit()

        logging.info(f"Patient created: {patient.patient_id}")
        return jsonify({
            'success': True,
            'patient': {
                'id': patient.patient_id,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'name': f"{patient.first_name} {patient.last_name}",
                'email': patient.email,
                'phone': patient.phone,
                'date_of_birth': patient.date_of_birth.isoformat(),
                'age': patient.age,
                'gender': patient.gender,
                'registered': patient.created_at.strftime('%b %d, %Y'),
                'conditions': [],
                'lastVisit': 'Never'
            }
        })
    except ValueError as e:
        logging.error(f"Invalid date format: {str(e)}")
        return jsonify({'success': False, 'message': 'Invalid date format for date_of_birth'}), 400
    except Exception as e:
        logging.error(f"Error creating patient: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@api.route('/patients/<patient_id>')
def get_patient(patient_id):
    patient = Patient.query.filter_by(patient_id=patient_id).first_or_404()
    
    records = MedicalRecord.query.filter_by(patient_id=patient.id).all()
    conditions = list(set([record.diagnosis for record in records]))
    
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(
        desc(Appointment.date)
    ).all()
    
    prescriptions = Prescription.query.filter_by(patient_id=patient.id).all()
    
    lab_results = LabResult.query.filter_by(patient_id=patient.id).all()
    
    return jsonify({
        'id': patient.patient_id,
        'first_name': patient.first_name,
        'last_name': patient.last_name,
        'name': f"{patient.first_name} {patient.last_name}",
        'email': patient.email,
        'phone': patient.phone,
        'date_of_birth': patient.date_of_birth.isoformat(),
        'age': patient.age,
        'gender': patient.gender,
        'blood_type': patient.blood_type,
        'allergies': patient.allergies,
        'current_medications': patient.current_medications,
        'insurance_provider': patient.insurance_provider,
        'policy_number': patient.policy_number,
        'emergency_contact': patient.emergency_contact,
        'registered': patient.created_at.strftime('%b %d, %Y') if patient.created_at else None,
        'conditions': conditions,
        'appointments': [{
            'id': appt.id,
            'date': appt.date.isoformat(),
            'time': appt.start_time.strftime('%H:%M'),
            'doctor': appt.doctor.username,
            'status': appt.status,
            'reason': appt.reason
        } for appt in appointments],
        'prescriptions': [{
            'id': rx.id,
            'medication_name': rx.medication_name,
            'dosage': rx.dosage,
            'start_date': rx.start_date.isoformat() if rx.start_date else None,
            'end_date': rx.end_date.isoformat() if rx.end_date else None,
            'status': rx.status
        } for rx in prescriptions],
        'lab_results': [{
            'id': lab.id,
            'test_name': lab.test_name,
            'result_value': lab.result_value,
            'date': lab.date.isoformat() if lab.date else None,
            'critical_flag': lab.critical_flag
        } for lab in lab_results]
    })

# Appointment routes
@api.route('/appointments')
def get_appointments():
    status_filter = request.args.get('status', 'all')
    date_filter = request.args.get('date', 'today')
    
    query = Appointment.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if date_filter == 'today':
        query = query.filter(Appointment.date == date.today())
    elif date_filter == 'upcoming':
        query = query.filter(Appointment.date >= date.today())
    
    appointments = query.order_by(Appointment.date, Appointment.start_time).all()
    
    result = []
    for appt in appointments:
        result.append({
            'id': f"A{appt.id:04d}",
            'time': appt.start_time.strftime('%H:%M'),
            'patient': appt.patient.name,
            'doctor': appt.doctor.username,
            'status': appt.status,
            'duration': int((appt.end_time.hour * 60 + appt.end_time.minute) - 
                           (appt.start_time.hour * 60 + appt.start_time.minute)) if appt.end_time else 30,
            'reason': appt.reason or 'Checkup',
            'notes': appt.notes or ''
        })
    
    return jsonify(result)

@api.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    
    patient_id = data.get('patient_id')
    if patient_id and patient_id.startswith('PT-'):
        patient = Patient.query.filter_by(patient_id=patient_id).first()
    else:
        patient = Patient.query.filter_by(name=patient_id).first()
    
    if not patient:
        return jsonify({'success': False, 'message': 'Patient not found'}), 404
    
    appointment_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    start_time = datetime.strptime(data.get('time'), '%H:%M').time()
    
    duration = data.get('duration', 30)
    end_time = (datetime.combine(date.today(), start_time) + timedelta(minutes=duration)).time()
    
    # Use a default doctor since we don't have authentication
    default_doctor = User.query.filter_by(role='doctor').first()
    if not default_doctor:
        return jsonify({'success': False, 'message': 'No doctor available'}), 404
    
    appointment = Appointment(
        patient_id=patient.id,
        doctor_id=default_doctor.id,
        date=appointment_date,
        start_time=start_time,
        end_time=end_time,
        status=data.get('status', 'scheduled'),
        reason=data.get('reason', ''),
        notes=data.get('notes', ''),
        telemedicine=data.get('telemedicine', False)
    )
    
    try:
        db.session.add(appointment)
        db.session.commit()
        
        notification = Notification(
            patient_id=patient.id,
            message=f"New appointment scheduled with Dr. {default_doctor.username} on {appointment_date} at {start_time}",
            notification_type='appointment'
        )
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({'success': True, 'appointment_id': appointment.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    data = request.get_json()
    appointment = Appointment.query.get_or_404(appointment_id)
    
    try:
        appointment.status = data.get('status', appointment.status)
        appointment.notes = data.get('notes', appointment.notes)
        appointment.reason = data.get('reason', appointment.reason)
        
        if 'date' in data:
            appointment.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'time' in data:
            appointment.start_time = datetime.strptime(data['time'], '%H:%M').time()
            duration = data.get('duration', 30)
            appointment.end_time = (datetime.combine(date.today(), appointment.start_time) + 
                                 timedelta(minutes=duration)).time()
        
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    try:
        db.session.delete(appointment)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Prescription routes
@api.route('/prescriptions')
def get_prescriptions():
    patient_id = request.args.get('patient_id')
    
    if patient_id:
        prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
    else:
        prescriptions = Prescription.query.all()
    
    result = []
    for rx in prescriptions:
        result.append({
            'id': rx.id,
            'patient_id': rx.patient.patient_id,
            'patient_name': rx.patient.name,
            'medication_name': rx.medication_name,
            'dosage': rx.dosage,
            'start_date': rx.start_date.isoformat() if rx.start_date else None,
            'end_date': rx.end_date.isoformat() if rx.end_date else None,
            'status': rx.status,
            'prescribing_doctor': rx.prescribing_doctor
        })
    
    return jsonify(result)

@api.route('/prescriptions', methods=['POST'])
def create_prescription():
    data = request.get_json()
    
    patient = Patient.query.filter_by(patient_id=data.get('patient_id')).first()
    if not patient:
        return jsonify({'success': False, 'message': 'Patient not found'}), 404
    
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date() if data.get('start_date') else None
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date() if data.get('end_date') else None
    
    # Use a default doctor since we don't have authentication
    default_doctor = User.query.filter_by(role='doctor').first()
    if not default_doctor:
        return jsonify({'success': False, 'message': 'No doctor available'}), 404
    
    prescription = Prescription(
        patient_id=patient.id,
        medication_name=data.get('medication_name'),
        dosage=data.get('dosage'),
        start_date=start_date,
        end_date=end_date,
        prescribing_doctor=default_doctor.username,
        notes=data.get('notes', ''),
        status=data.get('status', 'active')
    )
    
    try:
        db.session.add(prescription)
        db.session.commit()
        
        notification = Notification(
            patient_id=patient.id,
            message=f"New prescription for {data.get('medication_name')}",
            notification_type='prescription'
        )
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api.route('/prescriptions/<int:prescription_id>', methods=['PUT'])
def update_prescription(prescription_id):
    data = request.get_json()
    prescription = Prescription.query.get_or_404(prescription_id)
    
    try:
        prescription.medication_name = data.get('medication_name', prescription.medication_name)
        prescription.dosage = data.get('dosage', prescription.dosage)
        prescription.status = data.get('status', prescription.status)
        prescription.notes = data.get('notes', prescription.notes)
        
        if 'start_date' in data:
            prescription.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data:
            prescription.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Lab results routes
@api.route('/labresults')
def get_lab_results():
    patient_id = request.args.get('patient_id')
    critical_only = request.args.get('critical', False)
    
    query = LabResult.query
    
    if patient_id:
        patient = Patient.query.filter_by(patient_id=patient_id).first()
        if patient:
            query = query.filter_by(patient_id=patient.id)
    
    if critical_only:
        query = query.filter_by(critical_flag=True)
    
    results = query.order_by(desc(LabResult.date)).all()
    
    return jsonify([{
        'id': result.id,
        'patient_id': result.patient.patient_id,
        'patient_name': result.patient.name,
        'test_name': result.test_name,
        'result_value': result.result_value,
        'date': result.date.isoformat() if result.date else None,
        'critical_flag': result.critical_flag,
        'acknowledged': result.acknowledged
    } for result in results])

@api.route('/labresults', methods=['POST'])
def create_lab_result():
    data = request.get_json()
    
    patient = Patient.query.filter_by(patient_id=data.get('patient_id')).first()
    if not patient:
        return jsonify({'success': False, 'message': 'Patient not found'}), 404
    
    # Use a default provider since we don't have authentication
    default_provider = User.query.filter_by(role='doctor').first()
    if not default_provider:
        return jsonify({'success': False, 'message': 'No provider available'}), 404
    
    lab_result = LabResult(
        patient_id=patient.id,
        test_name=data.get('test_name'),
        result_value=data.get('result_value'),
        date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else date.today(),
        critical_flag=data.get('critical_flag', False),
        notes=data.get('notes', ''),
        ordering_provider=default_provider.username
    )
    
    try:
        db.session.add(lab_result)
        db.session.commit()
        
        if lab_result.critical_flag:
            notification = Notification(
                patient_id=patient.id,
                message=f"Critical lab result for {data.get('test_name')}: {data.get('result_value')}",
                notification_type='lab_result'
            )
            db.session.add(notification)
            db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Medical record routes
@api.route('/medical_records')
def get_medical_records():
    patient_id = request.args.get('patient_id')
    
    query = MedicalRecord.query
    if patient_id:
        patient = Patient.query.filter_by(patient_id=patient_id).first()
        if patient:
            query = query.filter_by(patient_id=patient.id)
    
    records = query.order_by(desc(MedicalRecord.date)).all()
    
    return jsonify([{
        'id': record.id,
        'patient_id': record.patient.patient_id,
        'patient_name': record.patient.name,
        'diagnosis': record.diagnosis,
        'date': record.date.isoformat() if record.date else None,
        'notes': record.notes,
        'provider': record.provider
    } for record in records])

@api.route('/medical_records', methods=['POST'])
def create_medical_record():
    data = request.get_json()
    
    patient = Patient.query.filter_by(patient_id=data.get('patient_id')).first()
    if not patient:
        return jsonify({'success': False, 'message': 'Patient not found'}), 404
    
    # Use a default provider since we don't have authentication
    default_provider = User.query.filter_by(role='doctor').first()
    if not default_provider:
        return jsonify({'success': False, 'message': 'No provider available'}), 404
    
    medical_record = MedicalRecord(
        patient_id=patient.id,
        diagnosis=data.get('diagnosis'),
        date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else date.today(),
        notes=data.get('notes', ''),
        provider=default_provider.username
    )
    
    try:
        db.session.add(medical_record)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Vital signs routes
@api.route('/vital_signs')
def get_vital_signs():
    patient_id = request.args.get('patient_id')
    
    query = VitalSign.query
    if patient_id:
        patient = Patient.query.filter_by(patient_id=patient_id).first()
        if patient:
            query = query.filter_by(patient_id=patient.id)
    
    vital_signs = query.order_by(desc(VitalSign.timestamp)).all()
    
    return jsonify([{
        'id': vital.id,
        'patient_id': vital.patient.patient_id,
        'patient_name': vital.patient.name,
        'heart_rate': vital.heart_rate,
        'blood_pressure': vital.blood_pressure,
        'oxygen_saturation': vital.oxygen_saturation,
        'temperature': vital.temperature,
        'timestamp': vital.timestamp.isoformat()
    } for vital in vital_signs])

@api.route('/vital_signs', methods=['POST'])
def create_vital_sign():
    data = request.get_json()
    
    patient = Patient.query.filter_by(patient_id=data.get('patient_id')).first()
    if not patient:
        return jsonify({'success': False, 'message': 'Patient not found'}), 404
    
    vital_sign = VitalSign(
        patient_id=patient.id,
        heart_rate=data.get('heart_rate'),
        blood_pressure=data.get('blood_pressure'),
        oxygen_saturation=data.get('oxygen_saturation'),
        temperature=data.get('temperature'),
        timestamp=datetime.strptime(data.get('timestamp'), '%Y-%m-%dT%H:%M:%S') if data.get('timestamp') else datetime.now()
    )
    
    try:
        db.session.add(vital_sign)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Notification routes
@api.route('/notifications')
def get_notifications():
    # Get all notifications since we don't have user authentication
    notifications = Notification.query.order_by(desc(Notification.timestamp)).all()
    
    return jsonify([{
        'id': note.id,
        'message': note.message,
        'timestamp': note.timestamp.isoformat(),
        'read': note.read,
        'type': note.notification_type
    } for note in notifications])

@api.route('/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    notification.read = True
    
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Analytics routes
@api.route('/analytics/patient_stats')
def patient_analytics():
    monthly_stats = db.session.query(
        extract('year', Patient.created_at).label('year'),
        extract('month', Patient.created_at).label('month'),
        func.count(Patient.id).label('count')
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    appointment_stats = db.session.query(
        Appointment.status,
        func.count(Appointment.id).label('count')
    ).group_by(Appointment.status).all()
    
    common_conditions = db.session.query(
        MedicalRecord.diagnosis,
        func.count(MedicalRecord.id).label('count')
    ).group_by(MedicalRecord.diagnosis).order_by(desc('count')).limit(10).all()
    
    return jsonify({
        'monthly_registrations': [{
            'month': f"{int(stat.year)}-{int(stat.month):02d}",
            'count': stat.count
        } for stat in monthly_stats],
        'appointment_statuses': [{
            'status': stat.status,
            'count': stat.count
        } for stat in appointment_stats],
        'common_conditions': [{
            'condition': cond.diagnosis,
            'count': cond.count
        } for cond in common_conditions]
    })

# Health program routes
@api.route('/programs')
def get_programs():
    programs = Program.query.all()
    
    return jsonify([{
        'id': program.id,
        'name': program.name,
        'description': program.description,
        'code': program.code,
        'participant_count': len(program.patients)
    } for program in programs])

@api.route('/programs/<int:program_id>/enroll', methods=['POST'])
def enroll_patient(program_id):
    data = request.get_json()
    patient_id = data.get('patient_id')
    
    program = Program.query.get_or_404(program_id)
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    
    if not patient:
        return jsonify({'success': False, 'message': 'Patient not found'}), 404
    
    existing_enrollment = Enrollment.query.filter_by(
        program_id=program_id,
        patient_id=patient.id
    ).first()
    
    if existing_enrollment:
        return jsonify({'success': False, 'message': 'Patient already enrolled'}), 400
    
    enrollment = Enrollment(
        program_id=program_id,
        patient_id=patient.id,
        status='active'
    )
    
    try:
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Medication inventory routes
@api.route('/medications/inventory')
def get_medication_inventory():
    medications = Medication.query.all()
    
    return jsonify([{
        'id': med.id,
        'name': med.name,
        'quantity': med.quantity,
        'low_stock_threshold': med.low_stock_threshold,
        'category': med.category,
        'low_stock': med.quantity <= med.low_stock_threshold
    } for med in medications])

@api.route('/medications/inventory', methods=['POST'])
def update_medication_inventory():
    data = request.get_json()
    medication_id = data.get('id')
    quantity = data.get('quantity')
    
    if medication_id:
        medication = Medication.query.get(medication_id)
        if medication:
            medication.quantity = quantity
            
            try:
                db.session.commit()
                return jsonify({'success': True})
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': str(e)}), 500
    
    return jsonify({'success': False, 'message': 'Medication not found'}), 404

# Pending action routes
@api.route('/pending_actions')
def get_pending_actions():
    # Get all pending actions since we don't have user authentication
    actions = PendingAction.query.order_by(PendingAction.due_date).all()
    
    return jsonify([{
        'id': action.id,
        'patient_id': action.patient.patient_id if action.patient else None,
        'patient_name': action.patient.name if action.patient else None,
        'action_type': action.action_type,
        'description': action.description,
        'due_date': action.due_date.isoformat() if action.due_date else None,
        'status': action.status,
        'priority': action.priority
    } for action in actions])

@api.route('/pending_actions', methods=['POST'])
def create_pending_action():
    data = request.get_json()
    
    patient = Patient.query.filter_by(patient_id=data.get('patient_id')).first()
    if not patient:
        return jsonify({'success': False, 'message': 'Patient not found'}), 404
    
    # Use a default user since we don't have authentication
    default_user = User.query.first()
    if not default_user:
        return jsonify({'success': False, 'message': 'No user available'}), 404
    
    action = PendingAction(
        patient_id=patient.id,
        assigned_user_id=default_user.id,
        action_type=data.get('action_type'),
        description=data.get('description'),
        due_date=datetime.strptime(data.get('due_date'), '%Y-%m-%d').date() if data.get('due_date') else None,
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'medium')
    )
    
    try:
        db.session.add(action)
        db.session.commit()
        
        notification = Notification(
            user_id=default_user.id,
            message=f"New pending action: {data.get('description')}",
            notification_type='pending_action'
        )
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api.route('/pending_actions/<int:action_id>/complete', methods=['POST'])
def complete_pending_action(action_id):
    action = PendingAction.query.get_or_404(action_id)
    
    try:
        action.status = 'completed'
        action.completed_at = datetime.now()
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Audit log routes
@api.route('/audit_logs')
def get_audit_logs():
    # Get all audit logs since we don't have user authentication
    logs = AuditLog.query.order_by(desc(AuditLog.timestamp)).limit(100).all()
    
    return jsonify([{
        'id': log.id,
        'action': log.action,
        'details': log.details,
        'timestamp': log.timestamp.isoformat(),
        'patient_id': log.patient_id
    } for log in logs])

# Utility routes
@api.route('/search')
def search():
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'all')
    
    results = []
    
    if search_type in ['all', 'patients']:
        patients = Patient.query.filter(
            or_(
                Patient.name.ilike(f'%{query}%'),
                Patient.patient_id.ilike(f'%{query}%')
            )
        ).limit(10).all()
        results.extend([{
            'type': 'patient',
            'id': p.patient_id,
            'name': p.name,
            'details': f'Age: {p.age}, Gender: {p.gender}'
        } for p in patients])
    
    if search_type in ['all', 'appointments']:
        appointments = Appointment.query.join(Patient).filter(
            or_(
                Patient.name.ilike(f'%{query}%'),
                Appointment.reason.ilike(f'%{query}%')
            )
        ).limit(10).all()
        results.extend([{
            'type': 'appointment',
            'id': f"A{appt.id:04d}",
            'name': appt.patient.name,
            'details': f"{appt.date} {appt.start_time.strftime('%H:%M')} - {appt.reason}"
        } for appt in appointments])
    
    return jsonify(results)

@api.route('/user/profile')
def get_user_profile():
    # Return a default user profile since we don't have authentication
    default_user = User.query.first()
    if not default_user:
        return jsonify({'error': 'No user available'}), 404
        
    return jsonify({
        'id': default_user.id,
        'username': default_user.username,
        'email': default_user.email,
        'role': default_user.role,
        'specialization': default_user.specialization,
        'created_at': default_user.created_at.isoformat()
    })