from datetime import datetime

class Patient:
    def __init__(self, patient_id, first_name, last_name, dob, address, phone, email, photo=None, parent_info=None):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob               
        self.address = address
        self.phone = phone
        self.email = email
        self.photo = photo
        self.parent_info = parent_info or {}
        self.treatments = {}         
        self.treatment_notes = {}  

    # ---------- Computed properties ----------
    @property
    def age(self):
        return (datetime.now().date() - self.dob).days // 365

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # ---------- Treatment handling ----------
    def add_treatment(self, treatment_name, description="-"):
        today = datetime.now().strftime("%Y-%m-%d")
        self.treatments.setdefault(today, []).append(treatment_name)
        self.treatment_notes.setdefault(today, []).append(description)