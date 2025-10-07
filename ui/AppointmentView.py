import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from models.appointment import Appointment

class AppointmentView:
    def __init__(self, master, appointment_repo, patients, appointments):
        self.master = master
        self.appointment_repo = appointment_repo
        self.patients = patients
        self.appointments = appointments

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True, pady=10)

        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="Add Appointment")
        self.notebook.add(self.view_tab, text="View Appointments")

        self.create_add_tab()
        self.create_view_tab()

    def create_add_tab(self):
        patient_list = [f"{p['first_name']} {p['last_name']}" for p in self.patients]
        ctk.CTkLabel(self.add_tab, text="Patient:").grid(row=0, column=0, padx=10, pady=10)
        self.patient_box = ttk.Combobox(self.add_tab, values=patient_list)
        self.patient_box.grid(row=0, column=1)

        ctk.CTkLabel(self.add_tab, text="Date:").grid(row=1, column=0, padx=10, pady=10)
        self.date = DateEntry(self.add_tab, date_pattern="y-mm-dd")
        self.date.grid(row=1, column=1)

        ctk.CTkLabel(self.add_tab, text="Time:").grid(row=2, column=0, padx=10, pady=10)
        self.time = ctk.CTkEntry(self.add_tab)
        self.time.grid(row=2, column=1)

        ctk.CTkLabel(self.add_tab, text="Reason:").grid(row=3, column=0, padx=10, pady=10)
        self.reason = ctk.CTkEntry(self.add_tab)
        self.reason.grid(row=3, column=1)

        ctk.CTkButton(self.add_tab, text="Add Appointment", command=self.add_appointment).grid(row=4, columnspan=2, pady=20)

    def add_appointment(self):
        p = self.patient_box.get()
        if not p:
            messagebox.showerror("Error", "Select a patient")
            return
        a = Appointment(p, str(self.date.get_date()), self.time.get(), self.reason.get())
        self.appointments.append(a.__dict__)
        self.appointment_repo.save(self.appointments)
        messagebox.showinfo("Success", "Appointment added successfully!")

    def create_view_tab(self):
        search = ctk.CTkEntry(self.view_tab, placeholder_text="Search by patient name...")
        search.pack(pady=5)
        search.bind("<KeyRelease>", lambda e: self.filter_appointments(search.get()))

        self.tree = ttk.Treeview(self.view_tab, columns=("Patient", "Date", "Time", "Reason"), show="headings")
        for c in ("Patient", "Date", "Time", "Reason"):
            self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True)
        self.populate_tree()

    def populate_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for a in self.appointments:
            self.tree.insert("", "end", values=(a["patient_name"], a["date"], a["time"], a["reason"]))

    def filter_appointments(self, name):
        filtered = [a for a in self.appointments if name.lower() in a["patient_name"].lower()]
        for i in self.tree.get_children():
            self.tree.delete(i)
        for a in filtered:
            self.tree.insert("", "end", values=(a["patient_name"], a["date"], a["time"], a["reason"]))