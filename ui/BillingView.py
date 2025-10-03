import customtkinter as ctk
from tkinter import ttk, messagebox

class BillingView:
    def __init__(self, parent, patient_repo):
        self.patient_repo = patient_repo
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self.frame, text="Billing", font=("Arial", 18)).pack(pady=10)

        self.patient_select = ttk.Combobox(self.frame, values=[p.full_name for p in self.patient_repo.data])
        self.patient_select.pack(pady=5)

        load_btn = ctk.CTkButton(self.frame, text="Load Bill", command=self.load_bill)
        load_btn.pack(pady=5)

        self.tree = ttk.Treeview(self.frame, columns=("Date", "Treatment", "Cost"), show="headings")
        for col in ("Date", "Treatment", "Cost"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="both", expand=True)

        self.total_label = ctk.CTkLabel(self.frame, text="Total: 0.00", font=("Arial", 14))
        self.total_label.pack(pady=10)

    def load_bill(self):
        patient_name = self.patient_select.get()
        if not patient_name:
            messagebox.showerror("Error", "Select a patient")
            return

        patient = next((p for p in self.patient_repo.data if p.full_name == patient_name), None)
        if not patient:
            messagebox.showerror("Error", "Patient not found")
            return

        # Clear tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        total = 0
        for date, treatments in patient.treatments.items():
            for treat in treatments:
                cost = 100.0  # Placeholder: later connect to treatment_price dict
                self.tree.insert("", "end", values=(date, treat, f"{cost:.2f}"))
                total += cost

        self.total_label.configure(text=f"Total: {total:.2f}")