from extension import db
from datetime import datetime, date, time, timedelta
from models import (
    User,
    Patient,
    Appointment,
    Prescription,
    LabResult,
    MedicalRecord,
    VitalSign,
    Program,
    Medication,
    Notification,
    Enrollment,
    AuditLog,
)
from app import app   # ✅ import your Flask app


def seed_database():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # -------------------- USERS --------------------
    users = [
        User(
            username="dr_smith",
            email="smith@hospital.com",
            role="doctor",
            specialization="Cardiology",
        ),
        User(
            username="dr_jones",
            email="jones@hospital.com",
            role="doctor",
            specialization="Neurology",
        ),
        User(
            username="nurse_mary",
            email="mary@hospital.com",
            role="nurse",
            specialization="General Medicine",
        ),
        User(
            username="admin",
            email="admin@hospital.com",
            role="admin",
        ),
    ]

    for user in users:
        user.set_password("test1234")
        db.session.add(user)

    # -------------------- PATIENTS --------------------
    patients = [
        Patient(
            patient_id="PT-1001",
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone="555-123-4567",
            date_of_birth=date(1985, 5, 15),
            gender="Male",
            blood_type="A+",
            allergies="Penicillin, Peanuts",
            current_medications="Lisinopril 10mg daily",
            insurance_provider="Blue Cross",
            policy_number="BC123456789",
            emergency_contact="Jane Doe (555-987-6543)",
        ),
        Patient(
            patient_id="PT-1002",
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@email.com",
            phone="555-234-5678",
            date_of_birth=date(1978, 8, 22),
            gender="Female",
            blood_type="O-",
            allergies="None",
            current_medications="Metformin 500mg twice daily",
            insurance_provider="Aetna",
            policy_number="AET987654321",
            emergency_contact="John Smith (555-876-5432)",
            in_icu=True,
        ),
        Patient(
            patient_id="PT-1003",
            first_name="Robert",
            last_name="Johnson",
            email="robert.j@email.com",
            phone="555-345-6789",
            date_of_birth=date(1992, 12, 3),
            gender="Male",
            blood_type="B+",
            allergies="Shellfish",
            current_medications="Albuterol inhaler as needed",
            insurance_provider="Cigna",
            policy_number="CIG456789123",
            emergency_contact="Mary Johnson (555-765-4321)",
            telemedicine_ready=True,
        ),
    ]

    for patient in patients:
        patient.set_password("TempPassword123")
        db.session.add(patient)

    db.session.commit()

    # -------------------- APPOINTMENTS --------------------
    appointments = [
        Appointment(
            patient_id=patients[0].id,
            doctor_id=users[0].id,
            date=date.today(),
            start_time=time(9, 0),
            end_time=time(9, 30),
            reason="Annual checkup",
            status="scheduled",
        ),
        Appointment(
            patient_id=patients[1].id,
            doctor_id=users[1].id,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(10, 45),
            reason="Follow-up on test results",
            status="scheduled",
            telemedicine=True,
        ),
        Appointment(
            patient_id=patients[2].id,
            doctor_id=users[0].id,
            date=date.today() + timedelta(days=1),
            start_time=time(11, 0),
            end_time=time(11, 30),
            reason="Medication review",
            status="scheduled",
        ),
    ]

    for appointment in appointments:
        db.session.add(appointment)

    # -------------------- PRESCRIPTIONS --------------------
    prescriptions = [
        Prescription(
            patient_id=patients[0].id,
            medication_name="Lisinopril",
            dosage="10mg daily",
            start_date=date.today() - timedelta(days=90),
            prescribing_doctor_id=users[0].id,
            prescribing_doctor_name="Dr. Smith",
            status="active",
        ),
        Prescription(
            patient_id=patients[1].id,
            medication_name="Metformin",
            dosage="500mg twice daily",
            start_date=date.today() - timedelta(days=60),
            prescribing_doctor_id=users[1].id,
            prescribing_doctor_name="Dr. Jones",
            status="active",
        ),
    ]

    for prescription in prescriptions:
        db.session.add(prescription)

    # -------------------- LAB RESULTS --------------------
    lab_results = [
        LabResult(
            patient_id=patients[0].id,
            test_name="Complete Blood Count",
            result_value="Normal",
            date=date.today() - timedelta(days=7),
            critical_flag=False,
            ordering_provider="Dr. Smith",
        ),
        LabResult(
            patient_id=patients[1].id,
            test_name="Blood Glucose",
            result_value="145 mg/dL",
            date=date.today() - timedelta(days=3),
            critical_flag=True,
            ordering_provider="Dr. Jones",
        ),
    ]

    for lab_result in lab_results:
        db.session.add(lab_result)

    # -------------------- MEDICAL RECORDS --------------------
    medical_records = [
        MedicalRecord(
            patient_id=patients[0].id,
            diagnosis="Hypertension",
            date=date.today() - timedelta(days=90),
            provider="Dr. Smith",
            notes="Patient prescribed Lisinopril 10mg daily",
        ),
        MedicalRecord(
            patient_id=patients[1].id,
            diagnosis="Type 2 Diabetes",
            date=date.today() - timedelta(days=60),
            provider="Dr. Jones",
            notes="Patient prescribed Metformin 500mg twice daily",
        ),
    ]

    for medical_record in medical_records:
        db.session.add(medical_record)

    # -------------------- VITAL SIGNS --------------------
    vital_signs = [
        VitalSign(
            patient_id=patients[0].id,
            heart_rate=72,
            blood_pressure="120/80",
            oxygen_saturation=98.5,
            temperature=36.8,
            timestamp=datetime.now(),
        ),
        VitalSign(
            patient_id=patients[1].id,
            heart_rate=85,
            blood_pressure="135/90",
            oxygen_saturation=97.2,
            temperature=37.1,
            timestamp=datetime.now(),
        ),
    ]

    for vital_sign in vital_signs:
        db.session.add(vital_sign)

    # -------------------- PROGRAMS --------------------
    programs = [
        Program(
            name="Diabetes Management",
            description="Comprehensive diabetes care and education program",
            code="DM2024",
        ),
        Program(
            name="Cardiac Rehabilitation",
            description="Supervised program to improve cardiovascular health",
            code="CR2024",
        ),
    ]

    for program in programs:
        db.session.add(program)

    db.session.commit()  # commit programs so IDs are available

    # -------------------- ENROLLMENTS --------------------
    enrollments = [
        Enrollment(
            program_id=programs[0].id,
            patient_id=patients[1].id,
            status="active",
        ),
        Enrollment(
            program_id=programs[1].id,
            patient_id=patients[0].id,
            status="active",
        ),
    ]

    for enrollment in enrollments:
        db.session.add(enrollment)

    # -------------------- MEDICATIONS --------------------
    medications = [
        Medication(
            name="Lisinopril",
            quantity=500,
            low_stock_threshold=50,
            category="Hypertension",
        ),
        Medication(
            name="Metformin",
            quantity=750,
            low_stock_threshold=100,
            category="Diabetes",
        ),
        Medication(
            name="Albuterol Inhaler",
            quantity=45,
            low_stock_threshold=20,
            category="Respiratory",
        ),
    ]

    for medication in medications:
        db.session.add(medication)

    # -------------------- NOTIFICATIONS --------------------
    notifications = [
        Notification(
            patient_id=patients[0].id,
            user_id=users[0].id,
            message="Upcoming appointment scheduled.",
            notification_type="appointment",
        ),
        Notification(
            patient_id=patients[1].id,
            user_id=users[1].id,
            message="New prescription available.",
            notification_type="prescription",
        ),
        Notification(
            patient_id=patients[1].id,
            user_id=users[1].id,
            message="Lab results ready for review.",
            notification_type="lab_result",
        ),
    ]

    for notification in notifications:
        db.session.add(notification)

    # -------------------- AUDIT LOGS --------------------
    audit_logs = [
        AuditLog(
            action="Created Patient",
            details="Patient John Doe created",
            patient_id=patients[0].id,
            user_id=users[3].id,  # admin
        ),
        AuditLog(
            action="Appointment Scheduled",
            details="Jane Smith scheduled for telemedicine",
            patient_id=patients[1].id,
            user_id=users[1].id,  # Dr. Jones
        ),
        AuditLog(
            action="Prescription Added",
            details="Metformin prescribed",
            patient_id=patients[1].id,
            user_id=users[1].id,
        ),
    ]

    for log in audit_logs:
        db.session.add(log)

    # -------------------- FINAL COMMIT --------------------
    db.session.commit()
    print("Database seeded successfully with users, patients, appointments, prescriptions, lab results, medical records, vital signs, programs, enrollments, medications, notifications, and audit logs!")


if __name__ == "__main__":
    with app.app_context():   # ✅ push app context
        seed_database()
