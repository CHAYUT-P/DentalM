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
        self.master.configure(bg="#e3e4e4")

        # Load repositories
        self.patient_repo = PatientRepository()
        self.appointment_repo = AppointmentRepository()

        self.patients = self.patient_repo.load()
        self.appointments = self.appointment_repo.load()

        # UI Layout
        self.setup_layout()

    def setup_layout(self):
        self.top_bar = ctk.CTkFrame(self.master, fg_color="#3ab286", height=20)
        self.top_bar.pack(side="top", fill="x")

        self.bottom_bar = ctk.CTkFrame(self.master, fg_color="#3ab286", height=20)
        self.bottom_bar.pack(side="bottom", fill="x")

        self.left_menu = ctk.CTkFrame(self.master, fg_color="#d0d0d0", width=200)
        self.left_menu.pack(side="left", fill="y")

        ctk.CTkButton(self.left_menu, text="Home", command=self.show_home, fg_color="#3a66b2").pack(pady=10)
        ctk.CTkButton(self.left_menu, text="Patients", command=self.show_patients, fg_color="#3a66b2").pack(pady=10)
        ctk.CTkButton(self.left_menu, text="Appointments", command=self.show_appointments, fg_color="#3a66b2").pack(pady=10)
        ctk.CTkButton(self.left_menu, text="Check Bill", command=self.show_billing, fg_color="#3a66b2").pack(pady=10)

        self.content_frame = ctk.CTkFrame(self.master)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.show_home()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        HomeView(self.content_frame)

    def show_patients(self):
        self.clear_content()
        PatientView(self.content_frame, self.patient_repo, self.patients, self.appointment_repo, self.appointments)

    def show_appointments(self):
        self.clear_content()
        AppointmentView(self.content_frame, self.appointment_repo, self.patients, self.appointments)

    def show_billing(self):
        self.clear_content()
        BillingView(self.content_frame, self.patient_repo)