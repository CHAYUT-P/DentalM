from .base_repo import Repository

class AppointmentRepository(Repository):
    def __init__(self):
        super().__init__("appointments.pkl")

    def add(self, appointment):
        self.data.append(appointment)
        self.save()

    def remove(self, appointment):
        self.data.remove(appointment)
        self.save()