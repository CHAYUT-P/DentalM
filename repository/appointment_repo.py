from .base_repo import BaseRepository

class AppointmentRepository(BaseRepository):
    def __init__(self):
        super().__init__("appointments.pkl")