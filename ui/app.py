import customtkinter as ctk
from .HomeView import HomeView
from .PatientView import PatientView
from .AppointmentView import AppointmentView
from .BillingView import BillingView
from repository.patient_repo import PatientRepository
from repository.appointment_repo import AppointmentRepository

class DentalManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Dental Management System")
        self.master.geometry("1400x1000")

        # storage
        self.patients_repo = PatientRepository()
        self.appts_repo = AppointmentRepository()

        # layout
        self.setup_layout()
        self.show_home()

    def setup_layout(self):
        self.menu_frame = ctk.CTkFrame(self.master, fg_color="#d0d0d0", width=200)
        self.menu_frame.pack(side=ctk.LEFT, fill=ctk.Y)

        ctk.CTkButton(self.menu_frame, text="Home", command=self.show_home).pack(pady=10)
        ctk.CTkButton(self.menu_frame, text="Patients", command=self.show_patients).pack(pady=10)
        ctk.CTkButton(self.menu_frame, text="Appointments", command=self.show_appointments).pack(pady=10)
        ctk.CTkButton(self.menu_frame, text="Billing", command=self.show_billing).pack(pady=10)

        self.content_frame = ctk.CTkFrame(self.master)
        self.content_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        HomeView(self.content_frame)

    def show_patients(self):
        self.clear_content()
        PatientView(self.content_frame, self.patients_repo)

    def show_appointments(self):
        self.clear_content()
        AppointmentView(self.content_frame, self.appts_repo, self.patients_repo)

    def show_billing(self):
        self.clear_content()
        BillingView(self.content_frame, self.patients_repo)