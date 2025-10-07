from .base_repo import BaseRepository

class PatientRepository(BaseRepository):
    def __init__(self):
        super().__init__("patients.pkl")