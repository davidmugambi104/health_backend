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
from app import app


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
        # Additional users
        User(
            username="dr_williams",
            email="williams@hospital.com",
            role="doctor",
            specialization="Pediatrics",
        ),
        User(
            username="dr_brown",
            email="brown@hospital.com",
            role="doctor",
            specialization="Orthopedics",
        ),
        User(
            username="dr_miller",
            email="miller@hospital.com",
            role="doctor",
            specialization="Oncology",
        ),
        User(
            username="nurse_john",
            email="john@hospital.com",
            role="nurse",
            specialization="Emergency",
        ),
        User(
            username="nurse_sarah",
            email="sarah@hospital.com",
            role="nurse",
            specialization="ICU",
        ),
        User(
            username="dr_anderson",
            email="anderson@hospital.com",
            role="doctor",
            specialization="Dermatology",
        ),
        User(
            username="dr_clark",
            email="clark@hospital.com",
            role="doctor",
            specialization="Endocrinology",
        ),
        User(
            username="nurse_davis",
            email="davis@hospital.com",
            role="nurse",
            specialization="Pediatrics",
        ),
        User(
            username="tech_robert",
            email="robert@hospital.com",
            role="technician",
            specialization="Radiology",
        ),
        User(
            username="tech_emma",
            email="emma@hospital.com",
            role="technician",
            specialization="Laboratory",
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
        # Additional patients
        Patient(
            patient_id="PT-1004",
            first_name="Emily",
            last_name="Williams",
            email="emily.w@email.com",
            phone="555-456-7890",
            date_of_birth=date(1990, 3, 10),
            gender="Female",
            blood_type="AB+",
            allergies="Latex",
            current_medications="Vitamin D 1000IU daily",
            insurance_provider="United Health",
            policy_number="UH123789456",
            emergency_contact="Michael Williams (555-654-3210)",
        ),
        Patient(
            patient_id="PT-1005",
            first_name="Michael",
            last_name="Brown",
            email="michael.b@email.com",
            phone="555-567-8901",
            date_of_birth=date(1982, 7, 25),
            gender="Male",
            blood_type="O+",
            allergies="Sulfa drugs",
            current_medications="Atorvastatin 20mg daily",
            insurance_provider="Humana",
            policy_number="HU456123789",
            emergency_contact="Sarah Brown (555-543-2109)",
            telemedicine_ready=True,
        ),
        Patient(
            patient_id="PT-1006",
            first_name="Sarah",
            last_name="Davis",
            email="sarah.d@email.com",
            phone="555-678-9012",
            date_of_birth=date(1975, 11, 30),
            gender="Female",
            blood_type="A-",
            allergies="Iodine, Eggs",
            current_medications="Levothyroxine 75mcg daily",
            insurance_provider="Cigna",
            policy_number="CIG789123456",
            emergency_contact="Robert Davis (555-432-1098)",
        ),
        Patient(
            patient_id="PT-1007",
            first_name="David",
            last_name="Miller",
            email="david.m@email.com",
            phone="555-789-0123",
            date_of_birth=date(1968, 9, 5),
            gender="Male",
            blood_type="B-",
            allergies="None",
            current_medications="Metoprolol 50mg twice daily",
            insurance_provider="Blue Cross",
            policy_number="BC456789123",
            emergency_contact="Lisa Miller (555-321-0987)",
            in_icu=True,
        ),
        Patient(
            patient_id="PT-1008",
            first_name="Jennifer",
            last_name="Wilson",
            email="jennifer.w@email.com",
            phone="555-890-1234",
            date_of_birth=date(1995, 2, 18),
            gender="Female",
            blood_type="O+",
            allergies="Penicillin",
            current_medications="Oral contraceptive daily",
            insurance_provider="Aetna",
            policy_number="AET123456987",
            emergency_contact="Chris Wilson (555-210-9876)",
            telemedicine_ready=True,
        ),
        Patient(
            patient_id="PT-1009",
            first_name="Christopher",
            last_name="Taylor",
            email="chris.t@email.com",
            phone="555-901-2345",
            date_of_birth=date(1988, 6, 12),
            gender="Male",
            blood_type="AB-",
            allergies="Peanuts, Tree nuts",
            current_medications="Loratadine 10mg daily",
            insurance_provider="United Health",
            policy_number="UH987654321",
            emergency_contact="Amanda Taylor (555-109-8765)",
        ),
        Patient(
            patient_id="PT-1010",
            first_name="Amanda",
            last_name="Anderson",
            email="amanda.a@email.com",
            phone="555-012-3456",
            date_of_birth=date(1972, 4, 22),
            gender="Female",
            blood_type="A+",
            allergies="Shellfish, Bees",
            current_medications="Warfarin 5mg daily",
            insurance_provider="Humana",
            policy_number="HU789456123",
            emergency_contact="Mark Anderson (555-098-7654)",
        ),
        Patient(
            patient_id="PT-1011",
            first_name="Daniel",
            last_name="Thomas",
            email="daniel.t@email.com",
            phone="555-123-7890",
            date_of_birth=date(1993, 8, 8),
            gender="Male",
            blood_type="O-",
            allergies="None",
            current_medications="Adderall 20mg daily",
            insurance_provider="Blue Cross",
            policy_number="BC987123456",
            emergency_contact="Rachel Thomas (555-987-0123)",
        ),
        Patient(
            patient_id="PT-1012",
            first_name="Jessica",
            last_name="Jackson",
            email="jessica.j@email.com",
            phone="555-234-8901",
            date_of_birth=date(1980, 12, 15),
            gender="Female",
            blood_type="B+",
            allergies="Aspirin",
            current_medications="Prozac 20mg daily",
            insurance_provider="Aetna",
            policy_number="AET456789321",
            emergency_contact="Kevin Jackson (555-876-5430)",
            in_icu=True,
        ),
    ]

    for patient in patients:
        patient.set_password("TempPassword123")
        db.session.add(patient)

    db.session.commit()

    # -------------------- APPOINTMENTS --------------------
    appointments = [
        # Original appointments
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
        # Additional appointments
        Appointment(
            patient_id=patients[3].id,
            doctor_id=users[3].id,
            date=date.today() + timedelta(days=2),
            start_time=time(14, 0),
            end_time=time(14, 45),
            reason="Vaccination",
            status="scheduled",
        ),
        Appointment(
            patient_id=patients[4].id,
            doctor_id=users[4].id,
            date=date.today() + timedelta(days=3),
            start_time=time(10, 30),
            end_time=time(11, 15),
            reason="Joint pain consultation",
            status="scheduled",
        ),
        Appointment(
            patient_id=patients[5].id,
            doctor_id=users[5].id,
            date=date.today() + timedelta(days=4),
            start_time=time(13, 0),
            end_time=time(13, 45),
            reason="Chemotherapy session",
            status="scheduled",
        ),
        Appointment(
            patient_id=patients[6].id,
            doctor_id=users[6].id,
            date=date.today() + timedelta(days=5),
            start_time=time(9, 30),
            end_time=time(10, 15),
            reason="Emergency follow-up",
            status="scheduled",
        ),
        Appointment(
            patient_id=patients[7].id,
            doctor_id=users[7].id,
            date=date.today() + timedelta(days=6),
            start_time=time(11, 30),
            end_time=time(12, 15),
            reason="ICU monitoring",
            status="scheduled",
        ),
        Appointment(
            patient_id=patients[8].id,
            doctor_id=users[8].id,
            date=date.today() + timedelta(days=7),
            start_time=time(15, 0),
            end_time=time(15, 45),
            reason="Skin condition evaluation",
            status="scheduled",
            telemedicine=True,
        ),
        Appointment(
            patient_id=patients[9].id,
            doctor_id=users[9].id,
            date=date.today() + timedelta(days=8),
            start_time=time(16, 0),
            end_time=time(16, 45),
            reason="Diabetes management",
            status="scheduled",
        ),
        Appointment(
            patient_id=patients[10].id,
            doctor_id=users[10].id,
            date=date.today() + timedelta(days=9),
            start_time=time(8, 30),
            end_time=time(9, 15),
            reason="Pediatric checkup",
            status="scheduled",
        ),
        Appointment(
            patient_id=patients[11].id,
            doctor_id=users[11].id,
            date=date.today() + timedelta(days=10),
            start_time=time(14, 30),
            end_time=time(15, 15),
            reason="X-ray review",
            status="scheduled",
        ),
        Appointment(
            patient_id=patients[0].id,
            doctor_id=users[1].id,
            date=date.today() + timedelta(days=14),
            start_time=time(10, 0),
            end_time=time(10, 30),
            reason="Follow-up consultation",
            status="scheduled",
        ),
        Appointment(
            patient_id=patients[1].id,
            doctor_id=users[0].id,
            date=date.today() + timedelta(days=21),
            start_time=time(11, 0),
            end_time=time(11, 45),
            reason="Neurological assessment",
            status="scheduled",
            telemedicine=True,
        ),
    ]

    for appointment in appointments:
        db.session.add(appointment)

    # -------------------- PRESCRIPTIONS --------------------
    prescriptions = [
        # Original prescriptions
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
        # Additional prescriptions
        Prescription(
            patient_id=patients[2].id,
            medication_name="Albuterol",
            dosage="2 puffs as needed",
            start_date=date.today() - timedelta(days=30),
            prescribing_doctor_id=users[0].id,
            prescribing_doctor_name="Dr. Smith",
            status="active",
        ),
        Prescription(
            patient_id=patients[3].id,
            medication_name="Vitamin D",
            dosage="1000IU daily",
            start_date=date.today() - timedelta(days=15),
            prescribing_doctor_id=users[3].id,
            prescribing_doctor_name="Dr. Anderson",
            status="active",
        ),
        Prescription(
            patient_id=patients[4].id,
            medication_name="Atorvastatin",
            dosage="20mg daily",
            start_date=date.today() - timedelta(days=45),
            prescribing_doctor_id=users[4].id,
            prescribing_doctor_name="Dr. Brown",
            status="active",
        ),
        Prescription(
            patient_id=patients[5].id,
            medication_name="Levothyroxine",
            dosage="75mcg daily",
            start_date=date.today() - timedelta(days=120),
            prescribing_doctor_id=users[5].id,
            prescribing_doctor_name="Dr. Miller",
            status="active",
        ),
        Prescription(
            patient_id=patients[6].id,
            medication_name="Metoprolol",
            dosage="50mg twice daily",
            start_date=date.today() - timedelta(days=75),
            prescribing_doctor_id=users[6].id,
            prescribing_doctor_name="Dr. Clark",
            status="active",
        ),
        Prescription(
            patient_id=patients[7].id,
            medication_name="Oral Contraceptive",
            dosage="1 tablet daily",
            start_date=date.today() - timedelta(days=30),
            prescribing_doctor_id=users[7].id,
            prescribing_doctor_name="Nurse Davis",
            status="active",
        ),
        Prescription(
            patient_id=patients[8].id,
            medication_name="Loratadine",
            dosage="10mg daily",
            start_date=date.today() - timedelta(days=10),
            prescribing_doctor_id=users[8].id,
            prescribing_doctor_name="Tech Robert",
            status="active",
        ),
        Prescription(
            patient_id=patients[9].id,
            medication_name="Warfarin",
            dosage="5mg daily",
            start_date=date.today() - timedelta(days=90),
            prescribing_doctor_id=users[9].id,
            prescribing_doctor_name="Tech Emma",
            status="active",
        ),
        Prescription(
            patient_id=patients[10].id,
            medication_name="Adderall",
            dosage="20mg daily",
            start_date=date.today() - timedelta(days=60),
            prescribing_doctor_id=users[10].id,
            prescribing_doctor_name="Dr. Williams",
            status="active",
        ),
        Prescription(
            patient_id=patients[11].id,
            medication_name="Prozac",
            dosage="20mg daily",
            start_date=date.today() - timedelta(days=30),
            prescribing_doctor_id=users[11].id,
            prescribing_doctor_name="Dr. Jones",
            status="active",
        ),
        Prescription(
            patient_id=patients[0].id,
            medication_name="Aspirin",
            dosage="81mg daily",
            start_date=date.today() - timedelta(days=180),
            prescribing_doctor_id=users[0].id,
            prescribing_doctor_name="Dr. Smith",
            status="active",
        ),
        Prescription(
            patient_id=patients[1].id,
            medication_name="Insulin",
            dosage="10 units before meals",
            start_date=date.today() - timedelta(days=45),
            prescribing_doctor_id=users[1].id,
            prescribing_doctor_name="Dr. Jones",
            status="active",
        ),
    ]

    for prescription in prescriptions:
        db.session.add(prescription)

    # -------------------- LAB RESULTS --------------------
    lab_results = [
        # Original lab results
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
        # Additional lab results
        LabResult(
            patient_id=patients[2].id,
            test_name="Allergy Test",
            result_value="Positive for Shellfish",
            date=date.today() - timedelta(days=5),
            critical_flag=False,
            ordering_provider="Dr. Smith",
        ),
        LabResult(
            patient_id=patients[3].id,
            test_name="Vitamin D Level",
            result_value="18 ng/mL (Low)",
            date=date.today() - timedelta(days=10),
            critical_flag=True,
            ordering_provider="Dr. Anderson",
        ),
        LabResult(
            patient_id=patients[4].id,
            test_name="Cholesterol Panel",
            result_value="Total: 210 mg/dL, LDL: 130 mg/dL",
            date=date.today() - timedelta(days=8),
            critical_flag=True,
            ordering_provider="Dr. Brown",
        ),
        LabResult(
            patient_id=patients[5].id,
            test_name="Thyroid Stimulating Hormone",
            result_value="4.2 mIU/L",
            date=date.today() - timedelta(days=12),
            critical_flag=False,
            ordering_provider="Dr. Miller",
        ),
        LabResult(
            patient_id=patients[6].id,
            test_name="Electrocardiogram",
            result_value="Normal sinus rhythm",
            date=date.today() - timedelta(days=3),
            critical_flag=False,
            ordering_provider="Dr. Clark",
        ),
        LabResult(
            patient_id=patients[7].id,
            test_name="Pregnancy Test",
            result_value="Negative",
            date=date.today() - timedelta(days=1),
            critical_flag=False,
            ordering_provider="Nurse Davis",
        ),
        LabResult(
            patient_id=patients[8].id,
            test_name="Immunoglobulin E",
            result_value="250 IU/mL (High)",
            date=date.today() - timedelta(days=7),
            critical_flag=True,
            ordering_provider="Tech Robert",
        ),
        LabResult(
            patient_id=patients[9].id,
            test_name="Prothrombin Time",
            result_value="16 seconds",
            date=date.today() - timedelta(days=2),
            critical_flag=False,
            ordering_provider="Tech Emma",
        ),
        LabResult(
            patient_id=patients[10].id,
            test_name="Drug Screening",
            result_value="Negative",
            date=date.today() - timedelta(days=4),
            critical_flag=False,
            ordering_provider="Dr. Williams",
        ),
        LabResult(
            patient_id=patients[11].id,
            test_name="Liver Function Test",
            result_value="ALT: 45 U/L, AST: 38 U/L",
            date=date.today() - timedelta(days=6),
            critical_flag=False,
            ordering_provider="Dr. Jones",
        ),
        LabResult(
            patient_id=patients[0].id,
            test_name="Hemoglobin A1C",
            result_value="5.6%",
            date=date.today() - timedelta(days=30),
            critical_flag=False,
            ordering_provider="Dr. Smith",
        ),
        LabResult(
            patient_id=patients[1].id,
            test_name="Urinalysis",
            result_value="Normal",
            date=date.today() - timedelta(days=14),
            critical_flag=False,
            ordering_provider="Dr. Jones",
        ),
    ]

    for lab_result in lab_results:
        db.session.add(lab_result)

    # -------------------- MEDICAL RECORDS --------------------
    medical_records = [
        # Original medical records
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
        # Additional medical records
        MedicalRecord(
            patient_id=patients[2].id,
            diagnosis="Asthma",
            date=date.today() - timedelta(days=30),
            provider="Dr. Smith",
            notes="Patient prescribed Albuterol inhaler for asthma symptoms",
        ),
        MedicalRecord(
            patient_id=patients[3].id,
            diagnosis="Vitamin D Deficiency",
            date=date.today() - timedelta(days=15),
            provider="Dr. Anderson",
            notes="Recommended Vitamin D supplementation and increased sun exposure",
        ),
        MedicalRecord(
            patient_id=patients[4].id,
            diagnosis="Hypercholesterolemia",
            date=date.today() - timedelta(days=45),
            provider="Dr. Brown",
            notes="Prescribed Atorvastatin and recommended dietary changes",
        ),
        MedicalRecord(
            patient_id=patients[5].id,
            diagnosis="Hypothyroidism",
            date=date.today() - timedelta(days=120),
            provider="Dr. Miller",
            notes="Started on Levothyroxine, follow-up in 6 weeks",
        ),
        MedicalRecord(
            patient_id=patients[6].id,
            diagnosis="Hypertension",
            date=date.today() - timedelta(days=75),
            provider="Dr. Clark",
            notes="Prescribed Metoprolol for blood pressure control",
        ),
        MedicalRecord(
            patient_id=patients[7].id,
            diagnosis="Birth Control Management",
            date=date.today() - timedelta(days=30),
            provider="Nurse Davis",
            notes="Prescribed oral contraceptive for family planning",
        ),
        MedicalRecord(
            patient_id=patients[8].id,
            diagnosis="Allergic Rhinitis",
            date=date.today() - timedelta(days=10),
            provider="Tech Robert",
            notes="Recommended Loratadine for seasonal allergies",
        ),
        MedicalRecord(
            patient_id=patients[9].id,
            diagnosis="Atrial Fibrillation",
            date=date.today() - timedelta(days=90),
            provider="Tech Emma",
            notes="Prescribed Warfarin for stroke prevention, INR monitoring required",
        ),
        MedicalRecord(
            patient_id=patients[10].id,
            diagnosis="ADHD",
            date=date.today() - timedelta(days=60),
            provider="Dr. Williams",
            notes="Prescribed Adderall for attention deficit disorder",
        ),
        MedicalRecord(
            patient_id=patients[11].id,
            diagnosis="Major Depressive Disorder",
            date=date.today() - timedelta(days=30),
            provider="Dr. Jones",
            notes="Started on Prozac, follow-up in 4 weeks",
        ),
        MedicalRecord(
            patient_id=patients[0].id,
            diagnosis="High Cholesterol",
            date=date.today() - timedelta(days=180),
            provider="Dr. Smith",
            notes="Recommended low-dose Aspirin for cardiovascular prevention",
        ),
        MedicalRecord(
            patient_id=patients[1].id,
            diagnosis="Diabetes Complications",
            date=date.today() - timedelta(days=45),
            provider="Dr. Jones",
            notes="Added insulin to diabetes management regimen",
        ),
    ]

    for medical_record in medical_records:
        db.session.add(medical_record)

    # -------------------- VITAL SIGNS --------------------
    vital_signs = [
        # Original vital signs
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
        # Additional vital signs
        VitalSign(
            patient_id=patients[2].id,
            heart_rate=68,
            blood_pressure="118/76",
            oxygen_saturation=99.0,
            temperature=36.9,
            timestamp=datetime.now() - timedelta(hours=2),
        ),
        VitalSign(
            patient_id=patients[3].id,
            heart_rate=76,
            blood_pressure="122/84",
            oxygen_saturation=98.2,
            temperature=36.7,
            timestamp=datetime.now() - timedelta(hours=4),
        ),
        VitalSign(
            patient_id=patients[4].id,
            heart_rate=82,
            blood_pressure="128/82",
            oxygen_saturation=97.8,
            temperature=37.0,
            timestamp=datetime.now() - timedelta(hours=6),
        ),
        VitalSign(
            patient_id=patients[5].id,
            heart_rate=71,
            blood_pressure="116/78",
            oxygen_saturation=98.7,
            temperature=36.6,
            timestamp=datetime.now() - timedelta(hours=8),
        ),
        VitalSign(
            patient_id=patients[6].id,
            heart_rate=88,
            blood_pressure="142/92",
            oxygen_saturation=96.5,
            temperature=37.3,
            timestamp=datetime.now() - timedelta(hours=10),
        ),
        VitalSign(
            patient_id=patients[7].id,
            heart_rate=74,
            blood_pressure="124/80",
            oxygen_saturation=98.9,
            temperature=36.8,
            timestamp=datetime.now() - timedelta(hours=12),
        ),
        VitalSign(
            patient_id=patients[8].id,
            heart_rate=79,
            blood_pressure="126/84",
            oxygen_saturation=97.5,
            temperature=37.2,
            timestamp=datetime.now() - timedelta(hours=14),
        ),
        VitalSign(
            patient_id=patients[9].id,
            heart_rate=81,
            blood_pressure="132/86",
            oxygen_saturation=97.0,
            temperature=37.1,
            timestamp=datetime.now() - timedelta(hours=16),
        ),
        VitalSign(
            patient_id=patients[10].id,
            heart_rate=77,
            blood_pressure="120/82",
            oxygen_saturation=98.3,
            temperature=36.9,
            timestamp=datetime.now() - timedelta(hours=18),
        ),
        VitalSign(
            patient_id=patients[11].id,
            heart_rate=84,
            blood_pressure="138/88",
            oxygen_saturation=96.8,
            temperature=37.4,
            timestamp=datetime.now() - timedelta(hours=20),
        ),
        VitalSign(
            patient_id=patients[0].id,
            heart_rate=75,
            blood_pressure="125/83",
            oxygen_saturation=98.1,
            temperature=36.9,
            timestamp=datetime.now() - timedelta(days=1),
        ),
        VitalSign(
            patient_id=patients[1].id,
            heart_rate=87,
            blood_pressure="140/90",
            oxygen_saturation=96.9,
            temperature=37.2,
            timestamp=datetime.now() - timedelta(days=1),
        ),
    ]

    for vital_sign in vital_signs:
        db.session.add(vital_sign)

    # -------------------- PROGRAMS --------------------
    programs = [
        # Original programs
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
        # Additional programs
        Program(
            name="Weight Management",
            description="Program to help patients achieve and maintain healthy weight",
            code="WM2024",
        ),
        Program(
            name="Smoking Cessation",
            description="Support program to help patients quit tobacco use",
            code="SC2024",
        ),
        Program(
            name="Prenatal Care",
            description="Comprehensive care for expectant mothers",
            code="PC2024",
        ),
        Program(
            name="Chronic Pain Management",
            description="Multidisciplinary approach to managing chronic pain",
            code="CPM2024",
        ),
        Program(
            name="Mental Health Support",
            description="Program offering therapy and support for mental health conditions",
            code="MHS2024",
        ),
        Program(
            name="Asthma Control",
            description="Education and management for asthma patients",
            code="AC2024",
        ),
        Program(
            name="Hypertension Management",
            description="Program to help control high blood pressure",
            code="HM2024",
        ),
        Program(
            name="Geriatric Care",
            description="Specialized care program for elderly patients",
            code="GC2024",
        ),
        Program(
            name="Post-Surgical Recovery",
            description="Support program for patients recovering from surgery",
            code="PSR2024",
        ),
        Program(
            name="Nutrition Counseling",
            description="Personalized dietary guidance and meal planning",
            code="NC2024",
        ),
    ]

    for program in programs:
        db.session.add(program)

    db.session.commit()  # commit programs so IDs are available

    # -------------------- ENROLLMENTS --------------------
    enrollments = [
        # Original enrollments
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
        # Additional enrollments
        Enrollment(
            program_id=programs[2].id,
            patient_id=patients[4].id,
            status="active",
        ),
        Enrollment(
            program_id=programs[3].id,
            patient_id=patients[6].id,
            status="completed",
        ),
        Enrollment(
            program_id=programs[4].id,
            patient_id=patients[7].id,
            status="active",
        ),
        Enrollment(
            program_id=programs[5].id,
            patient_id=patients[9].id,
            status="active",
        ),
        Enrollment(
            program_id=programs[6].id,
            patient_id=patients[11].id,
            status="active",
        ),
        Enrollment(
            program_id=programs[7].id,
            patient_id=patients[2].id,
            status="active",
        ),
        Enrollment(
            program_id=programs[8].id,
            patient_id=patients[0].id,
            status="active",
        ),
        Enrollment(
            program_id=programs[9].id,
            patient_id=patients[6].id,
            status="pending",
        ),
        Enrollment(
            program_id=programs[10].id,
            patient_id=patients[3].id,
            status="completed",
        ),
        Enrollment(
            program_id=programs[11].id,
            patient_id=patients[5].id,
            status="active",
        ),
        Enrollment(
            program_id=programs[0].id,
            patient_id=patients[9].id,
            status="active",
        ),
        Enrollment(
            program_id=programs[1].id,
            patient_id=patients[4].id,
            status="pending",
        ),
    ]

    for enrollment in enrollments:
        db.session.add(enrollment)

    # -------------------- MEDICATIONS --------------------
    medications = [
        # Original medications
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
        # Additional medications
        Medication(
            name="Atorvastatin",
            quantity=300,
            low_stock_threshold=40,
            category="Cholesterol",
        ),
        Medication(
            name="Levothyroxine",
            quantity=400,
            low_stock_threshold=60,
            category="Thyroid",
        ),
        Medication(
            name="Metoprolol",
            quantity=350,
            low_stock_threshold=45,
            category="Cardiovascular",
        ),
        Medication(
            name="Warfarin",
            quantity=200,
            low_stock_threshold=30,
            category="Anticoagulant",
        ),
        Medication(
            name="Amoxicillin",
            quantity=600,
            low_stock_threshold=80,
            category="Antibiotic",
        ),
        Medication(
            name="Omeprazole",
            quantity=450,
            low_stock_threshold=50,
            category="GI",
        ),
        Medication(
            name="Sertraline",
            quantity=380,
            low_stock_threshold=40,
            category="Antidepressant",
        ),
        Medication(
            name="Insulin Glargine",
            quantity=150,
            low_stock_threshold=25,
            category="Diabetes",
        ),
        Medication(
            name="Aspirin",
            quantity=1000,
            low_stock_threshold=100,
            category="Pain Relief",
        ),
        Medication(
            name="Ibuprofen",
            quantity=800,
            low_stock_threshold=75,
            category="Pain Relief",
        ),
    ]

    for medication in medications:
        db.session.add(medication)

    # -------------------- NOTIFICATIONS --------------------
    notifications = [
        # Original notifications
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
        # Additional notifications
        Notification(
            patient_id=patients[2].id,
            user_id=users[0].id,
            message="Your test results are available.",
            notification_type="lab_result",
        ),
        Notification(
            patient_id=patients[3].id,
            user_id=users[3].id,
            message="Reminder: Annual physical next week.",
            notification_type="appointment",
        ),
        Notification(
            patient_id=patients[4].id,
            user_id=users[4].id,
            message="Your medication has been refilled.",
            notification_type="prescription",
        ),
        Notification(
            patient_id=patients[5].id,
            user_id=users[5].id,
            message="New message from your doctor.",
            notification_type="message",
        ),
        Notification(
            patient_id=patients[6].id,
            user_id=users[6].id,
            message="Your insurance claim was processed.",
            notification_type="billing",
        ),
        Notification(
            patient_id=patients[7].id,
            user_id=users[7].id,
            message="Welcome to our patient portal!",
            notification_type="system",
        ),
        Notification(
            patient_id=patients[8].id,
            user_id=users[8].id,
            message="Program enrollment confirmed.",
            notification_type="program",
        ),
        Notification(
            patient_id=patients[9].id,
            user_id=users[9].id,
            message="Your vital signs need review.",
            notification_type="vital_signs",
        ),
        Notification(
            patient_id=patients[10].id,
            user_id=users[10].id,
            message="Appointment reminder: tomorrow at 10 AM.",
            notification_type="appointment",
        ),
        Notification(
            patient_id=patients[11].id,
            user_id=users[11].id,
            message="New medical record added to your file.",
            notification_type="medical_record",
        ),
        Notification(
            patient_id=patients[0].id,
            user_id=users[0].id,
            message="Your prescription is ready for pickup.",
            notification_type="prescription",
        ),
    ]

    for notification in notifications:
        db.session.add(notification)

    # -------------------- AUDIT LOGS --------------------
    audit_logs = [
        # Original audit logs
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
        # Additional audit logs
        AuditLog(
            action="Updated Patient Information",
            details="Updated contact information for Robert Johnson",
            patient_id=patients[2].id,
            user_id=users[2].id,  # nurse_mary
        ),
        AuditLog(
            action="Lab Results Viewed",
            details="Dr. Anderson viewed lab results for Emily Williams",
            patient_id=patients[3].id,
            user_id=users[3].id,
        ),
        AuditLog(
            action="Medication Dispensed",
            details="Atorvastatin dispensed to Michael Brown",
            patient_id=patients[4].id,
            user_id=users[4].id,
        ),
        AuditLog(
            action="Program Enrollment",
            details="Sarah Davis enrolled in Weight Management program",
            patient_id=patients[5].id,
            user_id=users[5].id,
        ),
        AuditLog(
            action="Vital Signs Recorded",
            details="Recorded vitals for David Miller",
            patient_id=patients[6].id,
            user_id=users[6].id,
        ),
        AuditLog(
            action="Telemedicine Appointment",
            details="Completed telemedicine appointment with Jennifer Wilson",
            patient_id=patients[7].id,
            user_id=users[7].id,
        ),
        AuditLog(
            action="Prescription Renewed",
            details="Renewed Loratadine prescription for Christopher Taylor",
            patient_id=patients[8].id,
            user_id=users[8].id,
        ),
        AuditLog(
            action="Critical Alert",
            details="High INR result flagged for Amanda Anderson",
            patient_id=patients[9].id,
            user_id=users[9].id,
        ),
        AuditLog(
            action="Medical Record Updated",
            details="Added progress note for Daniel Thomas",
            patient_id=patients[10].id,
            user_id=users[10].id,
        ),
        AuditLog(
            action="Discharge Summary",
            details="Completed discharge process for Jessica Jackson",
            patient_id=patients[11].id,
            user_id=users[11].id,
        ),
        AuditLog(
            action="Billing Update",
            details="Processed insurance claim for John Doe",
            patient_id=patients[0].id,
            user_id=users[3].id,  # admin
        ),
        AuditLog(
            action="System Login",
            details="User dr_jones logged into the system",
            patient_id=None,
            user_id=users[1].id,
        ),
    ]

    for log in audit_logs:
        db.session.add(log)

    # -------------------- FINAL COMMIT --------------------
    db.session.commit()
    print("Database seeded successfully with users, patients, appointments, prescriptions, lab results, medical records, vital signs, programs, enrollments, medications, notifications, and audit logs!")


if __name__ == "__main__":
    with app.app_context():
        seed_database()