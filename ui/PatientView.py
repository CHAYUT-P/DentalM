import customtkinter as ctk
from tkinter import ttk, messagebox
from models.patient import Patient
from datetime import datetime

class PatientView:
    def __init__(self, parent, repo):
        self.repo = repo
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self.frame, text="Patient Management", font=("Arial", 16)).pack(pady=10)

        # Add patient form
        self.first_name = ctk.CTkEntry(self.frame, placeholder_text="First Name")
        self.first_name.pack(pady=5)
        self.last_name = ctk.CTkEntry(self.frame, placeholder_text="Last Name")
        self.last_name.pack(pady=5)

        add_btn = ctk.CTkButton(self.frame, text="Add Patient", command=self.add_patient)
        add_btn.pack(pady=10)

        # Treeview of patients
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Name"), show="headings")
        self.tree.heading("ID", text="Patient ID")
        self.tree.heading("Name", text="Full Name")
        self.tree.pack(pady=10, fill="both", expand=True)

        self.populate_tree()

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for patient in self.repo.data:
            self.tree.insert("", "end", values=(patient.patient_id, patient.full_name))

    def add_patient(self):
        pid = f"{datetime.now().strftime('%y%m%d')}-{len(self.repo.data)+1:03d}"
        new_patient = Patient(pid, self.first_name.get(), self.last_name.get(),
                              datetime.now().date(), "-", "-", "-", "")
        self.repo.add(new_patient)
        messagebox.showinfo("Success", "Patient added")
        self.populate_tree()