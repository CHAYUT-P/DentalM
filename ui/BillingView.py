import customtkinter as ctk
from tkinter import ttk, messagebox
from models.treatments import TREATMENT_PRICE

class BillingView:
    def __init__(self, master, patient_repo):
        self.master = master
        self.patient_repo = patient_repo
        self.patients = patient_repo.load()
        self.selected_treatments = []

        self.frame = ctk.CTkFrame(master)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.frame, text="Select Patient:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.patient_box = ttk.Combobox(
            self.frame,
            values=[f"{p['first_name']} {p['last_name']}" for p in self.patients],
            width=40
        )
        self.patient_box.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(self.frame, text="Load Treatments", command=self.load_treatments).grid(row=0, column=2, padx=10, pady=10)

        self.treatment_frame = ctk.CTkScrollableFrame(self.frame, width=600, height=400)
        self.treatment_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.check_vars = []
        self.treatment_checkbuttons = []

        btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)

        self.select_all_btn = ctk.CTkButton(btn_frame, text="Select All", command=self.toggle_select_all)
        self.select_all_btn.pack(side="left", padx=5)

        self.check_bill_btn = ctk.CTkButton(btn_frame, text="Check Bill", fg_color="#3a66b2", command=self.calculate_bill)
        self.check_bill_btn.pack(side="left", padx=5)

        self.reset_btn = ctk.CTkButton(btn_frame, text="Clear", fg_color="#999999", command=self.clear_selection)
        self.reset_btn.pack(side="left", padx=5)

        self.bill_tree = ttk.Treeview(self.frame, columns=("Date", "Treatment", "Cost"), show="headings", height=8)
        for c in ("Date", "Treatment", "Cost"):
            self.bill_tree.heading(c, text=c)
            self.bill_tree.column(c, anchor="center", width=180)
        self.bill_tree.grid(row=3, column=0, columnspan=3, pady=10)

        self.total_label = ctk.CTkLabel(self.frame, text="Total: 0.00", font=("Arial", 16, "bold"))
        self.total_label.grid(row=4, column=0, columnspan=3, pady=10)

    def load_treatments(self):
        name = self.patient_box.get()
        if not name:
            messagebox.showerror("Error", "Please select a patient")
            return

        patient = next((p for p in self.patients if f"{p['first_name']} {p['last_name']}" == name), None)
        if not patient:
            messagebox.showerror("Error", "Patient not found")
            return

        for cb in self.treatment_checkbuttons:
            cb.destroy()
        self.check_vars.clear()
        self.treatment_checkbuttons.clear()

        if not patient["dental_treatment"]:
            ctk.CTkLabel(self.treatment_frame, text="No treatments found.").pack(pady=10)
            return

        for date, treatments in patient["dental_treatment"].items():
            for t in treatments:
                var = ctk.BooleanVar()
                text = f"{date} - {t} ({TREATMENT_PRICE.get(t, 0.0):.2f} ฿)"
                cb = ctk.CTkCheckBox(self.treatment_frame, text=text, variable=var)
                cb.pack(anchor="w", padx=10, pady=3)
                self.check_vars.append((var, date, t))
                self.treatment_checkbuttons.append(cb)

        self.total_label.configure(text="Total: 0.00")
        for row in self.bill_tree.get_children():
            self.bill_tree.delete(row)

    def toggle_select_all(self):
        if not self.check_vars:
            return
        all_selected = all(var.get() for var, _, _ in self.check_vars)
        for var, _, _ in self.check_vars:
            var.set(not all_selected)
        self.select_all_btn.configure(text="Deselect All" if not all_selected else "Select All")

    def clear_selection(self):
        for var, _, _ in self.check_vars:
            var.set(False)
        self.total_label.configure(text="Total: 0.00")
        for row in self.bill_tree.get_children():
            self.bill_tree.delete(row)
        self.select_all_btn.configure(text="Select All")

    def calculate_bill(self):
        self.selected_treatments.clear()
        total = 0.0
        for var, date, treatment in self.check_vars:
            if var.get():
                cost = TREATMENT_PRICE.get(treatment, 0.0)
                self.selected_treatments.append((date, treatment, cost))
                total += cost
        for row in self.bill_tree.get_children():
            self.bill_tree.delete(row)
        for date, treatment, cost in self.selected_treatments:
            self.bill_tree.insert("", "end", values=(date, treatment, f"{cost:.2f}"))
        self.total_label.configure(text=f"Total: {total:.2f} ฿")
        if not self.selected_treatments:
            messagebox.showinfo("No Selection", "Please select at least one treatment to check the bill.")