class Appointment:
    def __init__(self, patient_name, date, time, reason):
        self.patient_name = patient_name  # string (links by name, or could store patient_id instead)
        self.date = date                  # "yyyy-mm-dd"
        self.time = time                  # "HH:MM"
        self.reason = reason

    def __repr__(self):
        return f"<Appointment {self.patient_name} {self.date} {self.time}>"