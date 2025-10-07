import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk
from models.patient import Patient
from models.treatments import DENTAL_TREATMENTS


class PatientView:
    def __init__(self, master, patient_repo, patients, appointment_repo, appointments):
        self.master = master
        self.patient_repo = patient_repo
        self.appointment_repo = appointment_repo
        self.patients = patients
        self.appointments = appointments
        self.photo_path = ""

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True, pady=10)

        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="Add Patient")
        self.notebook.add(self.view_tab, text="View Patients")

        self.create_add_tab()
        self.create_view_tab()

    # ---- Add patient tab ----
    def create_add_tab(self):
        ctk.CTkLabel(self.add_tab, text="First Name:").grid(row=0, column=0, padx=10, pady=10)
        self.first_name = ctk.CTkEntry(self.add_tab)
        self.first_name.grid(row=0, column=1)

        ctk.CTkLabel(self.add_tab, text="Last Name:").grid(row=1, column=0, padx=10, pady=10)
        self.last_name = ctk.CTkEntry(self.add_tab)
        self.last_name.grid(row=1, column=1)

        ctk.CTkLabel(self.add_tab, text="Date of Birth:").grid(row=2, column=0, padx=10, pady=10)
        self.dob = DateEntry(self.add_tab, date_pattern="y-mm-dd")
        self.dob.grid(row=2, column=1)
        self.dob.bind("<<DateEntrySelected>>", self.check_age)

        ctk.CTkLabel(self.add_tab, text="Address:").grid(row=3, column=0, padx=10, pady=10)
        self.address = ctk.CTkEntry(self.add_tab)
        self.address.grid(row=3, column=1)

        ctk.CTkLabel(self.add_tab, text="Phone:").grid(row=4, column=0, padx=10, pady=10)
        self.phone = ctk.CTkEntry(self.add_tab)
        self.phone.grid(row=4, column=1)

        ctk.CTkLabel(self.add_tab, text="Email:").grid(row=5, column=0, padx=10, pady=10)
        self.email = ctk.CTkEntry(self.add_tab)
        self.email.grid(row=5, column=1)

        ctk.CTkLabel(self.add_tab, text="Dental Treatment:").grid(row=6, column=0, padx=10, pady=10)
        self.treatment_combobox = ttk.Combobox(self.add_tab, values=DENTAL_TREATMENTS)
        self.treatment_combobox.grid(row=6, column=1)

        ctk.CTkButton(self.add_tab, text="Upload Photo", command=self.upload_photo).grid(row=7, column=0, padx=10, pady=10)
        self.photo_label = ctk.CTkLabel(self.add_tab, text="No photo uploaded")
        self.photo_label.grid(row=7, column=1)

        self.parent_frame = ctk.CTkFrame(self.add_tab)
        ctk.CTkLabel(self.parent_frame, text="Parent Name:").grid(row=0, column=0, padx=5, pady=5)
        self.parent_name = ctk.CTkEntry(self.parent_frame)
        self.parent_name.grid(row=0, column=1)
        ctk.CTkLabel(self.parent_frame, text="Parent Phone:").grid(row=1, column=0, padx=5, pady=5)
        self.parent_phone = ctk.CTkEntry(self.parent_frame)
        self.parent_phone.grid(row=1, column=1)
        self.parent_frame.grid_remove()

        ctk.CTkButton(self.add_tab, text="Add Patient", command=self.add_patient).grid(row=8, columnspan=2, pady=20)

    def check_age(self, event=None):
        age = (datetime.now().date() - self.dob.get_date()).days // 365
        if age < 18:
            self.parent_frame.grid(row=9, columnspan=2)
        else:
            self.parent_frame.grid_remove()

    def upload_photo(self):
        path = filedialog.askopenfilename()
        if path:
            self.photo_path = path
            img = Image.open(path)
            img.thumbnail((100, 100))
            img = ImageTk.PhotoImage(img)
            self.photo_label.configure(image=img, text="")
            self.photo_label.image = img

    def add_patient(self):
        fn, ln = self.first_name.get(), self.last_name.get()
        if not fn or not ln:
            messagebox.showerror("Error", "Name required")
            return

        pid = datetime.now().strftime("%y%m%d-") + str(len(self.patients) + 1).zfill(3)
        parent_info = {}
        age = (datetime.now().date() - self.dob.get_date()).days // 365
        if age < 18:
            parent_info = {"parent_name": self.parent_name.get(), "parent_phone": self.parent_phone.get()}

        patient = Patient(pid, fn, ln, self.dob.get_date(), self.address.get(), self.phone.get(), self.email.get(), self.photo_path, parent_info)
        treatment = self.treatment_combobox.get()
        if treatment:
            patient.add_treatment(treatment)
        self.patients.append(patient.__dict__)
        self.patient_repo.save(self.patients)
        messagebox.showinfo("Success", "Patient added successfully!")

        # clear inputs
        for e in [self.first_name, self.last_name, self.address, self.phone, self.email]:
            e.delete(0, "end")
        self.treatment_combobox.set("")
        self.photo_label.configure(image=None, text="No photo uploaded")
        self.photo_path = ""

        # refresh & switch tab
        self.populate_tree()
        self.notebook.select(self.view_tab)

    # ---- View patients tab ----
    def create_view_tab(self):
        search = ctk.CTkEntry(self.view_tab, placeholder_text="Search by first name...")
        search.pack(pady=5)
        search.bind("<KeyRelease>", lambda e: self.filter_patients(search.get()))

        self.tree = ttk.Treeview(self.view_tab, columns=("ID", "First", "Last", "DOB"), show="headings")
        for c in ("ID", "First", "Last", "DOB"):
            self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, pady=10)
        self.tree.bind("<Double-1>", self.open_patient_window)

        self.populate_tree()

    def populate_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in self.patients:
            self.tree.insert("", "end", values=(p["patient_id"], p["first_name"], p["last_name"], p["dob"]))

    def filter_patients(self, name):
        filtered = [p for p in self.patients if name.lower() in p["first_name"].lower()]
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in filtered:
            self.tree.insert("", "end", values=(p["patient_id"], p["first_name"], p["last_name"], p["dob"]))

    # ---- Double-click patient ----
    def open_patient_window(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        pid = values[0]
        patient = next((p for p in self.patients if p["patient_id"] == pid), None)
        if not patient:
            messagebox.showerror("Error", "Patient not found")
            return

        win = ctk.CTkToplevel(self.master)
        win.title(f"{patient['first_name']} {patient['last_name']} Info")
        win.geometry("500x600")

        # Info
        ctk.CTkLabel(win, text=f"Patient ID: {patient['patient_id']}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(win, text=f"Name: {patient['first_name']} {patient['last_name']}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(win, text=f"DOB: {patient['dob']}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(win, text=f"Phone: {patient['phone']}", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(win, text=f"Email: {patient['email']}", font=("Arial", 14)).pack(pady=5)

        if patient["parent_info"]:
            ctk.CTkLabel(win, text="Parent Info:", font=("Arial", 14, "bold")).pack(pady=10)
            ctk.CTkLabel(win, text=f"Parent Name: {patient['parent_info'].get('parent_name', '')}").pack(pady=2)
            ctk.CTkLabel(win, text=f"Parent Phone: {patient['parent_info'].get('parent_phone', '')}").pack(pady=2)

        if patient.get("photo"):
            try:
                img = Image.open(patient["photo"])
                img.thumbnail((120, 120))
                img = ImageTk.PhotoImage(img)
                img_label = ttk.Label(win, image=img)
                img_label.image = img
                img_label.pack(pady=10)
            except Exception as e:
                print("Error loading photo:", e)

        # Buttons
        btn_frame = ctk.CTkFrame(win)
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Add Appointment", command=lambda: self.add_appointment_for(patient, win)).pack(padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="Add Treatment", command=lambda: self.add_treatment_for(patient, win)).pack(padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="Delete Patient", fg_color="red", command=lambda: self.delete_patient(patient, win)).pack(padx=5, pady=5)
        ctk.CTkButton(win, text="Close", command=win.destroy).pack(pady=10)

    def add_appointment_for(self, patient, win):
        win.destroy()
        # reuse AppointmentView from app
        from ui.AppointmentView import AppointmentView
        new_win = ctk.CTkToplevel(self.master)
        AppointmentView(new_win, self.appointment_repo, self.patients, self.appointments)
        # preselect
        messagebox.showinfo("Hint", f"Preselect {patient['first_name']} in appointment form.")

    def add_treatment_for(self, patient, win):
        new = ctk.CTkToplevel(win)
        new.title("Add Treatment")
        new.geometry("400x300")

        treatment_box = ttk.Combobox(new, values=DENTAL_TREATMENTS)
        treatment_box.pack(pady=10)
        desc = ctk.CTkTextbox(new, width=300, height=100)
        desc.pack(pady=10)

        def save():
            t = treatment_box.get()
            d = desc.get("1.0", "end-1c").strip() or "-"
            date = datetime.now().strftime("%Y/%m/%d")
            patient["dental_treatment"].setdefault(date, []).append(t)
            patient["treatment_descriptions"].setdefault(date, []).append(d)
            self.patient_repo.save(self.patients)
            messagebox.showinfo("Success", f"{t} added for {patient['first_name']}")
            new.destroy()

        ctk.CTkButton(new, text="Save", command=save).pack(pady=10)

    def delete_patient(self, patient, win):
        confirm = messagebox.askyesno("Confirm", f"Delete {patient['first_name']} {patient['last_name']}?")
        if not confirm:
            return
        self.patients = [p for p in self.patients if p["patient_id"] != patient["patient_id"]]
        self.patient_repo.save(self.patients)
        self.populate_tree()
        messagebox.showinfo("Success", "Deleted successfully.")
        win.destroy()