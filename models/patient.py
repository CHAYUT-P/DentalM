from datetime import datetime

class Patient:
    def __init__(self, patient_id, first_name, last_name, dob, address, phone, email, photo, parent_info=None):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.address = address
        self.phone = phone
        self.email = email
        self.photo = photo
        self.parent_info = parent_info or {}
        self.dental_treatment = {}
        self.treatment_descriptions = {}

    def add_treatment(self, treatment_name, description="-"):
        today_date = datetime.now().strftime("%Y/%m/%d")
        self.dental_treatment.setdefault(today_date, []).append(treatment_name)
        self.treatment_descriptions.setdefault(today_date, []).append(description)