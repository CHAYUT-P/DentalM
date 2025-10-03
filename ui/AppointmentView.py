import customtkinter as ctk
from tkinter import ttk, messagebox
from models.appointment import Appointment
from datetime import datetime

class AppointmentView:
    def __init__(self, parent, appt_repo, patient_repo):
        self.appt_repo = appt_repo
        self.patient_repo = patient_repo

        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self.frame, text="Appointment Management", font=("Arial", 16)).pack(pady=10)

        self.reason_entry = ctk.CTkEntry(self.frame, placeholder_text="Reason")
        self.reason_entry.pack(pady=5)

        self.patient_select = ttk.Combobox(self.frame, values=[p.full_name for p in self.patient_repo.data])
        self.patient_select.pack(pady=5)

        add_btn = ctk.CTkButton(self.frame, text="Add Appointment", command=self.add_appointment)
        add_btn.pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("Patient", "Date", "Time", "Reason"), show="headings")
        for col in ("Patient", "Date", "Time", "Reason"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="both", expand=True)

        self.populate_tree()

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for appt in self.appt_repo.data:
            self.tree.insert("", "end", values=(appt.patient_name, appt.date, appt.time, appt.reason))

    def add_appointment(self):
        patient = self.patient_select.get()
        if not patient:
            messagebox.showerror("Error", "Select a patient")
            return
        appt = Appointment(patient, datetime.now().strftime("%Y-%m-%d"), "10:00", self.reason_entry.get())
        self.appt_repo.add(appt)
        self.populate_tree()