from .base_repo import Repository

class PatientRepository(Repository):
    def __init__(self):
        super().__init__("patients.pkl")

    def add(self, patient):
        self.data.append(patient)
        self.save()

    def remove(self, patient_id):
        self.data = [p for p in self.data if p.patient_id != patient_id]
        self.save()

    def find_by_id(self, patient_id):
        return next((p for p in self.data if p.patient_id == patient_id), None)